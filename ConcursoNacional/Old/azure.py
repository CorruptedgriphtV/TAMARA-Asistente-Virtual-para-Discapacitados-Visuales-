import cv2
import requests
import pyttsx3
import myopen
import os

def main():
    # Capturar la imagen desde la cámara
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    # Configurar la URL y las credenciales de la API de Computer Vision
    endpoint = "https://tamaraserver.cognitiveservices.azure.com/"
    subscription_key = "975da0dae182426ba219f03767e152ae"
    api_url = f"{endpoint}vision/v3.2/analyze"

    # Guardar la imagen en un archivo temporal
    img_temp_path = "temp_img.jpg"
    cv2.imwrite(img_temp_path, frame)

    # Leer la imagen como bytes
    with open(img_temp_path, "rb") as image_file:
        image_data = image_file.read()

    # Realizar la solicitud a la API de Computer Vision
    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": subscription_key
    }
    params = {
        "visualFeatures": "Description"
    }
    response = requests.post(api_url, headers=headers, params=params, data=image_data)

    # Procesar la respuesta de la API de Computer Vision
    if response.status_code == 200:
        result = response.json()
        if "description" in result and "captions" in result["description"]:
            description = result["description"]["captions"][0]["text"]
            print("Descripción generada por Azure:", description)

            # Configurar las credenciales de la API de GPT-3
            api_key = "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"
            myopen.api_key = api_key

            # Generar descripción detallada con GPT-3
            prompt = "Eres TAMARA, asistes a personas con discapacidad visual y tu objetivo es proporcionar una descripción detallada de la imagen y ayudar en lo que el usuario solicite.\n\nInput: {}\n\n¿En qué puedo ayudarte?"
            user_input = input("Ingrese su solicitud: ")

            prompt_with_input = prompt.format(user_input)
            detailed_description = generate_text(prompt_with_input)

            # Imprimir y pronunciar la descripción generada por GPT-3
            print("Descripción detallada generada por GPT-3:", detailed_description)
            engine = pyttsx3.init()
            engine.say(detailed_description)
            engine.runAndWait()

        else:
            print("No se encontró una descripción en la respuesta de Azure.")
    else:
        print("Error en la solicitud a Azure:", response.text)

    # Liberar la cámara y eliminar el archivo temporal
    cap.release()
    if os.path.exists(img_temp_path):
        os.remove(img_temp_path)

def generate_text(prompt):
    response = myopen.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
        top_p=None,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].text.strip()

if __name__ == "__main__":
    main()