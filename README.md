
# G9-LATAM – TEAM 46

# TechMind AI
### Plataforma Inteligente para la Organización de Contenido Técnico

---

# Descripción General

**TechMind AI** es una solución desarrollada durante el **Hackathon ONE G9 – Alura + Oracle**, cuyo propósito es automatizar la organización de contenido técnico mediante técnicas de **Ciencia de Datos**, **Procesamiento de Lenguaje Natural (NLP)** y **Machine Learning**.

La plataforma recibe información técnica, como artículos, documentación, tutoriales, apuntes de estudio y material de referencia, la analiza utilizando un modelo de clasificación entrenado por el equipo y devuelve información estructurada que facilita su consulta, reutilización y almacenamiento.

La solución expone sus funcionalidades mediante una **API REST**, permitiendo que cualquier aplicación pueda consumir los resultados de forma sencilla y estandarizada. Además, se integra con **Oracle Cloud Infrastructure (OCI)** para el almacenamiento del modelo y el despliegue de la aplicación.

---

# Problema

Actualmente, estudiantes, desarrolladores y profesionales de tecnología consumen diariamente grandes cantidades de documentación técnica proveniente de diferentes fuentes.

Sin embargo, gran parte de esta información queda dispersa y sin una estructura adecuada, lo que genera diversos inconvenientes:

- Dificultad para localizar información previamente consultada.
- Clasificación manual de documentos.
- Duplicidad de contenido.
- Baja reutilización del conocimiento.
- Pérdida de tiempo buscando información.

Las plataformas educativas y los equipos técnicos necesitan herramientas que permitan organizar automáticamente esta información para mejorar la productividad y facilitar el aprendizaje continuo.

---

# Nuestra Solución

**TechMind AI** automatiza la organización de contenido técnico mediante un flujo inteligente basado en Machine Learning.

Cuando un usuario envía un texto técnico, el sistema:

- Analiza el contenido recibido.
- Procesa el texto utilizando técnicas de NLP.
- Clasifica automáticamente el documento dentro de una categoría.
- Identifica las palabras clave más representativas.
- Calcula el nivel de confianza de la clasificación.
- Devuelve la información estructurada en formato JSON.

De esta manera, se reduce significativamente el tiempo dedicado a catalogar documentos y se facilita la construcción de repositorios inteligentes de conocimiento.

---

# Objetivo General

Desarrollar un MVP capaz de clasificar y enriquecer automáticamente contenido técnico mediante técnicas de Ciencia de Datos, exponiendo los resultados a través de una API REST integrada con Oracle Cloud Infrastructure (OCI).

---

# Objetivos Específicos

- Construir una base de datos propia de contenido técnico.
- Clasificar automáticamente documentos por categorías temáticas.
- Extraer palabras clave relevantes de cada documento.
- Implementar un modelo de Machine Learning para clasificación de texto.
- Exponer el modelo mediante una API REST.
- Validar entradas y gestionar errores de forma adecuada.
- Integrar la solución con Oracle Cloud Infrastructure.
- Documentar completamente el proyecto.
- Entregar un MVP funcional que pueda evolucionar posteriormente.

---

# Alcance del Proyecto

El MVP contempla las siguientes funcionalidades:

## Incluye

- Clasificación automática de contenido técnico.
- Extracción automática de palabras clave.
- Cálculo de la probabilidad de clasificación.
- API REST para consulta del modelo.
- Integración con Oracle Cloud Infrastructure.
- Documentación del proyecto.
- Casos de prueba.
- Despliegue funcional.

## No Incluye (Versión MVP)

- Autenticación de usuarios.
- Base de datos relacional.
- Historial de consultas.
- Panel administrativo.
- Recomendaciones inteligentes.
- Búsqueda semántica avanzada.
- Procesamiento masivo de archivos.

Estas funcionalidades quedan planteadas como mejoras para futuras versiones.

---

# Público Objetivo

La solución está dirigida a:

- Estudiantes de tecnología.
- Plataformas educativas.
- Equipos de desarrollo.
- Empresas de software.
- Empresas de manufactura.
- Comunidades técnicas.
- Profesionales del área TI.

---

# Arquitectura General

La solución está compuesta por cuatro módulos principales.

## Ciencia de Datos

Responsable de construir el dataset, preparar la información, entrenar el modelo y generar el archivo serializado que será utilizado por la API.

## API REST

Recibe el contenido enviado por el usuario, carga el modelo entrenado y devuelve la clasificación correspondiente junto con información adicional.

## Oracle Cloud Infrastructure

Se utiliza para almacenar el modelo entrenado y desplegar la aplicación, garantizando disponibilidad, escalabilidad y acceso desde la nube.

## Frontend

Interfaz sencilla para demostrar el funcionamiento del sistema, permitiendo ingresar contenido técnico y visualizar los resultados obtenidos por el modelo.

---

# Tecnologías Utilizadas

## Ciencia de Datos

- Python
- Pandas
- NumPy
- Scikit-Learn
- TF-IDF
- Regresión Logística
- Joblib

## Backend

- FastAPI
- Pydantic
- Uvicorn

## Cloud

