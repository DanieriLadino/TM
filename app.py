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
.caja-trist
