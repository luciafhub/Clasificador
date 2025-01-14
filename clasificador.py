import fitz
import os
from PIL import Image
import cv2
import numpy as np
import streamlit as st
import zipfile
import time 

# Configuración de estilos CSS para un diseño atractivo
st.markdown(
    """
    <style>
    /* Fondo completo de la aplicación */
    body {
        background-color: #f2f6f7; /* Azul lavanda */
        color: black; /* Texto negro */
        font-family: 'Arial', sans-serif;
        margin: 0; /* Eliminar márgenes predeterminados */
        padding: 0; /* Eliminar padding predeterminado */
    }

    /* Contenedor principal */
    .stApp {
        background: linear-gradient(to bottom, #f2f6f7, #f2f6f7); /* Gradiente uniforme */
        padding: 0; /* Reducir padding superior del contenedor */
        margin: 0; /* Eliminar márgenes */
    }

    /* Encabezado principal */
    .stApp h1 {
        color: black; /* Texto negro */
        font-size: 3em;
        text-align: center;
        margin-top: 0; /* Eliminar margen superior */
    }

    /* Texto y subtítulos */
    .stApp h2, .stApp h3, .stApp p {
        color: black; /* Texto negro */
    }

    /* Fondo de la barra lateral */
    [data-testid="stSidebar"] {
        background-color: #00274d !important; /* Azul oscuro */
        color: #FFFFFF !important; /* Texto blanco */
    }

    /* Elementos de la barra lateral */
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] div {
        color: #FFFFFF !important; /* Texto completamente blanco */
    }

    /* Divisores */
    [data-testid="stSidebar"] hr {
        border: 1px solid #FFFFFF !important; /* Divisor blanco */
    }

    /* Imágenes */
    img {
        border-radius: 15px; /* Bordes redondeados */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Sombra */
    }
    </style>
    """,
    unsafe_allow_html=True
)



# Diccionario que asocia cada casilla a una ingeniería
ingenierias = {
    1: "Ingeniería de Telecomunicación",
    2: "Ingeniería Informática",
    3: "Ciencia e Ingeniería de Datos",
    4: "Ingeniería en Tecnologías Industriales",
    5: "Ingeniería de Organización Industrial",
    6: "Ingeniería Mecánica",
    7: "Ingeniería Química Industrial",
    8: "Ingeniería Eléctrica",
    9: "Ingeniería Electrónica Industrial y Automática",
}

# Función para convertir PDF a JPG
def pdf_to_jpg(pdf_path, output_folder):
    pdf_document = fitz.open(pdf_path)
    if pdf_document.page_count < 1:
        print(f"El PDF {pdf_path} no contiene páginas. Se omite.")
        return

    # Extraer la primera página
    page = pdf_document[0]
    pix = page.get_pixmap(dpi=300)  # Cambia DPI según la calidad deseada

    # Crear carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Guardar como imagen JPG
    output_path = os.path.join(output_folder, os.path.basename(pdf_path).replace(".pdf", ".jpg"))
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img.save(output_path, "JPEG")

    return output_path

# Función para recortar la imagen usando una plantilla
def crop_with_template(image_path, template_path, output_path):
    image = cv2.imread(image_path)
    template = cv2.imread(template_path, 0)

    if image is None or template is None:
        raise FileNotFoundError("No se pudo cargar la imagen o la plantilla")

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED) # con matchTemplate 
    _, _, _, max_loc = cv2.minMaxLoc(result)
    x, y = max_loc
    h, w = template.shape

    if cropped_img is None:
        raise ValueError(f"La imagen recortada está vacía. Revisa la plantilla: {template_path}")
    cv2.imwrite(output_path, cropped_img)

    cropped_img = image[y:y+h, x:x+w]
    cv2.imwrite(output_path, cropped_img)

# Función para analizar casillas revisando el centro
def analyze_casillas_by_center(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen: {image_path}")

    _, binary_image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[1])

    results = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if 15 < w < 50 and 15 < h < 50:
            center_x, center_y = x + w // 2, y + h // 2 # punto central de la casilla
            if binary_image[center_y, center_x] == 255:
                results.append("Marcada")
            else:
                results.append("No marcada")
    return results


