# Diccionario de datos — DataSetTechmind **V5**

**Proyecto:** TechMind AI · G9-LATAM-Team-46 (Hackathon ONE G9)  
**Versión del corpus:** **V5** — corte de raíz (V4.5 limpio + top-up técnico)  
**Paquete:** `entregas/DataSetTechmindV5_20260804/`  
**Generado (UTC):** 2026-08-04  

> Esta ficha describe **solo** el corpus de entrega **DataSetTechmind V5** (1061 / 955).  
> **No** describe el histórico `dataset_general_v5` (530) de julio 2026 (`BancoDatos_V5_*`).  
> Ver también `docs/DIFERENCIAS_DATASETS_V5.md`.

---

## 1. Resumen

| Métrica | Valor |
|---------|------:|
| Filas general / full | **1061** |
| Filas entrenamiento | **955** |
| Clases L1 | **7** |
| Orígenes (`titulo_origen`) | **~105** |
| Ratio max/min (full) | **≈ 1.05** |
| Ratio max/min (train) | **≈ 1.56** |
| PDFs blacklist residuales | **0** |
| Filas con `.op` / criterios operativos | **0** |

**Qué aporta esta versión**

1. Eliminación de basura de origen V1 (TOC, SHORT, PDFs fuera de dominio).  
2. Eliminación del molde residual `.op` del lote de balanceo.  
3. Re-balanceo realista (~150/L1) con top-up técnico estilo `dataset_general_base`, **sin densify**.  
4. Arquitectura “real” de software (patrones, resiliencia, APIs), no Agile/PESTEL.

**Fórmula**

```text
DataSetTechmindV5 = V4.5.FROZEN − 281 exclusiones + 152 top-up
```

---

## 2. Artefactos del paquete

| Artefacto | Ruta en el paquete | Rol |
|-----------|-------------------|-----|
| Dataset general / full | `data/DataSetTechmindV5.csv` | Corpus completo de la etapa |
| Dataset entrenamiento | `data/DataSetTechmindV5_entrenamiento.csv` | Subconjunto para modelado |
| Base post-filtro | `data/DataSetTechmindV5.base909.csv` | Trazabilidad (sin top-up) |
| Lote top-up | `data/lote_topup_v5.csv` | Solo las +152 filas nuevas |
| Lista de exclusión | `data/v5_exclusion_list.csv` | 281 ids eliminados + motivo |
| Datasheet | `data/DataSetTechmindV5.DATASHEET.md` | Métricas y gates |
| Árbol completo | `data/DataSetTechmindV5.ARBOL.md` | Taxonomía de cobertura |
| Diferencias de naming | `docs/DIFERENCIAS_DATASETS_V5.md` | General vs TechMind vs train |

---

## 3. Schema `DocumentoFragmento` (8 columnas)

General y entrenamiento comparten **exactamente** el mismo esquema.

| Columna | Tipo | Definición técnica y propósito |
| --- | --- | --- |
| `id_fragmento` | *String* | PK determinista (categoría + origen + prefijo de hash + página). |
| `titulo_origen` | *String* | Linaje: nombre de PDF o etiqueta de lote Fundamental / Topup. |
| `categoria_l1` | *String* | **Target** del clasificador (variable dependiente). 7 valores fijos. |
| `pagina` | *Integer* | Página o índice de sección del origen. |
| `texto_crudo` | *String* | **Feature** de texto a vectorizar (TF-IDF / embeddings). |
| `longitud_caracteres` | *Integer* | Densidad; base del filtro full → train. |
| `fecha_extraccion` | *Datetime* | ISO 8601 UTC; trazabilidad de ingesta/reescritura/top-up. |
| `hash_texto` | *String* | SHA-256 de `texto_crudo` (integridad y deduplicación). |

### Relación general → entrenamiento

```text
DataSetTechmindV5.csv                 (1061 filas)   ← “dataset general” de la entrega
        │
        │  filtro: longitud_caracteres >= max(percentil_10, 80)
        │  percentil_10 ≈ 1250 caracteres sobre el full
        │  → se excluyen 106 filas más cortas
        ▼
DataSetTechmindV5_entrenamiento.csv   (955 filas)
```

- Todo hash del train está en el general.  
- No hay filas nuevas en train.  
- El train **no** se rebalancea a 150×7 (el umbral de longitud altera la distribución).

---

## 4. Valores de `categoria_l1`

