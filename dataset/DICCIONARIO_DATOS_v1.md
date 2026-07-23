# Diccionario de datos — TechMind **V1**

**Proyecto:** TechMind AI · G9-LATAM-Team-46 (Hackathon ONE G9)  
**Versión del corpus:** **V1** — V1 — original (PDFs)  
**Etapa:** original / Fase 1 EDA  
**Generado (UTC):** 2026-07-23

> Documento de la **familia** `dataset/DICCIONARIO_DATOS.md`.  
> Esta ficha describe **solo** los artefactos de la versión **V1**.

---

## 1. Resumen

| Métrica | Valor |
|---------|------:|
| Filas general | **283** |
| Filas train | **254** |
| Clases L1 | **7** |
| Orígenes (`titulo_origen`) | **11** |
| Ratio max/min train | **6.333** |

**Qué aporta esta versión:** Extracción de PDFs técnicos del equipo. Sin sintéticos.

---

## 2. Ubicación de artefactos V1

| Artefacto | Ruta canónica (repo local) | Rol |
|-----------|---------------------------|-----|
| Dataset general V1 | `data/original/dataset_general_v1.csv` | Corpus completo de la etapa |
| Dataset entrenamiento V1 | `data/original/dataset_entrenamiento_v1.csv` | Subconjunto para modelado |
| Árbol de etapa | `data/original/arbol_conocimiento_techmind.md` | Taxonomía / propuesta de la etapa |
| Copia en entrega | `entregas/Fase1_EDA_paquete_*/docs/arbol_conocimiento_techmind.md` | Paquete compartible (fuera de `/data/`) |
| Espejo / entrega | `data/raw/csv/dataset_general_v1.csv` | Copia o patrón relacionado |
| Espejo / entrega | `data/processed/dataset_entrenamiento_v1.csv` | Copia o patrón relacionado |
| Espejo / entrega | `entregas/Fase1_EDA_paquete_*/data/*_v1.csv` | Copia o patrón relacionado |
| Espejo / entrega | `entregas/BancoDatos_V5_*/ (no aplica; ver diccionario v5)` | Copia o patrón relacionado |

> **Git:** la carpeta raíz `/data/` está en `.gitignore` (PDF privados y CSV de trabajo).  
> Para el repositorio remoto se usan copias en `entregas/**` y este diccionario en `dataset/`.

---

## 3. Schema `DocumentoFragmento` (8 columnas)

General y train de **V1** comparten **exactamente** el mismo esquema.

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
dataset_general_v1   (283 filas)
        │
        │  filtro por longitud_caracteres
        │  (pipeline de la etapa; train ⊆ general)
        ▼
dataset_entrenamiento_v1   (254 filas)
```

---

## 4. Distribución `categoria_l1` — general V1

| `categoria_l1` | Filas |
|---|---:|
| `Lenguajes_Programacion` | 116 |
| `Hardware` | 47 |
| `Bases_de_Datos` | 33 |
| `Inteligencia_Artificial` | 26 |
| `Redes_y_Comunicaciones` | 25 |
| `Arquitectura` | 21 |
| `Sistemas_Operativos` | 15 |
| **TOTAL** | **283** |

## 5. Distribución `categoria_l1` — train V1

| `categoria_l1` | Filas |
|---|---:|
| `Lenguajes_Programacion` | 95 |
| `Hardware` | 44 |
| `Bases_de_Datos` | 33 |
| `Redes_y_Comunicaciones` | 25 |
| `Inteligencia_Artificial` | 21 |
| `Arquitectura` | 21 |
| `Sistemas_Operativos` | 15 |
| **TOTAL** | **254** |

---

## 6. Orígenes (`titulo_origen`) — general V1

| `titulo_origen` | Filas |
|---|---:|
| `Tkinter_Fundamental.pdf` | 56 |
| `Módulo 1 y 2 Fundamentos de Hardware.pdf` | 47 |
| `Java_Fundamental.pdf` | 44 |
| `SQL_Fundamental.pdf` | 33 |
| `Fundamentos de Redes y TCP.pdf` | 25 |
| `Manual de Estrategia y Control.pdf` | 21 |
| `IntroducciónPython_AnálisisDatos.pdf` | 16 |
| `Guía Técnica de Oracle Virtual Machine.pdf` | 15 |
| `Optimizando FMs.pdf` | 13 |
| `VisualizaciónInterpretacióndeDatos.pdf` | 9 |
| `Limpieza y Optimización de Datos en Pandas.pdf` | 4 |

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

*G9-LATAM-Team-46 · TechMind · Diccionario V1*
