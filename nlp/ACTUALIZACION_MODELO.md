# Actualización al modelo entregado por el equipo de modelado

Fecha: 19 de agosto de 2026

## Resumen

El `.joblib` que traía el proyecto **no era el mismo** que el entregado por el
equipo de modelado. Son dos modelos distintos, entrenados sobre corpus
limpiados de forma diferente:

| | Modelo anterior (en el repo) | Modelo entregado (actual) |
|---|---|---|
| MD5 | `98376222…` | `bcca3157…` |
| Términos con dígitos | 0 | **987** (`s3`, `ec2`, `ubuntu 24`) |
| Términos de 2 letras | 0 | **497** (`js`, `ci`, `cd`, `go`) |
| ¿Contiene `the`? | No | **Sí** |

Ambos comparten arquitectura (TF-IDF 60.000 features, ngram (1,2), min_df=5,
LogisticRegression C=4.0) y las 8 categorías, pero **esperan entradas
distintas**.

## Por qué había que cambiar la limpieza

`src/cleaning.py` replicaba el preprocesamiento del modelo anterior: pasaba a
minúsculas, eliminaba dígitos, eliminaba todo carácter no alfanumérico y
descartaba palabras de 2 letras o menos. Ese criterio es correcto para el
modelo viejo y **destructivo para el nuevo**.

Medición sobre el texto
`"Migrar de Vue 2 a Vue 3 y desplegar en AWS S3 y EC2 con CI/CD, usando C# y C++ en .NET 8"`:

| Limpieza | Features reconocidas por el modelo nuevo |
|---|---|
| Anterior | 6 — `aws, con, desplegar, net, usando, vue` |
| Actual | **14** — añade `s3`, `ec2`, `ci`, `cd`, `ci cd`, `aws s3`, `de`, `en` |

Se perdía la señal de DevOps / Cloud completa. El fallo era silencioso: el
servicio respondía igual, solo que con menos evidencia.

## Cambios aplicados

1. **`models/modelo_techmind_v2.joblib`** — reemplazado por el entregado.

2. **`src/cleaning.py`** — reescrito como réplica de `limpiar_texto()` +
   `corregir_ortografia()` del notebook `limpieza_y_eda_techmind_v2_final`.
   Ya no baja a minúsculas (lo hace el vectorizador), conserva dígitos,
   palabras cortas y los caracteres técnicos `+ # . _ - /`.
   Se añade `preparar_entrada_modelo(titulo, texto)`, que limpia cada campo
   por separado y luego los une — igual que el entrenamiento.

3. **`src/classifier.py`** — pasa título y texto por separado al limpiador.
   Antes concatenaba y luego limpiaba, que no es equivalente si el título
   termina en una URL o un símbolo.

4. **`src/keywords.py`** — se añade filtro de términos vacíos. El modelo
   nuevo se entrenó **sin quitar stopwords**, así que su vocabulario las
   contiene y sin filtro la respuesta salía así:

   ```json
   ["spring boot", "java spring", "la creación", "los conceptos", "creación de"]
   ```

   El inglés se cubre con `ENGLISH_STOP_WORDS` de sklearn; el español y el
   ruido de foros van en listas propias. Se exige que **todos** los
   componentes de un n-grama aporten significado: con un criterio laxo
   sobrevive "la creación" porque "creación" pasa el filtro.
   `_FACTOR_CANDIDATOS` sube de 4 a 10 porque ahora se descartan más
   candidatos.

5. **`src/config.py`** — se elimina `LONGITUD_MINIMA_PALABRA` (ya no aplica).

6. **`tests/test_cleaning.py`** — reescrito. Cada aserción custodia una
   característica verificada en el vocabulario del `.joblib`: conserva
   dígitos, conserva palabras de 2 letras, conserva stopwords, conserva
   caracteres técnicos, no baja a minúsculas.

7. **`tests/test_keywords.py`** — el corpus de la prueba de bigramas se
   rehízo para que el bigrama gane por IDF y no por casualidad.

## Resultado

```
Backend            0.995  ['spring boot', 'java spring', 'apis', 'rest']
DevOps / Cloud     0.972  ['desplegar', 'aws s3', 'imagen', 'github actions']
Frontend           0.936  ['centrar', 'div', 'verticalmente', 'flexbox']
```

`aws s3` aparece: es la prueba directa de que el arreglo de dígitos funciona.

## Sobre los notebooks

Los dos notebooks subidos son idénticos a los anteriores (mismo tamaño en
bytes). El único archivo realmente nuevo es el `.joblib`.

