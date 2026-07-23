# Verificación: árbol completo V5 vs datasets v1–v5

**Resultado:** 84 PASS / 1 FAIL

Árbol: `C:/Team46/G9-LATAM-Team-46/data/augmented/arbol_conocimiento_v5_completo.md`

## Checklist

- ✅ total general v1 — real=283 esperado=283
- ✅ total train v1 — real=254 esperado=254
- ✅ total general v2 — real=388 esperado=388
- ✅ total train v2 — real=350 esperado=350
- ✅ total general v3 — real=440 esperado=440
- ✅ total train v3 — real=397 esperado=397
- ✅ total general v4 — real=484 esperado=484
- ✅ total train v4 — real=435 esperado=435
- ✅ total general v5 — real=530 esperado=530
- ✅ total train v5 — real=477 esperado=477
- ✅ schema general v1 — cols=['id_fragmento', 'titulo_origen', 'categoria_l1', 'pagina', 'texto_crudo', 'longitud_caracteres', 'fecha_extraccion', 'hash_texto']
- ✅ schema general v2 — cols=['id_fragmento', 'titulo_origen', 'categoria_l1', 'pagina', 'texto_crudo', 'longitud_caracteres', 'fecha_extraccion', 'hash_texto']
- ✅ schema general v3 — cols=['id_fragmento', 'titulo_origen', 'categoria_l1', 'pagina', 'texto_crudo', 'longitud_caracteres', 'fecha_extraccion', 'hash_texto']
- ✅ schema general v4 — cols=['id_fragmento', 'titulo_origen', 'categoria_l1', 'pagina', 'texto_crudo', 'longitud_caracteres', 'fecha_extraccion', 'hash_texto']
- ✅ schema general v5 — cols=['id_fragmento', 'titulo_origen', 'categoria_l1', 'pagina', 'texto_crudo', 'longitud_caracteres', 'fecha_extraccion', 'hash_texto']
- ✅ ids v1 subset de v2 — missing=0 new=105
- ✅ ids v2 subset de v3 — missing=0 new=52
- ✅ ids v3 subset de v4 — missing=0 new=44
- ✅ ids v4 subset de v5 — missing=0 new=46
- ✅ v2 delta SO +35 — 35
- ✅ v2 delta DB +35 — 35
- ✅ v2 delta Arch +35 — 35
- ✅ v2 no toca Hardware
- ✅ v2 no toca IA
- ✅ v2 no toca Redes
- ✅ v2 no toca Lenguajes
- ✅ v2 total +105
- ✅ v3 delta Hardware +52
- ✅ v3 solo mueve Hardware
- ✅ v3 total +52
- ✅ v4 delta Arch +30
- ✅ v4 delta Redes +14
- ✅ v4 no L1 Ciberseguridad
- ✅ v4 total +44
- ✅ v5 delta IA +35
- ✅ v5 delta Arch +11
- ✅ v5 IA final 61
- ✅ v5 Arch final 97
- ✅ v5 total +46
- ✅ v2 origen augment_balanceo_v2
- ✅ v3 origen hardware_v3
- ✅ v4 origen ciber_v4
- ✅ v5 origen ia_v5
- ✅ v3 ids synth_hw
- ✅ v4 ids synth_cyber
- ✅ v5 ids synth_ia
- ✅ v4 L1 Arch 30 — {'Redes_y_Comunicaciones': 14, 'Arquitectura': 30}
- ✅ v4 L1 Redes 14 — {'Redes_y_Comunicaciones': 14, 'Arquitectura': 30}
- ✅ v5 L1 IA 35 — {'Inteligencia_Artificial': 35, 'Arquitectura': 11}
- ✅ v5 L1 Arch 11 — {'Inteligencia_Artificial': 35, 'Arquitectura': 11}
- ✅ train v1 subset general — only_train=0
- ✅ train v2 subset general — only_train=0
- ✅ train v3 subset general — only_train=0
- ✅ train v4 subset general — only_train=0
- ✅ train v5 subset general — only_train=0
- ❌ train v5 = general filtrado len>=299 (P10=299) — pred=479 actual=477 symdiff=2
- ✅ tematica augment_rama_hardware_arquitectura_v3 — covered 10/10 hits={'Von Neumann': 1, 'RISC': 1, 'CISC': 1, 'NVMe': 8, 'PCIe': 7, 'ALU': 7, 'DMA': 5, 'caché': 18, 'pipeline': 9, 'SSD': 9}
- ✅ tematica augment_rama_ciberseguridad_v4 — covered 8/8 hits={'OWASP': 4, 'TLS': 8, 'CIA': 15, 'DevSecOps': 4, 'XSS': 2, 'PKI': 3, 'pentest': 4, 'SAST': 3}
- ✅ tematica augment_rama_ia_texto_ml_v5 — covered 10/10 hits={'TF-IDF': 9, 'F1': 7, 'RAG': 11, 'embedding': 4, 'chunk': 3, 'Logistic': 1, 'OpenAPI': 1, 'class_weight': 2, 'Precision': 2, 'Recall': 4}
- ✅ tematica augment_balanceo_v2 — covered 5/5 hits={'CFS': 18, 'Cassandra': 12, 'CAP': 17, 'microserv': 22, 'OCI': 36}
- ✅ arbol contiene 'Arquitectura de Computadores y Subsistemas'
- ✅ arbol contiene 'APLICADO v3'
- ✅ arbol contiene 'Ciberseguridad'
- ✅ arbol contiene 'APLICADO v4'
- ✅ arbol contiene 'Inteligencia Artificial y sistemas de texto'
- ✅ arbol contiene 'APLICADO v5'
- ✅ arbol contiene 'Von Neumann'
- ✅ arbol contiene 'OWASP'
- ✅ arbol contiene 'TF-IDF'
- ✅ arbol contiene 'Fundamentos de Hardware y Lógica Digital'
- ✅ arbol contiene 'Java'
- ✅ arbol contiene 'Tkinter'
- ✅ arbol contiene 'DevOps, CI/CD'
- ✅ arbol tabla L1 Lenguajes_Programacion=116
- ✅ arbol tabla L1 Hardware=99
- ✅ arbol tabla L1 Arquitectura=97
- ✅ arbol tabla L1 Bases_de_Datos=68
- ✅ arbol tabla L1 Inteligencia_Artificial=61
- ✅ arbol tabla L1 Sistemas_Operativos=50
- ✅ arbol tabla L1 Redes_y_Comunicaciones=39
- ✅ PDFs v1 mono-etiqueta L1 (o casi) — multi={}
- ✅ ratio max/min train v5 ~2.5-3.5 (doc ~2.87) — ratio=2.872 {'Redes_y_Comunicaciones': 39, 'Sistemas_Operativos': 48, 'Lenguajes_Programacion': 112, 'Inteligencia_Artificial': 60, 'Arquitectura': 74, 'Hardware': 98, 'Bases_de_Datos': 46}
- ✅ sintéticos v3 longitud >= 200 — min=339 mean=417
- ✅ sintéticos v4 longitud >= 200 — min=343 mean=422
- ✅ sintéticos v5 longitud >= 200 — min=317 mean=373

