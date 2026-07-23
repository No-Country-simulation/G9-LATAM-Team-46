# Datasheet / Ficha Técnica del Dataset: `DataSetTechmindV1.csv`

> Misma carpeta que el CSV · paquete listo para envío (local)

## 1. Identificación y Metadatos

| Campo | Valor |
| --- | --- |
| **Identificador Único** | `DataSetTechmindV1.csv` |
| **Versión** | TechmindV1.0 |
| **Fecha de Creación** | 2026-07-23 |
| **Autor(es) / Equipo** | G9-LATAM-Team-46 · TechMind AI |
| **Tipo de Dataset** | Mixto (PDF nativo + sintético + OCR imagen) |
| **Estado del Artefacto** | Processed / Corpus unificado de corrección |
| **Licencia / Privacidad** | Uso interno · PDF no versionados públicamente |
| **Ruta de trabajo** | `dataset/correcciones/augmented_correciones/trabajo_nuevo/datasets/DataSetTechmindV1.csv` |
| **Paquete de entrega** | `entregas/DataSetTechmindV1_20260723/` |
| **Schema** | DocumentoFragmento (8 columnas) |
| **Hash SHA-256** | `499fa5a1e122bf3a5ffdca83c0a5f6911a91ae9faae349d02c48d97ed3fc6cd1` |
| **Árbol asociado** | `DataSetTechmindV1.ARBOL.md` (misma carpeta) |

## 2. Motivación y casos de uso

* **Propósito:** Dataset unificado de la línea de corrección TechMind para clasificador L1 y experimentos RAG.
* **Previstos:** entrenamiento TF-IDF/LogReg; indexación de fragmentos; demostración de linaje multi-fuente.
* **Fuera de alcance:** test set con filas `ocr_*` o `augment_*` sin muestreo; generación de texto sin curación.

## 3. Volumetría

| Métrica | Valor |
| --- | ---: |
| Total filas | **668** |
| Columnas | 8 |
| PDF nativo tipográfico | 343 |
| Sintéticos balanceo | 38 |
| OCR imagen | 287 |
| Duplicados hash | 0 |
| Nulos | 0% |

### Diccionario (8 cols)

| Columna | Tipo | Descripción |
| --- | --- | --- |
| id_fragmento | String | PK |
| titulo_origen | String | PDF o lote augment_* |
| categoria_l1 | String | Target |
| pagina | Integer | Página; 0 en sintéticos |
| texto_crudo | String | Feature |
| longitud_caracteres | Integer | Densidad |
| fecha_extraccion | ISO-8601 | Timestamp |
| hash_texto | String | SHA-256 del texto |

## 4. Distribución L1

| categoria_l1 | n | % |
| --- | ---: | ---: |
| `Lenguajes_Programacion` | 138 | 20.7% |
| `Inteligencia_Artificial` | 129 | 19.3% |
| `Arquitectura` | 128 | 19.2% |
| `Redes_y_Comunicaciones` | 124 | 18.6% |
| `Hardware` | 63 | 9.4% |
| `Bases_de_Datos` | 49 | 7.3% |
| `Sistemas_Operativos` | 37 | 5.5% |

**Ratio max/min:** 3.73

## 5. Longitud

| Estadístico | Valor |
| --- | ---: |
| Media | 1792.8 |
| Std | 849.1 |
| Min | 147 |
| Mediana | 1717.5 |
| Max | 6396 |

## 6. Linaje

```text
ingesta tipográfica (343)
  + balanceo syn_v2 (38) → dataset_general_v2 (381)
  + OCR ContieneImagenes v1.1 (287)
  = DataSetTechmindV1 (668)
```

## 7. Limitaciones

- OCR puede tener ruido residual.
- No usar sintéticos/OCR como único test set.
- class_weight=balanced y L2 en TF-IDF recomendados.

## 8. Changelog

| Versión | Fecha | Cambio |
| --- | --- | --- |
| TechmindV1.0 | 2026-07-23 | Fusión v2 corregido + OCR completo + árbol y paquete de entrega |

*TechMind · ficha de envío*
