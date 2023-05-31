import cv2
import requests
from PIL import Image
import pyttsx3
import myopen
import os
def main():
    # Capturar la imagen desde la cámara
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Mostrar la imagen capturada
    img.show()

    # Guardar la imagen en un archivo temporal
    img_temp_path = "temp_img.jpg"
    img.save(img_temp_path)

    # Configurar la URL y las credenciales de la API de Computer Vision
    endpoint = "https://tamaraserver.cognitiveservices.azure.com/"
    subscription_key = "975da0dae182426ba219f03767e152ae"
    api_url = f"{endpoint}vision/v3.2/analyze"

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
        if "description" in result["description"]:
            description = result["description"]["captions"][0]["text"]
            print("Descripción generada por Azure:", description)

            # Generar descripción detallada con GPT-3.5
            prompt = "ERES UN ASISTENTE LLAMADO TAMARA, DESCRIBES QUE HAY EN LA IMAGEN Y PREGUNTAS EN QUE MAS PUEDES AYUDAR:"
            detailed_description = generate_text(prompt)

            # Imprimir y pronunciar la descripción generada
            print("Descripción detallada generada por GPT-3.5:", detailed_description)

            engine = pyttsx3.init()
            engine.say(description)
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
    myopen.api_key = "TU_CLAVE_API_GPT_3.5"

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