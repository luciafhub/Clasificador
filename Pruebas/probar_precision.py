import fitz  # PyMuPDF
import os
from PIL import Image
import cv2
import numpy as np
import pandas as pd

# Función para convertir PDF a JPG
def pdf_to_jpg(pdf_path, output_folder):
    pdf_document = fitz.open(pdf_path)
    if pdf_document.page_count < 1:
        print(f"El PDF {pdf_path} no contiene páginas. Se omite.")
        return

    page = pdf_document[0]
    pix = page.get_pixmap(dpi=300)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_path = os.path.join(output_folder, os.path.basename(pdf_path).replace(".pdf", ".jpg"))
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img.save(output_path, "JPEG")

    print(f"Primera página de {pdf_path} guardada como JPG en: {output_path}")

# Función para procesar todos los PDFs
def process_pdfs(input_folder, output_folder):
    if not os.path.exists(input_folder):
        print(f"La carpeta {input_folder} no existe.")
        return

    pdf_files = [f for f in os.listdir(input_folder) if f.endswith(".pdf")]
    if not pdf_files:
        print(f"No se encontraron archivos PDF en la carpeta {input_folder}.")
        return

    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)
        pdf_to_jpg(pdf_path, output_folder)

# Función para recortar la imagen con plantilla
def crop_with_template(image_path, template_path, output_path):
    image = cv2.imread(image_path)
    template = cv2.imread(template_path, 0)

    if image is None or template is None:
        raise FileNotFoundError("No se pudo cargar la imagen o la plantilla")

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(result)
    x, y = max_loc
    h, w = template.shape
    cropped_img = image[y:y+h, x:x+w]
    cv2.imwrite(output_path, cropped_img)

# Función: analizar casillas revisando el centro
def analyze_casillas_by_center(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen: {image_path}")

    # Binarizar la imagen (invertida para destacar las marcas)
    _, binary_image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY_INV)

    # Detectar contornos
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[1])  # Ordenar de arriba a abajo

    results = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # Verificar tamaños típicos de casillas
        if 15 < w < 50 and 15 < h < 50:
            # Revisar el píxel central
            center_x, center_y = x + w // 2, y + h // 2
            if binary_image[center_y, center_x] == 255:
                results.append("Marcada")
            else:
                results.append("No marcada")

    return results

# Función principal para procesar imágenes
def process_all_images(input_folder, template_path, output_folder, excel_path):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    data = pd.read_excel(excel_path, header=0)
    data["PDFS"] = data["PDFS"].astype(str).str.strip()
    data.set_index("PDFS", inplace=True)

    problematic_images = []
    total_cases = 0
    correct_cases = 0

    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            input_path = os.path.join(input_folder, filename)
            cropped_path = os.path.join(output_folder, f"cropped_{filename}")

            try:
                crop_with_template(input_path, template_path, cropped_path)

                # Analizar casillas con la nueva función
                results = analyze_casillas_by_center(cropped_path)
                if len(results) != 9:
                    problematic_images.append((filename, len(results)))
                    continue

                image_number = filename.split("_")[1].split(".")[0]
                pdf_name = f"pr_{image_number}"
                if pdf_name in data.index:
                    expected_results = data.loc[pdf_name].tolist()
                    expected_results = ["Marcada" if val == 1 else "No marcada" for val in expected_results]

                    print(f"Resultados para {filename}:")
                    for i, (detected, expected) in enumerate(zip(results, expected_results), start=1):
                        status = "Correcto" if detected == expected else "Incorrecto"
                        print(f"  Casilla {i}: {detected} (Esperado: {expected}) - {status}")

                        total_cases += 1
                        if detected == expected:
                            correct_cases += 1
                else:
                    print(f"{filename}: No se encontraron datos esperados en el Excel.")
            except FileNotFoundError as e:
                print(f"Error al procesar {filename}: {e}")

    if problematic_images:
        print("\nImágenes con problemas detectadas:")
        for filename, count in problematic_images:
            print(f"  {filename}: Se detectaron {count} casillas (esperado: 9).")

    if total_cases > 0:
        accuracy = (correct_cases / total_cases) * 100
        print(f"\nPorcentaje de acierto: {accuracy:.2f}%")
    else:
        print("No se procesaron suficientes datos para calcular el porcentaje de acierto.")

# Carpetas y parámetros
pdf_input_folder = "OFERTAS TODAS"
pdf_output_folder = "ofertas_en_png"
template_path = "plantilla_casillas.jpg"
image_output_folder = "recorte_casillas"
excel_path = "nombres_precision.xlsx"

# Convertir PDFs a imágenes
process_pdfs(pdf_input_folder, pdf_output_folder)

# Procesar las imágenes resultantes
process_all_images(pdf_output_folder, template_path, image_output_folder, excel_path)
