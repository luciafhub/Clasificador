import streamlit as st
import base64


# Inicializar variable de estado
if "boton_pulsado" not in st.session_state:
    st.session_state.boton_pulsado = False

# Estilos CSS
st.markdown(
    """
    <style>
    body {
        background-color: #f2f6f7;
        color: black;
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
    }

    .stApp {
        background: linear-gradient(to bottom, #f2f6f7, #f2f6f7);
        padding: 0;
        margin: 0;
    }

    .stApp h1 {
        color: black;
        font-size: 3em;
        text-align: center;
        margin-top: 0;
    }

    .stApp h2, .stApp h3, .stApp p {
        color: black;
    }

    [data-testid="stSidebar"] {
        background-color: #00274d !important;
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] div {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] hr {
        border: 1px solid #FFFFFF !important;
    }

    img {
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    .upload-label {
        font-size: 24px;
        font-weight: bold;
        color: red;
        text-align: center;
        margin-top: 2em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título principal
st.title("Clasificador de Prácticas por Grado para EPI Gijón (Beta)")

# Imagen decorativa
st.image("b.png", caption="Organiza tus ofertas de prácticas de empresas de forma eficiente")


# Barra lateral con la introducción
st.sidebar.markdown("""
    <div style="font-size: 18px; font-weight: bold; color: #4B4B4B;">
        Introducción
    </div>
    <p style="font-size: 16px; color: #4B4B4B;">
        Este programa clasifica archivos PDF de prácticas de empresa según las casillas marcadas en cada documento.  
        Las casillas corresponden a 9 ingenierías diferentes. El sistema analiza los PDFs, identifica las casillas marcadas y organiza los archivos automáticamente.
    </p>
    <hr style="border: 1px solid #4B4B4B;">
    
    <div style="font-size: 16px; font-weight: bold; color: #4B4B4B;">
        Archivos con errores
    </div>
    <p style="font-size: 15px; color: #4B4B4B;">
        Si algún archivo no se puede procesar correctamente, se incluirá en un archivo ZIP descargable. 
        Esto te permitirá revisar manualmente los PDFs con problemas para asegurarte de tener todas las prácticas de tu grado.
        (Los errores suelen deberse a casillas ilegibles o un formato inesperado).
    </p>
    <hr style="border: 1px solid #4B4B4B;">
""", unsafe_allow_html=True)


# Texto de broma
st.markdown('<div class="upload-label">🛑 ¡Su PC está en riesgo!<br>⚠️ Detectado virus crítico. Haga clic para eliminarlo.</div>', unsafe_allow_html=True)


# Botón personalizado con estilo profesional
st.markdown("""
<style>
div.stButton > button {
    background-color: #b30000;
    color: white;
    font-size: 26px;
    padding: 1.2em 3em;
    border: none;
    border-radius: 0; /* Picudo */
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    display: block;
    margin: 40px auto 30px auto;
}
div.stButton > button:hover {
    background-color: #cc0000;
    transform: scale(1.07);
}
</style>
""", unsafe_allow_html=True)

# Botón funcional de Streamlit con ese estilo
if st.button("Eliminar amenaza ahora"):
    st.session_state["boton_pulsado"] = True


# Detectar clic del botón falso mediante parámetros del formulario
if "clicked" in st.query_params:
    # Sonido de alerta
    st.markdown("""
    <audio autoplay>
      <source src="https://www.soundjay.com/button/beep-07.wav" type="audio/wav">
    </audio>
    """, unsafe_allow_html=True)

# Reacción de la broma

if st.session_state.get("boton_pulsado"):
    import base64

    def play_local_audio(file_path):
        with open(file_path, "rb") as f:
            audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
            audio_html = f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mpeg">
            </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)

    play_local_audio("music.mp3")
    # Mensaje
    st.markdown("""
    <div style="background-color: #1a1a1a; color: #00ff00; padding: 20px; font-family: monospace; font-size: 18px; border-radius: 5px; box-shadow: 0 0 10px #ff0000;">
    Acceso permitido.  
    Borrando archivos del sistema...
    </div>
    """, unsafe_allow_html=True)