## Conteos L1 (general)

| categoria_l1 | v1 | v2 | v3 | v4 | v5 |
|---|---:|---:|---:|---:|---:|
| Arquitectura | 21 | 56 | 56 | 86 | 97 |
| Bases_de_Datos | 33 | 68 | 68 | 68 | 68 |
| Hardware | 47 | 47 | 99 | 99 | 99 |
| Inteligencia_Artificial | 26 | 26 | 26 | 26 | 61 |
| Lenguajes_Programacion | 116 | 116 | 116 | 116 | 116 |
| Redes_y_Comunicaciones | 25 | 25 | 25 | 39 | 39 |
| Sistemas_Operativos | 15 | 50 | 50 | 50 | 50 |
| **TOTAL** | 283 | 388 | 440 | 484 | 530 |

## Cadena de aumento (filas nuevas)

| Paso | +filas | titulo_origen | L1 afectadas |
|------|-------:|---------------|--------------|
| v1→v2 | 105 | `augment_balanceo_v2` | SO+35, DB+35, Arch+35 |
| v2→v3 | 52 | `augment_rama_hardware_arquitectura_v3` | Hardware+52 |
| v3→v4 | 44 | `augment_rama_ciberseguridad_v4` | Arch+30, Redes+14 |
| v4→v5 | 46 | `augment_rama_ia_texto_ml_v5` | IA+35, Arch+11 |

## Nota sobre el único FAIL (filtro train)

No afecta la veracidad del **árbol**. El train V5 tiene 477 filas; un recálculo ingenuo `longitud >= max(P10, 80)` con P10=299 predice 479. Las 2 filas de diferencia (`synth_arch_0015`, `synth_db_0008`) miden exactamente **299** caracteres y quedan fuera con umbral efectivo **≥ 300** (el mismo desfase de 2 filas ya aparece en train v4). El árbol no declara el umbral exacto de caracteres del train.

## Conclusión

El árbol consolidado V5 es **coherente** con los datasets (84/85 checks). Totales, deltas L1, orígenes sintéticos, prefijos de id, mapeo L1 de Ciberseguridad (sin clase propia), keywords temáticas y nodos `[APLICADO v3/v4/v5]` coinciden con el corpus. El único desajuste es menor y pertenece al **derivado train**, no a la taxonomía.
