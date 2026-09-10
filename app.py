import streamlit as st
import numpy as np
from PIL import Image, ImageOps
from keras.models import load_model
import platform
import time
from datetime import datetime

st.set_page_config(page_title="Reconocimiento de Imágenes", page_icon="👍")

# ---------- ESTILOS Y ANIMACIONES ----------
st.markdown("""
<style>
.caja-feliz {
    background: linear-gradient(270deg, #00c9ff, #92fe9d, #f9d423, #ff4e50);
    background-size: 800% 800%;
    animation: fondoMovil 6s ease infinite, pulso 2s ease-in-out infinite;
    border-radius: 20px;
    padding: 25px;
    text-align: center;
    color: white;
    margin-bottom: 20px;
}
.emoji-salto {
    font-size: 80px;
    display: inline-block;
    animation: salto 1s ease infinite;
}
.texto-brillo {
    font-size: 26px;
    font-weight: bold;
    animation: brillo 1.5s ease-in-out infinite alternate;
}
@keyframes fondoMovil {
    0% {background-position: 0% 50%}
    50% {background-position: 100% 50%}
    100% {background-position: 0% 50%}
}
@keyframes pulso {
    0%, 100% {box-shadow: 0 0 10px rgba(146, 254, 157, 0.5)}
    50% {box-shadow: 0 0 35px rgba(146, 254, 157, 1)}
}
@keyframes salto {
    0%, 100% {transform: translateY(0) rotate(0deg)}
    50% {transform: translateY(-25px) rotate(-15deg)}
}
@keyframes brillo {
    from {text-shadow: 0 0 5px #fff}
    to {text-shadow: 0 0 20px #fff, 0 0 30px #ff00de}
}
.caja-triste {
    background: linear-gradient(180deg, #2c3e50, #4b6584);
    border-radius: 20px;
    padding: 25px;
    text-align: center;
    color: #dfe6e9;
    position: relative;
    overflow: hidden;
    min-height: 230px;
    margin-bottom: 20px;
}
.contenido {
    position: relative;
    z-index: 1;
}
.emoji-llanto {
    font-size: 80px;
    display: inline-block;
    animation: temblor 0.6s ease-in-out infinite;
}
.texto-triste {
    font-size: 24px;
    font-weight: bold;
    opacity: 0.85;
}
.gota {
    position: absolute;
    top: -30px;
    font-size: 22px;
    animation: lluvia linear infinite;
}
@keyframes temblor {
    0%, 100% {transform: translateX(0)}
    25% {transform: translateX(-5px)}
    75% {transform: translateX(5px)}
}
@keyframes lluvia {
    0% {transform: translateY(0); opacity: 0}
    10% {opacity: 1}
    100% {transform: translateY(300px); opacity: 0}
}
</style>
""", unsafe_allow_html=True)

# Lista donde se guardan los registros
if "registros" not in st.session_state:
    st.session_state.registros = []

st.write("Versión de Python:", platform.python_version())

# Cargar el modelo una sola vez (así la app no se pone lenta)
@st.cache_resource
def cargar_modelo():
    return load_model('keras_model.h5', compile=False)

model = cargar_modelo()

st.title("Reconocimiento de Imágenes")
image = Image.open('OIG5.jpg')
st.image(image, width=350)

with st.sidebar:
    st.subheader("Usando un modelo entrenado en Teachable Machine puedes usarlo en esta app para identificar")
    st.metric("personas registradas", len(st.session_state.registros))

img_file_buffer = st.camera_input("Toma una Foto")

if img_file_buffer is not None:
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Leer la foto y dejarla en 224x224 como la espera el modelo
    img = Image.open(img_file_buffer).convert("RGB")
    img = ImageOps.fit(img, (224, 224), Image.Resampling.LANCZOS)

    img_array = np.asarray(img)
    normalized_image_array = (img_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array

    # Predicción
    prediction = model.predict(data)
    prob_arriba = prediction[0][0]
    prob_abajo = prediction[0][1]

    # Revisar si la foto es nueva (para que las animaciones no se repitan sin razón)
    foto_id = hash(img_file_buffer.getvalue())
    foto_nueva = st.session_state.get("ultima_foto") != foto_id
    st.session_state["ultima_foto"] = foto_id

    # Barra de "escaneo" solo cuando llega una foto nueva
    if foto_nueva:
        barra = st.progress(0, text="analizando tu gesto... 🔍")
        for i in range(100):
            time.sleep(0.01)
            barra.progress(i + 1, text="analizando tu gesto... 🔍")
        barra.empty()

    # ---------- PULGAR ARRIBA: REGISTRO HABILITADO ----------
    if prob_arriba > 0.5:
        if foto_nueva:
            st.balloons()
            st.toast("¡acceso concedido! 🎉")

        st.markdown(
            '<div class="caja-feliz"><div class="emoji-salto">👍</div>'
            '<p class="texto-brillo">ok pulgar arriba detectado con éxito</p>'
            '<p>ya puedes hacer tu registro ✨</p></div>',
            unsafe_allow_html=True
        )
        st.image('pulgar_arriba.jpg', width=350)   # esta es la imagen que aparece

        st.subheader("📝 registro")
        with st.form("form_registro", clear_on_submit=True):
            nombre = st.text_input("nombre", key="nombre_registro")
            correo = st.text_input("correo", key="correo_registro")
            edad = st.number_input("edad", min_value=1, max_value=120, step=1, key="edad_registro")
            enviar = st.form_submit_button("registrarme 🚀")

        if enviar:
            if nombre.strip() == "" or correo.strip() == "":
                st.warning("completa tu nombre y tu correo para registrarte ✏️")
            else:
                st.session_state.registros.append({
                    "nombre": nombre,
                    "correo": correo,
                    "edad": int(edad),
                    "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
                })
                st.balloons()
                st.toast(f"¡bienvenido/a, {nombre}! 🥳")
                st.success(f"¡{nombre}, tu registro quedó guardado con éxito! 🎉")

        if st.session_state.registros:
            st.subheader("🏆 registrados")
            st.dataframe(st.session_state.registros)

    # ---------- PULGAR ABAJO: REGISTRO BLOQUEADO ----------
    elif prob_abajo > 0.5:
        if foto_nueva:
            st.snow()
            st.toast("registro bloqueado 😭")

        gotas = "".join(
            f'<span class="gota" style="left:{i * 9 + 3}%; '
            f'animation-duration:{1.2 + (i % 4) * 0.3}s; '
            f'animation-delay:{(i % 5) * 0.25}s;">💧</span>'
            for i in range(11)
        )
        st.markdown(
            f'<div class="caja-triste">{gotas}<div class="contenido">'
            '<div class="emoji-llanto">😢</div>'
            '<p class="texto-triste">pulgar abajo detectado con éxito</p>'
            '<p>el registro está bloqueado 🔒</p></div></div>',
            unsafe_allow_html=True
        )

        st.error("no puedes registrarte con el pulgar abajo 💔 toma otra foto con el pulgar arriba")

        st.subheader("🔒 registro bloqueado")
        st.text_input("nombre", disabled=True, key="nombre_bloqueado")
        st.text_input("correo", disabled=True, key="correo_bloqueado")
        st.button("registrarme", disabled=True, key="boton_bloqueado")

    else:
        st.write("No estoy seguro, intenta con otra foto.")