# Función para procesar y clasificar archivos
def process_and_classify(uploaded_files, template_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    classification = {key: [] for key in ingenierias.keys()}
    problematic_images = []

    for uploaded_file in uploaded_files:
        pdf_path = os.path.join(output_folder, uploaded_file.name)
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.read())

        jpg_path = pdf_to_jpg(pdf_path, output_folder)
        cropped_path = os.path.join(output_folder, f"cropped_{os.path.basename(jpg_path)}")

        try:
            crop_with_template(jpg_path, template_path, cropped_path)
            results = analyze_casillas_by_center(cropped_path)

            if len(results) != 9:
                problematic_images.append(uploaded_file.name)
                continue

            for idx, state in enumerate(results, start=1):
                if state == "Marcada":
                    classification[idx].append(uploaded_file.name)

        except FileNotFoundError as e:
            print(f"Error al procesar {uploaded_file.name}: {e}")
            problematic_images.append(uploaded_file.name)

    return classification, problematic_images

# Streamlit UI
st.title("Clasificador de Prácticas por Grado para EPI Gijón")

# Imagen principal
st.image("b.png", caption="Organiza tus ofertas de prácticas de empresas de forma eficiente", use_container_width=True)


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



# Personalizar el estilo del texto del cargador de archivos
st.markdown(
    """
    <style>
    .upload-label {
        font-size: 18px; /* Cambia el tamaño de la fuente */
        font-weight: bold; /* Opcional: poner en negrita */
        color: #4B4B4B; /* Cambia el color si lo deseas */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Mostrar el cargador de archivos con la clase personalizada
st.markdown('<div class="upload-label">📂 Sube tus archivos PDF aquí:</div>', unsafe_allow_html=True)
uploaded_files = st.file_uploader("", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    template_path = "plantilla_casillas.jpg"
    output_folder = "temp_output"

    # Crear carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Inicializar datos en session_state
    if "classification_data" not in st.session_state:
        st.session_state.classification_data = {key: [] for key in ingenierias.keys()}
        st.session_state.problematic_images = []
        st.session_state.files_processed = False

    # Procesar los archivos solo si no han sido procesados previamente
    if not st.session_state.files_processed:
        st.write("Procesando los archivos...")
        progress = st.progress(0)

        for i, uploaded_file in enumerate(uploaded_files, start=1):
            pdf_path = os.path.join(output_folder, uploaded_file.name)
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.read())

            jpg_path = pdf_to_jpg(pdf_path, output_folder)
            if not jpg_path:
                st.session_state.problematic_images.append(uploaded_file.name)
                continue

            cropped_path = os.path.join(output_folder, f"cropped_{os.path.basename(jpg_path)}")

            try:
                crop_with_template(jpg_path, template_path, cropped_path)
                results = analyze_casillas_by_center(cropped_path)

                if len(results) != 9:
                    st.session_state.problematic_images.append(uploaded_file.name)
                    continue

                for idx, state in enumerate(results, start=1):
                    if state == "Marcada":
                        st.session_state.classification_data[idx].append(uploaded_file.name)

            except FileNotFoundError as e:
                st.session_state.problematic_images.append(uploaded_file.name)

            progress.progress(int((i / len(uploaded_files)) * 100))

        st.success("✅ Archivos procesados correctamente.")
        st.session_state.files_processed = True

    # Mostrar imágenes problemáticas
    if st.session_state.problematic_images:
        st.warning("⚠️ Algunos archivos no se pudieron procesar correctamente:")
        for filename in st.session_state.problematic_images:
            st.write(f"- {filename}")

        zip_path_problems = "problematic_pdfs.zip"
        with zipfile.ZipFile(zip_path_problems, "w") as zipf:
            for pdf_path in st.session_state.problematic_images:
                zipf.write(os.path.join(output_folder, pdf_path), pdf_path)
        with open(zip_path_problems, "rb") as f:
            st.download_button(
                label="Descargar PDFs con problemas",
                data=f,
                file_name="pdfs_problemas.zip",
                mime="application/zip",
            )

    # Selección de ingeniería
    selected_engineering = st.selectbox("Selecciona una ingeniería:", ["Seleccione una ingeniería..."] + list(ingenierias.values()))

    if selected_engineering != "Seleccione una ingeniería...":
        selected_key = list(ingenierias.keys())[list(ingenierias.values()).index(selected_engineering)]

        st.write(f"PDFs disponibles para {selected_engineering}:")
        filtered_pdfs = st.session_state.classification_data[selected_key]
        if filtered_pdfs:
            for pdf in filtered_pdfs:
                st.write(f"- {pdf}")

            zip_path = "filtered_pdfs.zip"
            with zipfile.ZipFile(zip_path, "w") as zipf:
                for pdf_path in filtered_pdfs:
                    zipf.write(os.path.join(output_folder, pdf_path), pdf_path)
            with open(zip_path, "rb") as f:
                st.download_button(
                    label="Descargar PDFs",
                    data=f,
                    file_name="practicas_filtradas.zip",
                    mime="application/zip",
                )
        else:
            st.write("No hay PDFs disponibles para esta ingeniería.")
