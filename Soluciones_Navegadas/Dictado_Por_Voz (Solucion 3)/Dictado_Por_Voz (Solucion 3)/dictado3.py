import speech_recognition as sr
from gtts import gTTS
import keyboard
from playsound import playsound
from pydub import AudioSegment
import os
import spacy
import requests
import json
import sys

# Cargamos el modelo pre-entrenado en español de spaCy
nlp = spacy.load("es_core_news_sm")

def transcribe_voice(microphone_index):
    # Configurar el reconocimiento de voz
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=microphone_index)

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Ajustar durante 0.5 segundos para capturar el ruido del ambiente

    speak("Escuchando.")
    audio = None
    try:
        with microphone as source:
            audio = recognizer.listen(source, timeout=8)
    except sr.WaitTimeoutError:
        pass

    if audio:
        try:
            # Transcribir el audio a texto
            text = recognizer.recognize_google(audio, language="es-ES")
            # Procesar el texto con spaCy para realizar NER
            doc = nlp(text)
            # Filtrar las entidades nombradas que sean PERSON
            formatted_names = [ent.text for ent in doc.ents if ent.label_ == "PER"]
            # Unir los nombres con comas
            formatted_text = '\n'.join(formatted_names)
            speak("Texto transcribido:" + formatted_text)
            return formatted_text
        except sr.UnknownValueError:
            speak("No se pudo entender el audio")
        except sr.RequestError as e:
            speak("Error al solicitar resultados del servicio de reconocimiento de voz; {0}".format(e))

    return None

def speak(*messages, speed=1):
    #Concatenar todos los mensajes en uno solo
    full_message = " ".join(messages)
    # Guardar el mensaje en un archivo de audio
    tts = gTTS(text=full_message, lang='es')
    tts.save("C:/Users/Voolkia/Documents/temp.mp3")
    # Cambiar la velocidad del archivo de audio
    sound = AudioSegment.from_mp3("C:/Users/Voolkia/Documents/temp.mp3")
    sound = sound.speedup(playback_speed=speed)
    sound.export("temp.mp3", format="mp3")
    # Reproducir el archivo de audio
    playsound("C:/Users/Voolkia/Documents/temp.mp3")
    # Eliminar el archivo de audio despues de reproducirlo
    os.remove("C:/Users/Voolkia/Documents/temp.mp3")

def send_message_to_slack(message, webhook_url, incident_id=None, sites=None, metrics=None, products=None):
    formatted_message = ""
    if incident_id:
        formatted_message += f"ID del incidente: {incident_id}\n"
    if sites:
        formatted_message += f"Sitios: {sites}\n"
    if metrics:
        formatted_message += f"Métricas: {metrics}\n"
    if products:
        formatted_message += f"Productos: {products}\n"
    formatted_message += f"Nombres:\n{message}"

    payload = {'text': formatted_message}
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 200:
        print("Mensaje enviado correctamente a Slack.")
    else:
        print(f"Error al enviar el mensaje a Slack: {response.text}")

def extract_data_from_request(data):
    try:
        extracted_data = []
        for incident_data in data:
            incident_id = incident_data["id"]
            incident = incident_data["incident"]
            data_within_incident = incident["data"]
            sites = data_within_incident["sites"]
            metrics = data_within_incident.get("metrics", [])
            products = data_within_incident.get("products", [])
            extracted_data.append({
                "incident_id": incident_id,
                "sites": sites,
                "metrics": metrics,
                "products": products
            })
        return extracted_data
    except Exception as e:
        print(f"Error al extraer datos de la solicitud: {e}")
        return []

def main(data):
    microphone_index = 1
    webhook_url = 'SLACK_WEBHOOK'

    speak("Presionar ESCAPE para iniciar escucha o Ctrl + C para finalizar el programa")
    try:
        extracted_data = extract_data_from_request(data)
        if not extracted_data:
            print("No se encontraron datos de incidentes válidos.")
            return

        for incident_data in extracted_data:
            incident_id = incident_data["incident_id"]
            sites = incident_data["sites"]
            metrics = incident_data["metrics"]
            products = incident_data["products"]
            transcriptions = []
            speak(f"Iniciando escucha para incidente con ID {incident_id}. Ajustando el micrófono para el ruido ambiente.")
            processing_incident = True
            while processing_incident:
                if keyboard.is_pressed('esc'):
                    speak("Comenzando la escucha de voz.")
                    text = transcribe_voice(microphone_index)
                    if text:
                        transcriptions.append(text)
                        speak("¿Desea agregar más nombres? (Presione Ctrl + s para sí o Ctrl + p para no)")
                        response = None
                        while response is None:
                            if keyboard.is_pressed('ctrl+s'):
                                speak("Escuchando nuevamente")
                                text = transcribe_voice(microphone_index)
                                if text:
                                    transcriptions.append(text)
                                    speak("Quiere seguir agregando nombres? Presione Ctrl + s en caso contrario Ctrl + p")
                                else:
                                    speak("No se detectó audio después de varios intentos. Si quiere probar agregar nuevamente aprete Ctrl + s caso contrario Ctrl + p")
                            elif keyboard.is_pressed('ctrl+p'):
                                speak("Deteniendo la escucha de voz.")
                                all_transcriptions = '\n'.join(transcriptions)
                                send_message_to_slack(all_transcriptions, webhook_url, incident_id=incident_id, sites=sites, metrics=metrics, products=products)
                                processing_incident = False
                                break
                    else:
                        speak("No se detectó audio después de varios intentos.\nDeteniendo la escucha...")
                        processing_incident = False

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        data = json.loads(sys.argv[1])
        main(data)
    else:
        print("No se proporcionaron datos. El programa se está ejecutando sin datos de entrada.")
