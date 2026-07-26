Diagnóstico inicial del data set

Tiene un tamaño de 36714 filas con 6 columnas, lo cual nos ayuda para entrenar nuestro modelo y los resultados sean favorables para el proyecto.

Viendo la informacion del dataset corroboramos que las columnas “título”, “texto”, “categoría”,”fuente” y “tags” no tienen valores nulos lo cual nos permite trabajar de forma óptima con estas columnas, a diferencia de la columna calidad que tiene 25574 registros correctos y 11140 filas que tienen un valor null.

Sin embargo, la columna numérica de “calidad” presenta 11,140 valores faltantes (30.35%), para no desechar todos los registros de texto que carecen de calificación, se optó por no eliminar estos registros del dataset general ya que no aportan algún valor al análisis que requerimos, dentro de esta columna pero si los registros de las que depende las demás columnas.

Se analizó la frecuencia de las variables categóricas y se observa que las categorías y fuentes se repiten de manera natural agrupando el contenido del dataset, esto indica que el dataset cuenta con una representación estructurada por temas.

Aplicamos el conteo por categoría para analizar la distribución que contiene el dataset, en las primeras 6 categorías tiene 5000 registros lo que significa que el dataset es altamente balanceado en sus categorías principales.
Las dos últimas categorías caen en cantidad que se refleja en base de datos y seguridad, lo cual nos crea un ligero desequilibrio o caída en estas dos áreas específicas, no es un error crítico pero se debe mencionar para el análisis.

Al analizar la distribución de la variable categoría se observa que el dataset cuenta con 8 categorías en total 6 de ellas completamente balanceadas con 5000 registros, no obstante las categorías de base de datos y seguridad presentan una representación ligeramente menor con 4140 y 2574 respectivamente lo cual constituye un sesgo menor en la distribución que deberá considerarse al momento de evaluar el rendimiento del modelo por clase 

MEJORAS
Respecto al análisis de longitud de documentos en palabras, se observa una diferencia entre los títulos y los textos principales. Los títulos mantienen un comportamiento igual con un promedio de 9.6 palabras. Por su parte, los textos principales presentan una media de 351 palabras, pero con una alta desviación estándar (510.8 palabras) y un rango que va desde las 15 hasta las 3,740 palabras. Con esto se puede concluir que la mayoría de los registros se concentran en tamaños medianos.

Tratamiento de la variable calidad: Para futuros modelos predictivos que dependan de esta métrica, se recomienda aislar los 25,574 registros calificados o aplicar una estrategia de imputación basada en segmentación por fuente (ya que los nulos se concentran en Medium). Para tareas generales de NLP, se aconseja conservar el dataset íntegro de 36,714 filas ignorando dicha columna.
Mitigación del desequilibrio menor: Aunque el dataset está mayormente balanceado, se sugiere aplicar técnicas de aumento de datos (data augmentation) o ponderación de clases (class weights) para las categorías de Bases de Datos y Seguridad al momento de entrenar clasificadores.
Estandarización de textos largos: Evaluar un filtrado o truncamiento de los documentos extremadamente largos (valores atípicos superiores al percentil 95) para optimizar el rendimiento computacional durante la vectorización de texto en fases de Machine Learning.
