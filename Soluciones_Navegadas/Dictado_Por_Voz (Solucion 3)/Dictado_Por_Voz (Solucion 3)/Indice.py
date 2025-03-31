import speech_recognition as sr

def print_microphone_list():
    # Obtener la lista de nombres de los dispositivos de entrada de audio
    microphones = sr.Microphone.list_microphone_names()

    print("Lista de dispositivos de entrada de audio:")
    for i, microphone_name in enumerate(microphones):
        print(f"{i}: {microphone_name}")

print_microphone_list()