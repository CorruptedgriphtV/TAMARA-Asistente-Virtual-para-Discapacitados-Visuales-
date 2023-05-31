import streamlit as st
import cv2
import numpy as np

def main():
    st.title("Aplicación de cámara en Streamlit")

    # Configurar la captura de video desde la cámara
    cap = cv2.VideoCapture(0)

    # Verificar si la cámara está disponible
    if not cap.isOpened():
        st.error("No se puede acceder a la cámara")
        return

    # Configurar las propiedades de la cámara
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Leer y mostrar el video desde la cámara
    while True:
        ret, frame = cap.read()

        # Verificar si se ha capturado correctamente el marco
        if not ret:
            st.warning("Error al capturar el marco")
            break

        # Convertir el marco a formato RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Mostrar el video en la página web
        st.image(frame_rgb, channels="RGB")

        # Verificar si el usuario ha presionado el botón "Detener"
        if st.button("Detener"):
            break

    # Liberar la cámara
    cap.release()

if __name__ == "__main__":
    main()