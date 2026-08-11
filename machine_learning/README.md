# TechMind 
## Descripción Este flujo de trabajo de Machine Learning está diseñado para la clasificación automatizada de información técnica dentro de entornos de desarrollo colaborativo y comunidades de aprendizaje. Para determinar la estrategia más eficiente para el proyecto TechMind, se implementó un análisis comparativo entre modelos de **Regresión Logística** y **Naive Bayes**, evaluando su capacidad de predicción mediante métricas de exactitud (accuracy) y precisión. El sistema se sustenta en un pipeline de procesamiento de lenguaje natural (NLP) que estandariza, limpia y analiza textos técnicos complejos, permitiendo asignar cada entrada a su categoría correspondiente con alta fiabilidad. ## Características Principales  **Pipeline de Procesamiento Automatizado:** Limpieza, normalización y análisis de textos técnicos complejos para garantizar la calidad de los datos.  **Ingeniería de Características:** Utiliza vectorización TF-IDF con stop words personalizadas en inglés y español.  **Modelos de Clasificación:** Análisis comparativo entre Regresión Logística y Naive Bayes, con optimización de hiperparámetros mediante GridSearchCV para asegurar la máxima eficiencia. 
Escalabilidad: Diseñado para manejar flujos constantes de información en entornos profesionales. 
## Metodología El flujo de trabajo se centra en un pipeline que procesa, limpia y analiza textos complejos, permitiendo asignar categorías de forma precisa: 
1. Limpieza: Normalización de texto y eliminación de ruido (URLs, HTML, caracteres especiales) preservando términos técnicos críticos. 
2. Vectorización: Transformación de texto a formato numérico mediante TF-IDF. 
3. Entrenamiento: Evaluación comparativa entre Regresión Logística y Naive Bayes para determinar la mejor solución para el proyecto. 
4. Optimización: Ajuste fino del modelo seleccionado utilizando GridSearchCV para obtener los mejores hiperparámetros. 
## Tecnologías Utilizadas 
Lenguaje: Python  
Machine Learning: Scikit-Learn  
NLP: Librerías de procesamiento de texto y vectores TF-IDF 
Entorno: Visual Studio Code 
## Instalación 
1. Clonar el repositorio. 
2. Instalar las dependencias necesarias: `pip install -r requirements.txt` 
3. Ejecutar el pipeline de procesamiento de datos. 
