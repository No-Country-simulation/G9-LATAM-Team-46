# Diccionario de datos — TechMind **V5**

**Proyecto:** TechMind AI · G9-LATAM-Team-46 (Hackathon ONE G9)  
**Versión del corpus:** **V5** — V5 — rama IA de texto / ML services  
**Etapa:** v5 rama (corpus de trabajo actual)  
**Generado (UTC):** 2026-07-23

> Documento de la **familia** `dataset/DICCIONARIO_DATOS.md`.  
> Esta ficha describe **solo** los artefactos de la versión **V5**.

---

## 1. Resumen

| Métrica | Valor |
|---------|------:|
| Filas general | **530** |
| Filas train | **477** |
| Clases L1 | **7** |
| Orígenes (`titulo_origen`) | **15** |
| Ratio max/min train | **2.872** |

**Qué aporta esta versión:** IA texto, métricas, pipelines de fragmentos, RAG, API ML (+46). L1: Inteligencia_Artificial (+35), Arquitectura (+11).

**Delta respecto a la versión anterior:** v4 → v5: +46 (`augment_rama_ia_texto_ml_v5`, `synth_ia_*`)

---

## 2. Ubicación de artefactos V5

| Artefacto | Ruta canónica (repo local) | Rol |
|-----------|---------------------------|-----|
| Dataset general V5 | `data/augmented/working/dataset_general_v5.csv` | Corpus completo de la etapa |
| Dataset entrenamiento V5 | `data/augmented/working/dataset_entrenamiento_v5.csv` | Subconjunto para modelado |
| Árbol de etapa | `data/augmented/arbol_v5_rama.md` | Taxonomía / propuesta de la etapa |
| Árbol completo fusionado | `data/augmented/arbol_conocimiento_v5_completo.md` | Vista unificada hasta V5 |
| Copia en entrega | `entregas/BancoDatos_V5_*/docs/arbol_conocimiento_v5_completo.md` | Paquete compartible (fuera de `/data/`) |
| Espejo / entrega | `data/augmented/working/dataset_*_v5.csv` | Copia o patrón relacionado |
| Espejo / entrega | `entregas/BancoDatos_V5_*/data/*_v5.csv` | Copia o patrón relacionado |

> **Git:** la carpeta raíz `/data/` está en `.gitignore` (PDF privados y CSV de trabajo).  
> Para el repositorio remoto se usan copias en `entregas/**` y este diccionario en `dataset/`.

---

## 3. Schema `DocumentoFragmento` (8 columnas)

General y train de **V5** comparten **exactamente** el mismo esquema.

| Columna | Tipo | Definición técnica y propósito |
| --- | --- | --- |
| `id_fragmento` | *String* | PK determinista (categoría + origen + hash / prefijo sintético). |
| `titulo_origen` | *String* | Linaje: nombre de PDF o etiqueta de lote (`augment_*`). |
| `categoria_l1` | *String* | **Target** del clasificador (variable dependiente). |
| `pagina` | *Integer* | Página del PDF; en sintéticos suele ser `0`. |
| `texto_crudo` | *String* | **Feature** de texto a vectorizar (TF-IDF / embeddings). |
| `longitud_caracteres` | *Integer* | Densidad; base del filtro general → train. |
| `fecha_extraccion` | *Datetime* | ISO 8601; control de versión temporal de la ingesta. |
| `hash_texto` | *String* | SHA-256 de `texto_crudo` (integridad y deduplicación). |

Columnas verificadas en disco: `id_fragmento, titulo_origen, categoria_l1, pagina, texto_crudo, longitud_caracteres, fecha_extraccion, hash_texto`.

### Relación general → entrenamiento

```text
dataset_general_v5   (530 filas)
        │
        │  filtro por longitud_caracteres
        │  (pipeline de la etapa; train ⊆ general)
        ▼
dataset_entrenamiento_v5   (477 filas)
```

---

## 4. Distribución `categoria_l1` — general V5

| `categoria_l1` | Filas |
|---|---:|
| `Lenguajes_Programacion` | 116 |
| `Hardware` | 99 |
| `Arquitectura` | 97 |
| `Bases_de_Datos` | 68 |
| `Inteligencia_Artificial` | 61 |
| `Sistemas_Operativos` | 50 |
| `Redes_y_Comunicaciones` | 39 |
| **TOTAL** | **530** |

## 5. Distribución `categoria_l1` — train V5

| `categoria_l1` | Filas |
|---|---:|
| `Lenguajes_Programacion` | 112 |
| `Hardware` | 98 |
| `Arquitectura` | 74 |
| `Inteligencia_Artificial` | 60 |
| `Sistemas_Operativos` | 48 |
| `Bases_de_Datos` | 46 |
| `Redes_y_Comunicaciones` | 39 |
| **TOTAL** | **477** |

---

## 6. Orígenes (`titulo_origen`) — general V5

| `titulo_origen` | Filas |
|---|---:|
| `augment_balanceo_v2` | 105 |
| `Tkinter_Fundamental.pdf` | 56 |
| `augment_rama_hardware_arquitectura_v3` | 52 |
| `Módulo 1 y 2 Fundamentos de Hardware.pdf` | 47 |
| `augment_rama_ia_texto_ml_v5` | 46 |
| `Java_Fundamental.pdf` | 44 |
| `augment_rama_ciberseguridad_v4` | 44 |
| `SQL_Fundamental.pdf` | 33 |
| `Fundamentos de Redes y TCP.pdf` | 25 |
| `Manual de Estrategia y Control.pdf` | 21 |
| `IntroducciónPython_AnálisisDatos.pdf` | 16 |
| `Guía Técnica de Oracle Virtual Machine.pdf` | 15 |
| `Optimizando FMs.pdf` | 13 |
| `VisualizaciónInterpretacióndeDatos.pdf` | 9 |
| `Limpieza y Optimización de Datos en Pandas.pdf` | 4 |

### Lote nuevo de esta etapa (`augment_rama_ia_texto_ml_v5`)

Filas añadidas en el lote: **46**

| `categoria_l1` | Filas |
|---|---:|
| `Inteligencia_Artificial` | 35 |
| `Arquitectura` | 11 |
| **TOTAL** | **46** |

---

## 7. Notas de diseño

1. **Un fragmento, una `categoria_l1` principal.**
2. Las filas sintéticas usan `titulo_origen` de lote y prefijos `synth_*` en `id_fragmento`.
3. No se versionan PDF en Git.
4. El clasificador MVP predice sobre el conjunto cerrado de L1 presentes en el CSV de la versión elegida.

---

## 8. Índice de diccionarios por versión

| Versión | Archivo |
|--------:|---------|
| Índice | [`DICCIONARIO_DATOS.md`](./DICCIONARIO_DATOS.md) |
| V1 | [`DICCIONARIO_DATOS_v1.md`](./DICCIONARIO_DATOS_v1.md) |
| V2 | [`DICCIONARIO_DATOS_v2.md`](./DICCIONARIO_DATOS_v2.md) |
| V3 | [`DICCIONARIO_DATOS_v3.md`](./DICCIONARIO_DATOS_v3.md) |
| V4 | [`DICCIONARIO_DATOS_v4.md`](./DICCIONARIO_DATOS_v4.md) |
| V5 | [`DICCIONARIO_DATOS_v5.md`](./DICCIONARIO_DATOS_v5.md) |

*G9-LATAM-Team-46 · TechMind · Diccionario V5*