- Oracle Cloud Infrastructure (OCI)
- OCI Object Storage
- OCI Compute

## Herramientas de Desarrollo

- Git
- GitHub
- Google Colab
- Docker
- Trello

---

# Metodología de Desarrollo

El proyecto se desarrolló utilizando una metodología colaborativa basada en iteraciones cortas.

Cada integrante fue responsable de un módulo específico mientras el líder coordinó la integración continua del proyecto.

El desarrollo se dividió en ocho etapas.

---

# Etapa 1 – Definición del Alcance

Durante esta etapa se analizó el reto planteado por el Hackathon.

Se definieron:

- Objetivos del proyecto.
- Alcance del MVP.
- Arquitectura general.
- Módulos del sistema.
- Flujo de funcionamiento.
- Contrato de entrada y salida de la API.

---

# Etapa 2 – Construcción del Dataset

El equipo recopiló contenido técnico proveniente de:

- Documentación oficial.
- Tutoriales.
- Artículos especializados.
- Material de estudio.
- Contenido elaborado por el propio equipo.

Posteriormente toda la información fue revisada, normalizada y clasificada manualmente por categorías.

---

# Etapa 3 – Exploración y Preparación de Datos

Se realizó un análisis exploratorio del dataset.

Las principales actividades fueron:

- Análisis de la distribución de categorías.
- Identificación de datos duplicados.
- Evaluación de la longitud de los documentos.
- Limpieza del texto.
- Eliminación de stopwords.
- Tokenización.
- Normalización del contenido.
- Preparación del dataset para entrenamiento.

---

# Etapa 4 – Entrenamiento del Modelo

Se desarrolló un modelo de clasificación de texto utilizando técnicas de Machine Learning.

Durante esta etapa se realizó:

- Vectorización del contenido.
- Entrenamiento del modelo.
- Evaluación del rendimiento.
- Comparación de resultados.
- Selección del mejor modelo.
- Serialización para producción.

---

# Etapa 5 – Desarrollo del Backend

Se implementó una API REST responsable de:

- Recibir contenido técnico.
- Ejecutar el modelo entrenado.
- Obtener la categoría correspondiente.
- Generar la probabilidad de clasificación.
- Extraer palabras clave.
- Retornar una respuesta estructurada en formato JSON.

La API incorpora validación de datos y manejo de errores.

---

# Etapa 6 – Integración con Oracle Cloud

Una vez finalizado el modelo y la API, ambos componentes fueron integrados con Oracle Cloud Infrastructure.

La solución utiliza:

- OCI Object Storage para almacenar el modelo.
- OCI Compute para ejecutar la aplicación.

---

# Etapa 7 – Validación del Proyecto

Se realizaron múltiples pruebas utilizando contenido técnico perteneciente a distintas categorías.

Se verificó:

- Correcta clasificación.
- Tiempo de respuesta.
- Consistencia de las respuestas.
- Manejo adecuado de errores.
- Correcto funcionamiento del despliegue.

---

# Etapa 8 – Documentación

Se elaboró la documentación técnica y funcional del proyecto.

Esta documentación incluye:

- Descripción de la solución.
- Arquitectura.
- Tecnologías utilizadas.
- Flujo de funcionamiento.
- Organización del equipo.
- Instrucciones de instalación.
- Ejemplos de uso.
- Casos de prueba.

---

# Beneficios de la Solución

La implementación de **TechMind AI** permite:

- Automatizar la clasificación de documentos.
- Reducir el tiempo de búsqueda de información.
- Mejorar la organización del conocimiento.
- Facilitar el aprendizaje continuo.
- Incrementar la productividad de equipos técnicos.
- Centralizar contenido técnico de forma estructurada.
- Facilitar la integración con otras aplicaciones mediante una API REST.

---

# Resultados Esperados

Con este MVP se espera demostrar que es posible utilizar técnicas de Ciencia de Datos para organizar automáticamente grandes volúmenes de contenido técnico de forma rápida, eficiente y escalable.

La solución constituye una base sólida para evolucionar hacia una plataforma inteligente de gestión del conocimiento incorporando funcionalidades como:

- Búsqueda semántica.
- Recomendación automática de contenidos.
- Clustering de documentos.
- Dashboard de administración.
- Procesamiento masivo de documentos.
- Persistencia de resultados.

---

# Equipo de Desarrollo

| Integrante 


| Lucio Fernández Chávez | Líder del Proyecto y Coordinador de Ciencia de Datos 

| David Fletes Esparza |  

| Sebastián Lugo |  

| Edson Alberto Herrera Cervantes |

| Willman Alca Alfaro |

| Daniel Soto | 

| Hipólito Pérez Martínez | 

| Edmer Rubio | 

---

# Conclusión

**TechMind AI** representa una solución práctica para la organización inteligente de contenido técnico mediante la integración de Ciencia de Datos, Machine Learning, APIs REST y Oracle Cloud Infrastructure.

El proyecto demuestra cómo la automatización puede transformar información dispersa en conocimiento estructurado, reutilizable y fácilmente accesible, constituyendo una base tecnológica escalable para futuras mejoras y nuevos casos de uso tanto en entornos educativos como empresariales.

