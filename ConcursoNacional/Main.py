import requests
import openai
import os
import subprocess
import pygame
from gtts import gTTS
import speech_recognition as sr
import time
from datetime import datetime

def play_sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def generate_text(prompt):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=100
    )
    generated_text = response.choices[0].text.strip()
    return generated_text

def take_photo(filename):
    command = "raspistill -o {}".format(filename)
    subprocess.run(command, shell=True)

def text_to_speech(text, filename):
    tts = gTTS(text=text, lang='es')
    tts.save(filename)
    subprocess.call(["mplayer", filename], shell=False)

def get_user_command():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='es-ES')
            return text
        except:
            return ""

def listen_for_activation():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        print("Sonido de activar")
        print("Esperando la orden de activación...")
        audio = r.record(source,duration=6)
        try:
            text = r.recognize_google(audio, language='es-ES')
            print(f"Usted dijo: {text}")
            if "tamara" in text.lower() or "activar" in text.lower():
                return True
            else:
                return False
        except:
            print("Lo siento, no entendí eso. Por favor, inténtalo de nuevo.")
            return False

api_key = "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"
openai.api_key = api_key

def main():
    endpoint = "https://tamaraserver.cognitiveservices.azure.com/"
    subscription_key = "975da0dae182426ba219f03767e152ae"
    api_url = f"{endpoint}vision/v3.2/analyze"
    description = ""
    inference_counter = 0

    while True:
        if listen_for_activation():
            print("Activación confirmada, ejecutando el programa...")

            play_sound("Intro.mp3")

            user_input = get_user_command()

            play_sound("Outro.mp3")
            time.sleep(1)
           # play_sound("Espera.mp3")
            if any(phrase in user_input.lower() for phrase in ["qué estoy viendo", "qué se ve", "que estoy viendo", "que se ve"]):
                img_temp_path = "temp_img.jpg"
                take_photo(img_temp_path)

                with open(img_temp_path, "rb") as image_file:
                    image_data = image_file.read()

                headers = {
                    "Content-Type": "application/octet-stream",
                    "Ocp-Apim-Subscription-Key": subscription_key
                }
                params = {
                    "visualFeatures": "Description",
                    "language": "es"
                }
                response = requests.post(api_url, headers=headers, params=params, data=image_data)

                if response.status_code == 200:
                    result = response.json()
                    if "description" in result and "captions" in result["description"]:
                        description = result["description"]["captions"][0]["text"]
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        with open("temp_description.txt", "a") as f:
                            f.write(timestamp + ": " + description + "\n")
                    else:
                        print("No se encontró una descripción en la respuesta de Azure.")
                else:
                    print("Error en la solicitud a Azure:", response.text)

                if os.path.exists(img_temp_path):
                    os.remove(img_temp_path)

                text_to_speech("Imagen reconocida: " + description, "output.mp3")
            
            with open("temp_description.txt", "r", encoding='ISO-8859-1') as f:
                saved_description = f.read()

            prompt = "Eres TAMARA, asistes a personas con discapacidad visual y tu objetivo es proporcionar una descripción detallada de la imagen y ayudar en lo que el usuario solicite, no inventes muchas cosas, solo retroalimenta a lo que ves .\n\nUsuario: {}\n\nDescripción de Azure: {}\n\nRespuesta:"
            prompt_with_input = prompt.format(user_input, saved_description)
            additional_assistance = generate_text(prompt_with_input)

            print("Respuesta adicional generada por GPT-3:", additional_assistance)
            text_to_speech(additional_assistance, "output.mp3")
            inference_counter += 1
            if inference_counter % 10 == 0:
                os.remove("temp_description.txt")
        else:
            print("Orden no reconocida, esperando la orden de activación.")

if __name__ == "__main__":
    main()
