# Clasificador de Prácticas por Grado para EPI Gijón

Este proyecto es una aplicación web desarrollada con Streamlit que permite clasificar archivos PDF de prácticas de empresa según las casillas marcadas, organizándolos automáticamente por grado de ingeniería.

🌐 Acceso a la Aplicación

👉 Usa la aplicación directamente aquí: Clasificador de Prácticas EPI Gijón

🛠️ Funcionalidades

Conversión de PDFs a imágenes: Convierte la primera página del PDF a JPG.

Recorte de imágenes: Utiliza una plantilla para recortar áreas específicas de las imágenes.

Análisis de casillas: Detecta si las casillas están marcadas o no.

Clasificación automática: Organiza los PDFs según la ingeniería seleccionada.

Gestión de errores: Los PDFs que no se procesan correctamente se agrupan en un ZIP descargable.

📂 Uso de la aplicación

Carga de archivos PDF: Sube uno o varios PDFs usando el botón de carga.

Procesamiento: El sistema analiza los PDFs y clasifica los documentos.

Descarga:

PDFs correctamente clasificados.

ZIP con PDFs que presentaron errores.

Filtrado por ingeniería: Selecciona la ingeniería para ver los PDFs relacionados.

📄 Estructura del Proyecto

├── clasificador.py         # Código principal de la app
├── plantilla_casillas.jpg  # Plantilla para recortar las imágenes
├── temp_output/            # Carpeta temporal para imágenes procesadas
├── requirements.txt        # Dependencias necesarias
└── README.md               # Documentación del proyecto

🐞 Posibles errores

Error en la carga de imágenes: Puede ser por PDFs corruptos o casillas ilegibles.

Error de dependencias: Asegúrate de usar opencv-python-headless en lugar de opencv-python en Streamlit Cloud.

🤝 Contribuciones

¡Las contribuciones son bienvenidas! Abre un issue o envía un pull request.

📜 Licencia

Este proyecto está bajo la licencia MIT.

Desarrollado por: Lucía Fernández Rodríguez

