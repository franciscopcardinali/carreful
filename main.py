import streamlit as st
from model import ProductoModel
from controller import SupermercadoController

# --- UNICA configuracion de pagina ---
st.set_page_config(
    page_title="Carreful", 
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def inicializar_core():
    # Local: "database.db" | Producción Render: "/opt/render/project/src/data/database.db"
    modelo = ProductoModel("database.db")
    controlador = SupermercadoController(modelo)
    return controlador

controlador = inicializar_core()

from view import inicializar_vista_web
inicializar_vista_web(controlador)