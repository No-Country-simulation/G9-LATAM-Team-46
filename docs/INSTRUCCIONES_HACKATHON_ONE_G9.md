# Hackathon ONE – Proyectos G9 | Alura + Oracle

**Equipo:** G9-LATAM-Team-46  
**Proyecto:** TechMind — Clasificación y organización inteligente de contenidos  
**Referencia oficial:** [proyectos-hackathon-g9-latam](https://alura-es-cursos.github.io/proyectos-hackathon-g9-latam/)

> Este documento conserva las **instrucciones oficiales del hackathon**.  
> La documentación operativa del MVP del equipo está en [`README.md`](./README.md).

---

## Sobre el Hackathon

Maratón de innovación para alumnos del programa **ONE** (Oracle Next Education), en la que se ponen en práctica los conocimientos adquiridos desarrollando soluciones reales con tecnología e inteligencia artificial.

### Objetivo del hackathon

Desarrollar **MVPs funcionales** que integren:

- Ciencia de Datos  
- API REST  
- Servicios de nube **OCI** (Oracle Cloud Infrastructure)

…para resolver problemas reales del mercado.

### Equipos

Los alumnos se organizan en grupos multidisciplinares en la plataforma **NoCountry**, uniendo perfiles de Back-End, Ciencia de Datos y más.

### Tecnologías principales

Python, Scikit-Learn, Java, Spring Boot y Oracle Cloud Infrastructure (OCI).

### Entregas del equipo

Cada equipo entrega:

1. Notebook de Data Science  
2. API REST documentada  
3. Integración con al menos un servicio OCI  

---

## Descripción del proyecto (TechMind)

Crear una solución que permita la **organización inteligente de contenido técnico**, facilitando su clasificación, consulta y reutilización.

La solución debe recibir textos técnicos (por ejemplo: descripciones de artículos, documentación, anotaciones de estudio, contenidos de cursos, tutoriales o materiales de referencia) y utilizar técnicas de **Ciencia de Datos** para identificar información relevante sobre ese contenido.

### Enfoques posibles

Los equipos podrán explorar diferentes enfoques, como:

- Clasificación temática del contenido  
- Identificación de palabras clave  
- Agrupación por temas similares  
- Recomendación de contenidos relacionados  
- Organización automática de bases de conocimiento  

El resultado deberá estar disponible en formato **JSON** para su consumo por otras aplicaciones.

Este tipo de solución puede ser utilizado por plataformas educativas, comunidades técnicas, empresas o profesionales que deseen construir repositorios inteligentes de conocimiento.

Opcionalmente, la solución puede complementarse con una interfaz sencilla para el registro, búsqueda o consulta de los contenidos procesados.

La solución **deberá integrarse con los servicios OCI** para el almacenamiento de modelos, documentos, despliegue de APIs y/o persistencia de datos.

### Sector

Plataformas educativas, documentación técnica y gestión del conocimiento corporativo.

### Stack técnico sugerido

| Área | Tecnologías |
|------|-------------|
| Ciencia de Datos | Python, Pandas, Scikit-Learn, TF-IDF |
| Back-End | Java, Spring Boot (u otra stack REST) |
| Nube | OCI (Object Storage, Compute, Functions, etc.) |

---

## Necesidad del cliente (explicación no técnica)

Profesionales y estudiantes de tecnología consumen diariamente una gran cantidad de contenido técnico, lo que dificulta organizar, localizar y reutilizar esta información posteriormente.

La solución debe permitir:

- Organizar contenidos automáticamente  
- Facilitar las búsquedas por temas o tópicos  
- Encontrar contenidos relacionados  
- Reducir el esfuerzo manual de catalogación  
- Construir una base de conocimiento reutilizable  

Esta solución permite transformar grandes volúmenes de información en conocimiento estructurado y de fácil acceso.

---

## Validación de mercado

Las herramientas de gestión del conocimiento son ampliamente utilizadas por empresas, equipos técnicos y plataformas educativas.

Las soluciones que automatizan la organización de contenidos pueden:

- Reducir el tiempo dedicado a la búsqueda de información  
- Mejorar la productividad  
- Facilitar el intercambio de conocimiento  
- Apoyar procesos de aprendizaje continuo  
- Escalar repositorios de conocimiento de manera eficiente  

Incluso las soluciones simples pueden generar valor al automatizar tareas repetitivas y mejorar el acceso a la información.

---

## Expectativa para este Hackathon

### Objetivo

Entregar un **MVP funcional** que permita organizar y enriquecer contenidos técnicos utilizando técnicas de Ciencia de Datos e integración con una API.

### Alcance recomendado

Los equipos podrán trabajar con uno o más enfoques, tales como:

- Clasificación de contenido  
- Agrupación de documentos  
- Extracción de palabras clave  
- Búsqueda semántica  
- Recomendación de contenidos relacionados  

La integración entre la aplicación y el modelo de Ciencia de Datos deberá ser definida por el equipo, considerando la arquitectura adoptada para la solución.

Se recomienda que la integración se realice de manera que permita **consumir el modelo a través de la API** desarrollada para el proyecto.

---

## Resultados esperados

### 1. Notebook del equipo de Ciencia de Datos (Jupyter/Colab)

Debe contener:

- Exploración y limpieza de datos (**EDA**)  
- Procesamiento de textos  
- Transformación de datos a un formato adecuado para el modelado  
- Entrenamiento y evaluación de modelos  
- Métricas de rendimiento apropiadas para la solución propuesta  
- Serialización del modelo (**joblib/pickle**)  

### 2. Aplicación Back-End (API REST)

La API debe incluir:

- Endpoints relacionados con la solución desarrollada  
- Recepción de contenido para su procesamiento  
- Retorno de los resultados generados por el modelo  
- Validación de entrada  
- Manejo de errores  

### 3. Integración con OCI

Sugerencias de uso:

| Servicio OCI | Uso sugerido |
|--------------|--------------|
| **Object Storage** | Almacenamiento de modelos o documentos |
| **OCI Compute** | Alojamiento de la aplicación |
| **OCI Functions** | Procesamiento específico |
| **Base de datos** (opcional) | Persistencia de datos |

> **Requisito obligatorio:** la solución debe utilizar **al menos un servicio OCI**.

### 4. Documentación mínima (README)

- Cómo ejecutar el proyecto  
- Cómo utilizar la API  
- Ejemplos de solicitud y respuesta  
- Dependencias y versiones utilizadas  

### 5. Demostración funcional

Presentar la solución en funcionamiento y explicar cómo los modelos utilizados generan los resultados.

---

## Funcionalidades requeridas (MVP)

El servicio debe exponer **al menos un endpoint** capaz de recibir contenido técnico y devolver información procesada por la solución desarrollada.

### Endpoint de ejemplo

`POST /contenido`

#### Entrada

```json
{
  "titulo": "Introducción a Spring Boot",
  "texto": "En este contenido se presentan los conceptos básicos para la creación de APIs REST utilizando Java y Spring Boot."
}
```

#### Salida

```json
{
  "categoria": "Backend",
  "probabilidad": 0.89,
  "informacion_adicional": [
    "Java",
    "Spring Boot",
    "API REST"
  ]
}
```

> La estructura final de la respuesta podrá variar según el enfoque elegido por el equipo.

---

## Requisitos obligatorios

| # | Requisito |
|---|-----------|
| 1 | Modelo entrenado y cargado |
| 2 | Procesamiento funcional del contenido |
| 3 | API operativa |
| 4 | Integración con OCI |
| 5 | Mínimo de tres ejemplos de uso |
| 6 | Documentación funcional |

### Checklist de entregas del MVP (resumen oficial)

- [ ] Notebook con EDA, entrenamiento y serialización del modelo  
- [ ] API REST con endpoint `POST /contenido` (o equivalente)  
- [ ] Retorno JSON con categoría, probabilidad y palabras clave (según enfoque)  
- [ ] Integración con al menos un servicio OCI  
- [ ] Mínimo de 3 ejemplos de uso documentados  

---

## Recursos opcionales

- Recomendación de contenidos relacionados  
- Búsqueda por palabras clave  
- Procesamiento por lotes (CSV)  
- Dashboard sencillo  
- Persistencia de resultados  
- Containerización con Docker  
- Pruebas automatizadas  
- Explicabilidad del modelo  
- Búsqueda semántica  
- Consulta por categorías  

---

## Directrices técnicas para estudiantes

### Ciencia de Datos

Cada equipo deberá construir su propia base de contenidos.

Los datos podrán ser:

- Obtenidos de fuentes públicas  
- Extraídos de documentación  
- Producidos por el propio equipo  

**Sugerencias de tecnologías:**

- Python  
- Pandas  
- Scikit-Learn  
- TF-IDF  
- Regresión Logística  
- Técnicas de similitud textual  

Se permite el uso de otros enfoques y modelos.

**Entregables del área:**

- EDA y preprocesamiento  
- Ingeniería de atributos  
- Entrenamiento y evaluación  
- Serialización del modelo  

### Back-End

Desarrollar una API REST utilizando las tecnologías trabajadas durante la formación.

La API deberá:

- Recibir los datos de entrada de la solución  
- Consumir el modelo desarrollado por el equipo de Ciencia de Datos  
- Devolver respuestas en formato JSON  
- Realizar validaciones y manejo de errores  
- Exponer los endpoints necesarios para el funcionamiento de la aplicación  

La arquitectura utilizada quedará a criterio del equipo y deberá estar documentada.

**Entregables del área:**

- API REST (p. ej. Spring Boot)  
- Integración con el modelo de DS  
- Validación y tratamiento de errores  
- Documentación de los endpoints  

### OCI (Oracle Cloud Infrastructure)

La solución debe utilizar **al menos un servicio OCI** como parte obligatoria del proyecto.

Opciones habituales:

- Object Storage  
- OCI Compute  
- OCI Functions  
- Base de datos (opcional)  

---

## Estructura esperada del repositorio

```text
.
├── README.md
├── INSTRUCCIONES_HACKATHON_ONE_G9.md
├── notebook/          # EDA, entrenamiento, evaluación, serialización
├── api/               # API REST
├── models/            # Modelo serializado (joblib/pickle)
├── data/              # Dataset del equipo
└── docs/              # Documentación adicional (opcional)
```

---

## Ejemplo de uso de la API (referencia del brief)

### Endpoint principal

`POST /contenido`

### Respuestas esperadas

| Código | Significado |
|--------|-------------|
| `200 OK` | Contenido procesado correctamente |
| `400 Bad Request` | Faltan campos obligatorios o el formato es inválido |
| `500 Internal Server Error` | Error inesperado del servidor |

### Tres ejemplos de uso (mínimo requerido)

#### 1. Clasificación de contenido Backend

**Entrada**

```json
{
  "titulo": "Construcción de APIs con FastAPI",
  "texto": "Este artículo explica cómo crear servicios REST modernos en Python."
}
```

**Salida esperada**

```json
{
  "categoria": "Backend",
  "probabilidad": 0.91,
  "informacion_adicional": ["Python", "FastAPI", "API REST"]
}
```

#### 2. Extracción de palabras clave / ML

**Entrada**

```json
{
  "titulo": "Fundamentos de ML",
  "texto": "El documento describe clasificación supervisada, TF-IDF y validación de modelos."
}
```

**Salida esperada**

```json
{
  "categoria": "Data Science",
  "probabilidad": 0.87,
  "informacion_adicional": ["clasificación supervisada", "TF-IDF", "validación de modelos"]
}
```

#### 3. Contenido relacionado (enfoque opcional)

**Entrada**

```json
{
  "titulo": "Normalización de datos",
  "texto": "Se presentan técnicas para limpiar y preparar datos antes del entrenamiento."
}
```

**Salida esperada**

```json
{
  "categoria": "Data Science",
  "probabilidad": 0.84,
  "informacion_adicional": ["limpieza de datos", "preprocesamiento"],
  "contenidos_relacionados": [
    "Preprocesamiento de texto",
    "Feature engineering",
    "Pipeline de ML"
  ]
}
```

---

## Socios del programa

- **Alura** — formación de los alumnos del programa ONE  
- **Oracle** — infraestructura Oracle Cloud  
- **Programa ONE** (Oracle Next Education) — iniciativa de educación en tecnología en Latinoamérica  
- **NoCountry** — organización de grupos e infraestructura colaborativa del Hackathon  

---

## Notas

Este archivo documenta el brief oficial del **Hackathon ONE – Proyectos G9** para el proyecto **TechMind**.

Para instrucciones de ejecución del MVP del equipo, ver [`README.md`](./README.md).
