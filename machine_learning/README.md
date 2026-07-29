Operaciones de preparación de los datos para aplicar modelos. (modelado.ipynb)

1.- Limpieza.
1.1-Normalización de minúsculas:
Se convierte todo el texto en minúsculas para evitar que los conceptos principales se    traten como términos diferentes. Se aplica la función limpiar.

1.2- String a la columna ‘Texto limpio’.
Se convierte la columna donde se tiene limpio el texto a string para poder utilizarlo y poder aplicar el primer modelo.

2.-Vectorizar con modelo IT-IDF.
Para evitar las palabras o letras que son conocidas como palabras vacías, que no aportan un significado relevante al tema principal de un texto, se realizó una lista con los probables artículos , preposiciones, conjunciones etc. para poder evitarlas en el modelo.

3.- Regresión Logística.
Al obtener los resultados de la matriz, que en este caso referimos como “x_tfidf”, (X) como variables independientes, para (y) voy a utilizar la columna “categoria_l1” la cual nos indica a qué categoría pertenece cada texto.
Para poder aplicar la regresión, los datos se dividen en un 80% para entrenar al modelo y con el 20% haremos las pruebas.
