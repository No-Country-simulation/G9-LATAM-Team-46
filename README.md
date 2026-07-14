# G9-LATAM-Team-46
Desarrollar un MVP que clasifique y enriquezca automáticamente contenido técnico mediante Ciencia de Datos, expuesto vía una API REST integrada a OCI.


## Objetivo

Desarrollar un MVP que clasifique y enriquezca automáticamente contenido técnico
mediante Ciencia de Datos, expuesto vía una API REST integrada a OCI.

### Objetivos específicos

- Clasificar automáticamente contenido técnico por categoría temática (Backend, 
  Frontend, DevOps, Cloud, Bases de Datos, etc.) mediante un modelo entrenado con 
  técnicas de Ciencia de Datos (TF-IDF + Regresión Logística).
- Extraer palabras clave relevantes de cada contenido de forma automática.
- Exponer la funcionalidad mediante una API REST con validación de entrada, 
  manejo de errores y respuestas en formato JSON.
- Integrar la solución con servicios de OCI (Object Storage y Compute) para 
  garantizar almacenamiento y despliegue escalables.
- Reducir el esfuerzo manual de catalogación de contenido técnico para 
  estudiantes, equipos técnicos y plataformas educativas.

## Proceso de desarrollo

El proyecto se desarrolló en las siguientes etapas:

### 1. Definición del alcance
Se analizó el brief del hackathon y se definió el enfoque: clasificación 
temática + extracción de palabras clave, con clustering y recomendación de 
contenidos relacionados como funcionalidades opcionales. Se acordó el contrato 
de entrada/salida de la API antes de iniciar el desarrollo.

### 2. Construcción del dataset
Se recopilaron y etiquetaron manualmente entre 150 y 300 textos técnicos cortos, 
distribuidos en distintas categorías temáticas, provenientes de documentación 
pública, resúmenes de cursos y contenido propio del equipo.

### 3. Exploración y limpieza de datos (EDA)
Se realizó un análisis exploratorio del dataset: distribución de categorías, 
longitud de los textos y frecuencia de términos. Se aplicó limpieza de texto 
(normalización, eliminación de stopwords en español, tokenización).

### 4. Procesamiento y modelado
- Vectorización de los textos con **TF-IDF**.
- Entrenamiento de un modelo de **Regresión Logística** para la clasificación 
  temática, con partición de datos en entrenamiento y prueba.
- Extracción de palabras clave mediante los términos de mayor peso TF-IDF 
  por documento.
- Evaluación del modelo con métricas de *accuracy*, *F1-score* y matriz 
  de confusión.
- Serialización del modelo y el vectorizador entrenados con `joblib`.

### 5. Desarrollo de la API (Back-End)
Se construyó una API REST con **FastAPI** que:
- Recibe contenido técnico mediante el endpoint `POST /contenido`.
- Carga el modelo serializado y genera la predicción de categoría, 
  probabilidad y palabras clave asociadas.
- Valida los datos de entrada y maneja errores de forma explícita.
- Retorna los resultados en formato JSON.

### 6. Integración con OCI
- El modelo y el dataset se almacenaron en **OCI Object Storage**.
- La API se desplegó en una instancia de **OCI Compute**, la cual descarga 
  el modelo desde Object Storage al iniciar el servicio.

### 7. Pruebas y validación
Se ejecutaron al menos tres ejemplos de uso distintos sobre la API desplegada, 
verificando la correcta respuesta del servicio ante distintos tipos de 
contenido técnico.

### 8. Documentación
Se documentó el proyecto, incluyendo instrucciones de ejecución, uso de la 
API, ejemplos de solicitud/respuesta y dependencias utilizadas (ver sección 
"Cómo ejecutar el proyecto" más abajo).