Confirmado además dónde se usan stopwords en el entrenamiento: **en ninguna
parte**. Aparecen solo en el notebook de EDA (celdas 57-61), para el conteo de
frecuencias y para un `TfidfVectorizer` auxiliar de `max_features=5000` que
solo sirve para mostrar términos característicos por categoría y **nunca se
guardó**. El notebook de modelado (`ml_data_v2_final`, celdas 9 y 19) usa
`TfidfVectorizer(max_features=60000, min_df=5, ngram_range=(1,2))` sin
`stop_words` y sin lematización.

---

# Segunda tanda: port desde techmind_nlp

Cambios aplicados después de comparar ambos proyectos. Se conserva la
arquitectura de este proyecto (Protocol, inyección de dependencias,
jerarquía de excepciones) y se traen solo las mejoras medibles.

## 1. Caché del vocabulario — 43 ms → 1.8 ms

`ExtractorPalabrasClaveTfidf` llamaba a `get_feature_names_out()` en cada
request. Esa función reconstruye y ordena las 60.000 features cada vez:
medido, ~40 ms de los ~43 ms totales, frente a ~1 ms de `predict_proba`.
Como el vectorizador ya está ajustado y no cambia, ahora se calcula una sola
vez por instancia.

Además el vector disperso se recorre por `indices`/`data` (CSR) en lugar de
densificarlo con `toarray()`: se reservaban 60.000 posiciones para leer las
~25 con valor.

**El cuello de botella no estaba en el modelo, estaba en una función
auxiliar.** Es un buen ejemplo de por qué conviene medir antes de optimizar.

## 2. Ponderación por coeficiente de clase

Las palabras clave se ordenaban por TF-IDF puro, lo que sube términos raros
pero genéricos. Ahora:

```
relevancia = TF-IDF x (1 + max(0, coeficiente del término en la categoría))
```

Solo cuenta el aporte positivo: un coeficiente negativo significa que el
término apunta a OTRA categoría y no debe presentarse como palabra clave de
esta. El efecto es que las palabras clave **explican** la clasificación en
vez de solo describir el texto.

| Caso | Antes | Después |
|---|---|---|
| Kubernetes | `desplegar, aws s3, imagen, construir` | `GitHub Actions, ci cd, AWS S3, Kubernetes, Docker` |
| Spring Boot | `spring boot, java spring, apis, rest` | `Spring Boot, java spring, APIs, REST` |

El clasificador (`pipeline.named_steps["clf"]`) se inyecta en el constructor
del extractor; el parámetro `categoria` de `extraer()` es opcional, así que
el `Protocol` sigue cumpliéndose y cualquier implementación alternativa que
no lo use sigue siendo válida.

## 3. Prioridad a los n-gramas largos

Efecto secundario del punto 2: al ponderar por coeficiente, `spring` y `boot`
puntúan alto por separado y el filtro de redundancia los tomaba antes que
`spring boot`, devolviendo `['Spring', 'Boot']`. Ahora los candidatos
finalistas se reordenan por cantidad de palabras antes de la deduplicación.
El recorte por relevancia ya ocurrió, así que esto solo decide entre
finalistas.

## 4. Capitalización original

El vectorizador trabaja en minúsculas, así que sus features salen como
`spring boot`. Se recupera la grafía del texto de entrada para devolver
`Spring Boot`. Es cosmético, pero es lo que se proyecta en pantalla durante
la sustentación.

Esto solo es posible porque la limpieza corregida ya no baja a minúsculas.

## 5. Nuevo módulo `src/tokenization.py`

Expone `tokenizar()`, `eliminar_stopwords()` y `tokenizar_y_filtrar()`, que
son funciones pedidas explícitamente en el alcance del rol de NLP y que el
proyecto no tenía como tales.

Su docstring deja claro el alcance: **no se aplican antes del clasificador**
(rompería el contrato con el entrenamiento), sino en análisis y depuración.
Reutilizan `es_termino_util()` de `keywords.py` para que el criterio de
filtrado sea uno solo en todo el proyecto.

No se implementa lematización, y el módulo explica por qué: el corpus es
bilingüe, `WordNetLemmatizer` solo cubre inglés, y el IDF ya neutraliza los
términos vacíos (IDF de `the` = 1.07 contra 5.35 de `kubernetes`).

## 6. `tests/test_tokenization.py`

Diez pruebas nuevas del módulo anterior.

## Estado

72 pruebas verificadas en verde. Las de `test_inference.py` y
`test_classifier.py` usan fixtures de pytest (`tmp_path`, `monkeypatch`) que
requieren pytest real — **córrelas con `pytest tests/ -v`**.
