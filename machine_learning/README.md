# TechMind - Machine Learning

Sistema de Procesamiento de Lenguaje Natural (PLN) y Machine Learning diseñado para clasificar automáticamente artículos y preguntas técnicas en sus respectivas áreas de especialización (*Backend, Bases de Datos, Ciencia de Datos, DevOps / Cloud, Frontend, Mobile, Programación General y Seguridad*).

---

##  Características del Proyecto
- **Limpieza avanzada de texto:** Expresiones regulares personalizadas para normalización y conservación de términos técnicos cortos (`go`, `js`, `ai`, `ml`, etc.).
- **Ingeniería de Características:** Extracción de n-gramas (unigramas y bigramas) y ponderación mediante **TF-IDF**.
- **Procesamiento explícito (Sin Pipeline):** Aplicación manual y controlada de **TF-IDF** separando los conjuntos de entrenamiento y prueba para evitar fugas de datos (*data leakage*).
- **Modelado comparativo:** Implementación y evaluación de **Regresión Logística** (con manejo de clases desbalanceadas mediante `class_weight='balanced'`) y **Naive Bayes**.
- **Optimización automática:** Búsqueda de hiperparámetros mediante **GridSearchCV** y validación cruzada.
- **Evaluación exhaustiva:** Cálculo de métricas (*Accuracy, Precision, Recall, F1-Score*) y generación de **Matrices de Confusión**.



##  Resultados y Rendimiento
* **Exactitud Global (Accuracy):** ~75.35% en el modelo base de Regresión Logística.
* **Estabilidad:** El modelo optimizado mediante `GridSearchCV` ofrece un rendimiento muy robusto y consistente.
* **Clase mejor desempeñada:** *Mobile* (Precisión de 0.86), gracias a la fuerte diferenciación de su vocabulario técnico.



##  Requisitos e Instalación

Asegúrate de tener Python instalado junto con las siguientes librerías de Machine Learning y Ciencia de Datos:

```bash
pip install pandas numpy scikit-learn matplotlib
