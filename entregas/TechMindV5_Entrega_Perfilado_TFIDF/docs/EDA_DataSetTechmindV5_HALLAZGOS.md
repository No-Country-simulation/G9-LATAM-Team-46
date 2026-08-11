# Hallazgos EDA — DataSetTechmind V5 (perfilado)

- fecha_utc: 2026-08-11T14:43:37.632217+00:00
- fuente: `../data/DataSetTechmindV5_perfilado.csv`
- n_rows: 1061
- n_origenes: 105
- ratio L1 max/min: 1.0467
- recommend_group_split: True
- |vocab|: 20769  hapax%: 43.5
- min_df table: {1: 20769, 2: 10959, 3: 7987, 5: 5320}
- flags: {'toc': np.int64(0), 'cmd_list': np.int64(0), 'figura': np.int64(0)}

## Balance

| L1 | n | % |
|----|--:|--:|
| `Arquitectura` | 150 | 14.14 |
| `Bases_de_Datos` | 150 | 14.14 |
| `Hardware` | 157 | 14.8 |
| `Inteligencia_Artificial` | 153 | 14.42 |
| `Lenguajes_Programacion` | 150 | 14.14 |
| `Redes_y_Comunicaciones` | 151 | 14.23 |
| `Sistemas_Operativos` | 150 | 14.14 |

## Concentración por origen (top1_share)

           categoria_l1  n_origenes                                                   top1_origen  top1_n  top1_share_pct  top3_share_pct
 Redes_y_Comunicaciones           4                                Conceptos básicos de redes.pdf      92            60.9            92.7
               Hardware           5                      Módulo 1 y 2 Fundamentos de Hardware.pdf      61            38.9            79.0
 Lenguajes_Programacion          11                                       Tkinter_Fundamental.pdf      49            32.7            74.0
         Bases_de_Datos          16                                           SQL_Fundamental.pdf      36            24.0            60.7
Inteligencia_Artificial          13                    IA_Clasificacion_Texto_RAG_Fundamental.pdf      31            20.3            50.3
           Arquitectura          39             Ciberseguridad_Fundamentos_AppSec_Fundamental.pdf      26            17.3            28.0
    Sistemas_Operativos          19 Sistemas_Operativos_Memoria_Virtual_PageCache_Fundamental.pdf      26            17.3            46.0

## Términos con mayor lift por L1 (df≥5)

- **Arquitectura:** topic, stock, spans, sinkhole, sdk, scopes, schemas, remaining
- **Bases_de_Datos:** vacuum, transmutar, tombstones, tabla_de_vendedores, statement, sstable, someter, selectividad
- **Hardware:** voltajes, transistores, termica, tantalio, semiconductores, semiconductor, resistencias, portadores
- **Inteligencia_Artificial:** visualizaciones, veamos, texte, semma, recopilar, recopilacion, rag, puedas
- **Lenguajes_Programacion:** try, tk.stringvar, tk.label, submit, str, root.mainloop, reentrantlock, recolector
- **Redes_y_Comunicaciones:** ssid, smtp, retransmisiones, representado, pki, octeto, musica, middleboxes
- **Sistemas_Operativos:** vfs, tick, starvation, sleeper, semaphores, semaforo, sched_rr, sched_fifo

## Implicaciones (fuera de este EDA)
1. Valorar GroupShuffleSplit por `titulo_origen`.
2. Valorar min_df≈2 dado el % de hapax.
3. Train / joblib / índice **no** se hacen en este notebook.

