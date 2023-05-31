import cv2
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
import os
import pyttsx3

def main():
    # Configuración del modelo de IA
    model_url = "https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/classification/4"
    model = hub.load(model_url)

    # Capturar la imagen desde la cámara
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Mostrar la imagen en la consola
    img.show()

    # Guardar la imagen en un archivo temporal
    img_temp_path = "temp_img.jpg"
    img.save(img_temp_path)

    # Realizar la predicción con el modelo de IA
    img_tensor = tf.io.read_file(img_temp_path)
    img_tensor = tf.image.decode_jpeg(img_tensor, channels=3)
    img_tensor = tf.image.resize(img_tensor, [224, 224])
    img_tensor = tf.expand_dims(img_tensor, axis=0)
    img_tensor = img_tensor / 255.0

    predictions = model(img_tensor)
    predicted_label = tf.argmax(predictions, axis=1)

    # Mostrar el resultado de la predicción en la consola
    label_path = tf.keras.utils.get_file("ImageNetLabels.txt", "https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt")
    with open(label_path) as f:
        labels = f.readlines()
    object_recognized = labels[predicted_label[0]].strip()
    print("Objeto reconocido:", object_recognized)

    # Convertir el resultado en voz utilizando eSpeak
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(f"Objeto reconocido: {object_recognized}")
    engine.runAndWait()

    # Liberar la cámara y eliminar el archivo temporal
    cap.release()
    if os.path.exists(img_temp_path):
        os.remove(img_temp_path)

if __name__ == "__main__":
    main()