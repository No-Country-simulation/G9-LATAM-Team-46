# Datasheet — DataSetTechmind **V5**

**Fecha:** 2026-08-04  
**Cupo:** opción A (~150/L1)  
**Corpus:** `datasets/DataSetTechmindV5.csv`  
**Train:** `datasets/DataSetTechmindV5_entrenamiento.csv`  

---

## 1. Resumen ejecutivo

| Métrica | Valor |
|---------|------:|
| Total filas | **1061** |
| Base filtrada (V4.5 − exclusiones) | 909 |
| Top-up técnico limpio | 152 |
| Train (≥ p10 longitud) | 955 |
| Ratio max/min L1 | **1.047** (≤ 1.20) |
| PDFs blacklist | **0** |
| SHORT &lt; 500 | **0** |
| Hashes únicos | 1061 |

**Fórmula:**  
`V5 = V4.5.FROZEN − 281 exclusiones de raíz + 152 top-up estilo dataset_general_base`

---

## 2. Balance L1 (opción A)

| categoria_l1 | n | vs 150 |
|--------------|--:|-------:|
| Hardware | 157 | +7 |
| Inteligencia_Artificial | 153 | +3 |
| Redes_y_Comunicaciones | 151 | +1 |
| Sistemas_Operativos | 150 | 0 |
| Lenguajes_Programacion | 150 | 0 |
| Arquitectura | 150 | 0 |
| Bases_de_Datos | 150 | 0 |

Surplus en HW/IA/Redes se conserva (técnico bueno). No se forzó 170×7.

---

## 3. Pipeline aplicado

1. **Freeze** V4.5 → `DataSetTechmindV4.5.FROZEN_FOR_V5.csv`  
2. **Exclusión** 281 ids (`v5_exclusion_*.txt/csv`): blacklist PDFs + OP_PAGE + flags OCR  
3. **Base** 909 → `DataSetTechmindV5.base909.csv`  
4. **Top-up** 152 jobs (Arch 102, SO 29, Leng 12, BD 9)  
   - Prompt: `PROMPT_REESCRITURA_ESTILO_BASE.md` + few-shot L1  
   - Jobs: `inbox/v5/topup_jobs/`  
5. **Ensamble + merge** → V5.csv + gates  

---

## 4. Gates QA V5

| Gate | Umbral | Resultado |
|------|--------|-----------|
| Banlist `.op` / criterios operativos | 0 % | **PASS** |
| PDFs blacklist | 0 filas | **PASS** |
| SHORT &lt; 500 | 0 en corpus | **PASS** |
| Hashes únicos | 100 % | **PASS** |
| Ratio max/min L1 | ≤ 1.20 | **PASS** (1.047) |
| Longitud top-up | ~1400–2800 | med **2205** |

---