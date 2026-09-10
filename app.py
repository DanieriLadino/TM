import streamlit as st
import numpy as np
from PIL import Image, ImageOps
from keras.models import load_model
import platform

st.write("Versión de Python:", platform.python_version())

@st.cache_resource
def cargar_modelo():
    return load_model('keras_model.h5', compile=False)

model = cargar_modelo()

st.title("Reconocimiento de Imágenes")
image = Image.open('OIG5.jpg')
st.image(image, width=350)

with st.sidebar:
    st.subheader("Usando un modelo entrenado en Teachable Machine puedes usarlo en esta app para identificar")

img_file_buffer = st.camera_input("Toma una Foto")

if img_file_buffer is not None:
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    img = Image.open(img_file_buffer).convert("RGB")
    img = ImageOps.fit(img, (224, 224), Image.Resampling.LANCZOS)

    img_array = np.asarray(img)
    normalized_image_array = (img_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array

    prediction = model.predict(data)
    prob_arriba = prediction[0][0]
    prob_abajo = prediction[0][1]

    if prob_arriba > 0.5:
        st.header("pulgar arriba")
        st.image('pulgar_arriba.jpg', width=350)
    elif prob_abajo > 0.5:
        st.header("pulgar abajo")
