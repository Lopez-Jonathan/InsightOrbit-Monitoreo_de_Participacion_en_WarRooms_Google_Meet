import speech_recognition as sr
import keyboard
from gtts import gTTS
from playsound import playsound
from pydub import AudioSegment
import os
import spacy

# Cargamos el modelo pre-entrenado en espanol de spaCY
nlp = spacy.load("es_core_news_sm")

def transcribe_voice(microphone_index):
    # Configurar el reconocimiento de voz
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=microphone_index)

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.1)  # Ajustar durante 0.5 segundos para capturar el ruido del ambiente

    speak("Escuchando.")
    audio = None
    try:
        with microphone as source:
            audio = recognizer.listen(source, timeout=0.8)
    except sr.WaitTimeoutError:
        pass

    if audio:
        try:
            # Transcribir el audio a texto
            text = recognizer.recognize_google(audio, language="es-ES")
            # Procesar el texto con spaCY para realizar NAMED Entity Recognition (NER)
            doc = nlp(text)
            # Filtrar las entidades nombradas que sean PERSON (Personas)
            formatted_names = [ent.text for ent in doc.ents if ent.label_ == "PER"]
            #Unir los nombres con comas
            formatted_text = ', '.join(formatted_names)
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

def main():
    microphone_index = 1  # Índice del micrófono del auricular
    listening = 0
    audio=0
    url= 'SLACK_WEBHOOK'
    # Esperar hasta que se presione Ctrl + C para salir
    speak("Presionar ESCAPE para iniciar escucha o Ctrl + C para finalizar el programa")
    try:
        while True:
            # Verificar si la tecla 'Esc' está siendo presionada
            if keyboard.is_pressed('esc'):
                listening += 1
                speak("Comenzando la escucha de voz.\nAjustando el microfono, para el ruido ambiente.")
                while listening == 1:
                    text = transcribe_voice(microphone_index)
                    if text:
                        speak("Deteniendo la escucha de voz.")
                        with open("C:/Users/Voolkia/Desktop/nombres.txt", "a") as file:
                            file.write(text + "\n")
                        listening += 1
                    else:
                        audio+=1
                        if audio == 1:
                            speak("No se detectó audio después de varios intentos.\nDeteniendo la escucha...")
                            listening = 0  # Salir del bucle de escucha
            else:
                listening = 0
                audio=0

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
