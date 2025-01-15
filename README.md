# Clasificador de Prácticas por Grado para EPI Gijón

Este proyecto es una aplicación web desarrollada con Streamlit que permite clasificar archivos PDF de prácticas de empresa según las casillas marcadas, organizándolos automáticamente por grado de ingeniería.

## 🌐 Acceso a la Aplicación

👉 **Usa la aplicación directamente aquí:** [Clasificador de Prácticas EPI Gijón](https://clasificador-ingenierias.streamlit.app/)

## 🛠️ Funcionalidades

- **Conversión de PDFs a imágenes:** Convierte la primera página del PDF a JPG.  
- **Recorte de imágenes:** Utiliza una plantilla para recortar áreas específicas de las imágenes.  
- **Análisis de casillas:** Detecta si las casillas están marcadas o no según su zona central.  
- **Clasificación automática:** Organiza los PDFs según la ingeniería seleccionada.  
- **Gestión de errores:** Los PDFs que no se procesan correctamente se agrupan en un ZIP descargable.  

## 📂 Uso de la aplicación

1. **Carga de archivos PDF:** Sube uno o varios PDFs usando el botón de carga.  
2. **Procesamiento:** El sistema analiza los PDFs y clasifica los documentos.  
3. **Descarga:**  
   - PDFs correctamente filtrados por ingeniería.  
   - ZIP con PDFs que presentaron errores.

   
## 🧪 Validación del Modelo

Dentro de la carpeta **`pruebas/`** se encuentra un script llamado **`script_verificacion.py`** y un archivo **`nombres_precision.xlsx`** para verificar la precisión del clasificador.

- **`script_verificacion.py`:** Procesa los PDFs (que están el carpeta "OFERTAS TODAS" y/o en los .zip) y verifica si la clasificación fue correcta comparándola con los datos del Excel.
- **`nombres_precision.xlsx`:** Contiene los resultados esperados. Tiene tantas filas como PDFs procesados y 9 columnas, una por cada ingeniería. Si un PDF tiene una casilla marcada, el valor es **1**.
- **El archivo `nombres_precision.xlsx` fue creado manualmente**, revisando cada PDF uno por uno y marcando con un **1** las casillas correspondientes a cada ingeniería. Esto permite verificar si el programa clasifica correctamente los PDFs.
- La verificación demuestra que el clasificador alcanza una **precisión del 100%** sobre un conjunto de **142 PDFs**.


## 🐞 Posibles errores

- **Error en el procesamiento de casillas:** Puede ser por PDFs con un formato inesperado o casillas ilegibles. Si esto sucede, se guardan en una carpeta para descargar los PDFs problemáticos y así revisarlos manualmente.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Abre un issue o envía un pull request.

---

**Desarrollado por:** Lucía Fernández Rodríguez