| Valor | Significado |
|-------|-------------|
| `Arquitectura` | Diseño de sistemas, patrones, resiliencia, APIs, observabilidad |
| `Bases_de_Datos` | SQL, transacciones, índices, distribución, NoSQL/LSM |
| `Hardware` | CPU, memoria, almacenamiento, fundamentos de hardware |
| `Inteligencia_Artificial` | Datos, texto/RAG, FMs, prompts, visualización de datos |
| `Lenguajes_Programacion` | Java, Python, UI (Tkinter), concurrencia |
| `Redes_y_Comunicaciones` | Redes básicas, TCP, QUIC/gRPC |
| `Sistemas_Operativos` | Planificación, memoria, I/O, contenedores, sync |

---

## 5. Distribución L1 — general (full)

| `categoria_l1` | Filas |
|---|---:|
| `Hardware` | 157 |
| `Inteligencia_Artificial` | 153 |
| `Redes_y_Comunicaciones` | 151 |
| `Sistemas_Operativos` | 150 |
| `Lenguajes_Programacion` | 150 |
| `Arquitectura` | 150 |
| `Bases_de_Datos` | 150 |
| **TOTAL** | **1061** |

## 6. Distribución L1 — entrenamiento

| `categoria_l1` | Filas |
|---|---:|
| `Arquitectura` | 150 |
| `Redes_y_Comunicaciones` | 146 |
| `Bases_de_Datos` | 146 |
| `Sistemas_Operativos` | 145 |
| `Inteligencia_Artificial` | 141 |
| `Hardware` | 131 |
| `Lenguajes_Programacion` | 96 |
| **TOTAL** | **955** |

> Lenguajes baja en train porque parte del lote nativo/fundacional queda bajo el umbral de longitud del p10.

---

## 7. Construcción y calidad

### Pipeline

1. Freeze de `DataSetTechmindV4.5` (estilo base ya reescrito).  
2. Exclusión determinista (blacklist PDF + OP_PAGE + flags OCR).  
3. Top-up con `PROMPT_REESCRITURA_ESTILO_BASE` + few-shot L1.  
4. Merge + gates.  
5. Derivación de train por longitud.

### Gates de aceptación (full)

| Gate | Resultado |
|------|-----------|
| Blacklist PDF (Agile / Estrategia / Ciberseg Cisco) | 0 filas |
| `.op` / “criterios operativos” | 0 filas |
| SHORT &lt; 500 | 0 filas |
| Hashes únicos | 1061/1061 |
| Ratio max/min L1 | ≤ 1.20 (1.05) |

### Motivos de exclusión (281 filas, no están en V5)

| Motivo | n (primario) |
|--------|-------------:|
| BLACKLIST_PDF | 116 |
| OP_PAGE | 112 |
| FLAG:SHORT | 35 |
| FLAG:TOC | 16 |
| FLAG:CMD_LIST | 2 |

Detalle: `data/v5_exclusion_list.csv`.

---

## 8. Uso recomendado

| Tarea | Archivo |
|-------|---------|
| Entrenar TF-IDF + LogisticRegression | `DataSetTechmindV5_entrenamiento.csv` |
| EDA / cobertura / datasheet de producto | `DataSetTechmindV5.csv` |
| Auditar limpieza | `v5_exclusion_list.csv` + base909 |
| Auditar solo top-up | `lote_topup_v5.csv` |

**Sugerencia ML:** `class_weight='balanced'` en el clasificador (el train no está perfectamente plano).

---

## 9. Naming y confusiones a evitar

| Nombre confuso | Realidad |
|----------------|----------|
| `dataset_general_v5` (530) en `working/` o `BancoDatos_V5_*` | Histórico **otro** linaje |
| `DataSetTechmindV5` (1061) | **Canónico** de esta entrega |
| `dataset_general_base` (343) | Estilo de prosa nativa; **no** es V5 |
| “V5 = solo rama IA” | Eso era la narrativa de julio; **esta** V5 es corte de raíz multi-L1 |

En este paquete, **general = `DataSetTechmindV5.csv`**.

---

## 10. Referencias del paquete

- Árbol: `data/DataSetTechmindV5.ARBOL.md`  
- Datasheet: `data/DataSetTechmindV5.DATASHEET.md`  
- Diferencias de roles: `docs/DIFERENCIAS_DATASETS_V5.md`  
- README del paquete: `README.md`  
