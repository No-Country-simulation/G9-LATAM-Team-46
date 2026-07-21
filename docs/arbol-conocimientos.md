# Árbol de conocimientos — TechMind

**Proyecto:** TechMind (Hackathon ONE G9 · Team 46)  
**Propósito:** taxonomía jerárquica para clasificar, etiquetar y organizar contenido técnico (artículos, cursos, tutoriales, notas de estudio).

---

## Cómo se usa en el proyecto

| Nivel | Rol en TechMind |
|-------|-----------------|
| **L1 – Dominio** | Categoría principal del clasificador (salida `categoria`) |
| **L2 – Área** | Subcategoría o refinamiento |
| **L3 – Tema** | Etiquetas / palabras clave (`informacion_adicional`) |
| **L4+ – Detalle** | Contenido educativo profundo (p. ej. temario Java); no es etiqueta ML del MVP |

**Regla práctica del MVP:** el modelo predice sobre un conjunto acotado de categorías L1/L2. El árbol completo sirve como vocabulario de referencia, documentación y expansión futura.

---

## 1. Árbol completo (referencia de conocimiento)

```text
Tecnología
└── Computación e Informática
    ├── Hardware
    │   ├── Arquitectura de Computadores
    │   ├── Procesadores y CPU
    │   ├── Memoria (RAM, ROM, Caché)
    │   ├── Almacenamiento (HDD, SSD, NVMe)
    │   ├── Placas Base y Componentes
    │   └── Periféricos y Dispositivos de E/S
    │
    ├── Software
    │   ├── Sistemas Operativos
    │   │   ├── Fundamentos de SO
    │   │   ├── Administración de Sistemas
    │   │   ├── Linux
    │   │   ├── Windows Server
    │   │   └── macOS / iOS / Android
    │   │
    │   ├── Lenguajes de Programación
    │   │   ├── Clasificación General
    │   │   │   ├── Lenguajes Compilados
    │   │   │   ├── Lenguajes Interpretados
    │   │   │   └── Lenguajes Híbridos / JIT
    │   │   │
    │   │   ├── Paradigmas
    │   │   │   ├── Orientación a Objetos (POO)
    │   │   │   │   ├── Fundamentos POO
    │   │   │   │   ├── Herencia y Polimorfismo
    │   │   │   │   └── Encapsulamiento y Abstracción
    │   │   │   ├── Programación Funcional
    │   │   │   └── Programación Procedimental / Imperativa
    │   │   │
    │   │   ├── Java (detalle curricular)
    │   │   │   ├── Fundamentos
    │   │   │   │   ├── 1. Introducción al Lenguaje Java
    │   │   │   │   │   ├── Objetivos de Aprendizaje
    │   │   │   │   │   ├── Contexto y Evolución del Lenguaje
    │   │   │   │   │   ├── Compiled vs. Interpreted
    │   │   │   │   │   ├── Portability y la Solución de Java (JVM + Bytecode)
    │   │   │   │   │   └── Escritura, Compilación y Ejecución
    │   │   │   │   │       └── Modo Interpretado y JShell
    │   │   │   │   ├── 2. Variables y Tipos de Datos
    │   │   │   │   │   ├── Representación de Variables
    │   │   │   │   │   ├── Identificadores
    │   │   │   │   │   ├── Tipado Fuerte (Strongly Typed)
    │   │   │   │   │   ├── Tipos Primitivos
    │   │   │   │   │   ├── Tipos de Objeto (Reference Types)
    │   │   │   │   │   ├── Reglas y Convenciones de Identificadores
    │   │   │   │   │   ├── Inicialización y Constantes (final)
    │   │   │   │   │   └── Inferencia de Tipos (var)
    │   │   │   │   ├── 3. Operadores y Expresiones
    │   │   │   │   │   ├── Operadores de Asignación y Aritméticos
    │   │   │   │   │   ├── Asignación Compuesta
    │   │   │   │   │   ├── Incremento y Decremento (Prefix vs Postfix)
    │   │   │   │   │   ├── Operadores Relacionales y de Igualdad
    │   │   │   │   │   ├── Operadores Lógicos
    │   │   │   │   │   ├── Operador Ternario
    │   │   │   │   │   ├── Jerarquía y Precedencia
    │   │   │   │   │   ├── Promoción Numérica
    │   │   │   │   │   └── Typecasting (Widening vs Narrowing)
    │   │   │   │   ├── 4. Manejo de Cadenas (Strings) y Caracteres
    │   │   │   │   │   ├── Representación y Escape Characters
    │   │   │   │   │   ├── Inmutabilidad de String
    │   │   │   │   │   ├── Métodos de la Clase String
    │   │   │   │   │   └── Wrapper Classes
    │   │   │   │   ├── 5. Estructuras de Datos: Arreglos (Arrays)
    │   │   │   │   ├── 6. Estructuras de Control de Flujo
    │   │   │   │   │   ├── if / else
    │   │   │   │   │   ├── Bucles (while, do-while, for, for-each)
    │   │   │   │   │   ├── continue y break
    │   │   │   │   │   └── switch / case (clásico, Arrow Syntax y Switch Expressions)
    │   │   │   │   └── 7. Modularización y Métodos
    │   │   │   │       ├── Anatomía de un Método
    │   │   │   │       ├── Convenciones de Nomenclatura
    │   │   │   │       └── Variables Locales y Scope
    │   │   │   ├── Intermedio
    │   │   │   │   ├── 8. Fundamentos de Orientación a Objetos
    │   │   │   │   │   ├── Abstracción
    │   │   │   │   │   ├── Clases e Instancias
    │   │   │   │   │   ├── Operador new
    │   │   │   │   │   ├── Constructores
    │   │   │   │   │   └── Referencias y null
    │   │   │   │   ├── 9. Propiedades de Objetos, Shadowing y this
    │   │   │   │   │   ├── Variables de Instancia vs Locales
    │   │   │   │   │   ├── Getters y Setters
    │   │   │   │   │   ├── Variable Shadowing
    │   │   │   │   │   ├── Referencia this
    │   │   │   │   │   └── Method Overloading
    │   │   │   │   ├── 10. Encapsulamiento y Modificadores de Acceso
    │   │   │   │   │   ├── Principio de Encapsulamiento
    │   │   │   │   │   ├── public y private
    │   │   │   │   │   └── Package-Private
    │   │   │   │   ├── 11. Constructores y Reutilización de Lógica
    │   │   │   │   │   ├── Constructor por Defecto
    │   │   │   │   │   ├── Constructores Personalizados y Sobrecarga
    │   │   │   │   │   └── Constructor Chaining
    │   │   │   │   └── 12. Miembros Estáticos (static)
    │   │   │   │       ├── Variables de Clase
    │   │   │   │       ├── Métodos Estáticos
    │   │   │   │       └── Constantes Globales (static final)
    │   │   │   ├── Avanzado
    │   │   │   │   ├── 13. Herencia (Inheritance)
    │   │   │   │   │   ├── Principio de Herencia
    │   │   │   │   │   ├── Method Overriding y @Override
    │   │   │   │   │   ├── Referencia super
    │   │   │   │   │   ├── Resolución Dinámica de Métodos
    │   │   │   │   │   ├── Clase Object
    │   │   │   │   │   ├── Comparación de Objetos y equals()
    │   │   │   │   │   └── Prevención de NullPointerException
    │   │   │   │   └── 14. Manejo de Excepciones
    │   │   │   │       ├── Jerarquía de Excepciones
    │   │   │   │       ├── Unchecked vs Checked Exceptions
    │   │   │   │       ├── try / catch
    │   │   │   │       ├── throw y throws
    │   │   │   │       ├── Excepciones Personalizadas
    │   │   │   │       └── Stack Trace
    │   │   │   └── Aplicaciones
    │   │   │       ├── 15. Paquetes, Módulos y Firma main
    │   │   │       └── 16. Transición a IDEs
    │   │   │
    │   │   ├── Python
    │   │   │   ├── Fundamentos del Lenguaje
    │   │   │   ├── Estructuras de Datos
    │   │   │   ├── POO en Python
    │   │   │   └── Ecosistema (pip, venv, Jupyter)
    │   │   │
    │   │   ├── JavaScript / TypeScript
    │   │   │   ├── Fundamentos JS
    │   │   │   ├── TypeScript
    │   │   │   └── Entorno (Node.js, npm)
    │   │   │
    │   │   └── Otros (C#, Go, Kotlin, SQL como lenguaje)
    │   │
    │   ├── Frameworks y Herramientas de Desarrollo
    │   │   ├── Backend (Spring Boot, Django, FastAPI, Express, NestJS, .NET)
    │   │   ├── Frontend (HTML/CSS, React, Angular, Vue)
    │   │   └── Mobile (Android, iOS, Flutter, React Native)
    │   │
    │   ├── Bases de Datos y Persistencia
    │   │   ├── Relacionales (SQL): MySQL, PostgreSQL, Oracle
    │   │   ├── NoSQL: MongoDB, Redis, Cassandra
    │   │   └── ORM / ODM (Hibernate, JPA, SQLAlchemy, Prisma)
    │   │
    │   ├── Redes y Comunicaciones
    │   │   ├── Modelos OSI y TCP/IP
    │   │   ├── Protocolos (HTTP, HTTPS, REST, GraphQL, gRPC, WebSockets)
    │   │   └── Diseño de APIs
    │   │
    │   ├── Inteligencia Artificial, Machine Learning y Ciencia de Datos
    │   │   ├── Fundamentos de ML
    │   │   ├── Aprendizaje Supervisado / No Supervisado / Refuerzo
    │   │   ├── Deep Learning y Redes Neuronales
    │   │   ├── NLP / Procesamiento de Texto
    │   │   ├── Computer Vision
    │   │   ├── Herramientas (Scikit-Learn, TensorFlow, PyTorch, Pandas)
    │   │   ├── EDA y Preprocesamiento
    │   │   └── MLOps
    │   │
    │   ├── Ciberseguridad
    │   │   ├── Fundamentos de Seguridad
    │   │   ├── Criptografía
    │   │   ├── Ethical Hacking y Pentesting
    │   │   ├── Seguridad en Aplicaciones Web (OWASP)
    │   │   └── DevSecOps
    │   │
    │   ├── DevOps, CI/CD y Automatización
    │   │   ├── Control de Versiones (Git)
    │   │   ├── Contenedores (Docker)
    │   │   ├── Orquestación (Kubernetes)
    │   │   ├── Pipelines CI/CD
    │   │   └── Infrastructure as Code (Terraform, Ansible)
    │   │
    │   └── Arquitectura de Software y Buenas Prácticas
    │       ├── Patrones de Diseño
    │       ├── Principios SOLID y Clean Architecture
    │       ├── Arquitecturas Modernas (Microservicios, Serverless, Event-Driven)
    │       ├── Clean Code y Refactoring
    │       └── Testing (Unitario, Integración, E2E)
    │
    ├── Cloud Computing y Servicios en la Nube
    │   ├── Modelos de Servicio (IaaS, PaaS, SaaS, FaaS)
    │   ├── Oracle Cloud Infrastructure (OCI)
    │   │   ├── Compute, Object Storage, Functions
    │   │   ├── Container Engine (OKE)
    │   │   └── Autonomous Database
    │   ├── Amazon Web Services (AWS)
    │   ├── Microsoft Azure
    │   └── Google Cloud Platform (GCP)
    │
    └── Tecnologías Emergentes
        ├── Internet de las Cosas (IoT) y Edge Computing
        ├── Blockchain y Web3
        ├── Realidad Aumentada / Virtual
        └── 5G y Redes de Nueva Generación
```

---

## 2. Taxonomía del clasificador (MVP)

Conjunto **cerrado y equilibrado** de categorías para el modelo de Data Science y la API (`categoria`).

### Categorías L1 (salida principal)

| ID | Categoría | Descripción breve | Ejemplos de contenido |
|----|-----------|-------------------|------------------------|
| `hardware` | Hardware | Componentes físicos y arquitectura de equipos | CPU, RAM, SSD, placas base |
| `sistemas_operativos` | Sistemas Operativos | SO, administración y shells | Linux, Windows Server, procesos |
| `lenguajes` | Lenguajes de Programación | Sintaxis, tipos, paradigmas, un lenguaje concreto | Java, Python, JS, POO |
| `backend` | Backend | APIs, servicios y frameworks servidor | Spring Boot, FastAPI, REST |
| `frontend` | Frontend | UI web y frameworks de cliente | React, HTML/CSS, Vue |
| `mobile` | Mobile | Apps móviles nativas o multiplataforma | Android, Flutter, React Native |
| `bases_de_datos` | Bases de Datos | Persistencia, SQL/NoSQL, ORM | PostgreSQL, MongoDB, JPA |
| `redes` | Redes y APIs | Protocolos, redes y diseño de APIs | HTTP, TCP/IP, GraphQL |
| `data_science` | Data Science y ML | ML, NLP, datos y notebooks | Scikit-Learn, TF-IDF, EDA |
| `ciberseguridad` | Ciberseguridad | Seguridad, crypto, OWASP | Pentesting, DevSecOps |
| `devops` | DevOps y CI/CD | Git, contenedores, pipelines, IaC | Docker, Kubernetes, Git |
| `arquitectura` | Arquitectura de Software | Diseño, patrones, testing, clean code | SOLID, microservicios |
| `cloud` | Cloud Computing | Nube y servicios cloud | OCI, AWS, IaaS/PaaS |
| `emergentes` | Tecnologías Emergentes | IoT, blockchain, AR/VR, 5G | Web3, Edge, IoT |

> Los ejemplos del brief (`Backend`, `Data Science`) mapean a `backend` y `data_science`.

### Subtemas frecuentes (L2/L3 → `informacion_adicional`)

Palabras clave sugeridas (no son clases del modelo; se extraen o se asocian por reglas/TF-IDF):

| Categoría L1 | Keywords de apoyo |
|--------------|-------------------|
| `lenguajes` | Java, Python, JavaScript, TypeScript, POO, JVM, variables, excepciones, herencia |
| `backend` | Spring Boot, FastAPI, Django, Express, API REST, microservicios, endpoints |
| `frontend` | React, Angular, Vue, HTML, CSS, DOM, componentes |
| `bases_de_datos` | SQL, MySQL, PostgreSQL, Oracle, MongoDB, Redis, Hibernate, JPA, ORM |
| `data_science` | Machine Learning, TF-IDF, clasificación, Pandas, Scikit-Learn, EDA, NLP |
| `cloud` | OCI, Object Storage, AWS, Azure, GCP, IaaS, PaaS, Functions |
| `devops` | Git, Docker, Kubernetes, CI/CD, Terraform, Ansible |
| `redes` | HTTP, HTTPS, REST, GraphQL, WebSockets, TCP/IP, OSI |
| `arquitectura` | SOLID, Clean Architecture, patrones de diseño, testing, refactoring |
| `ciberseguridad` | OWASP, criptografía, autenticación, pentesting |
| `sistemas_operativos` | Linux, Windows, procesos, permisos, shell |
| `hardware` | CPU, RAM, SSD, arquitectura, periféricos |
| `mobile` | Android, iOS, Flutter, React Native |
| `emergentes` | IoT, Blockchain, Web3, AR, VR, 5G |

---

## 5. Criterios de diseño (para el equipo)

1. **Profundidad desigual a propósito:** Java está expandido al detalle curricular (ONE/Alura). Otras ramas quedan en L2–L3 hasta que haya dataset suficiente.  
2. **Clasificador simple primero:** 14 clases L1 + keywords; evitar cientos de hojas del temario Java como clases del modelo.  
3. **Un contenido, una categoría principal:** si un texto mezcla Java + Spring, priorizar la intención dominante (p. ej. framework → `backend`; sintaxis Java → `lenguajes`).  
4. **Alineación con el stack del hackathon:** Java, Spring Boot, Python, Scikit-Learn, OCI tienen cobertura explícita.  
5. **Extensible:** se pueden añadir idiomas o nodos L4 sin cambiar las 14 categorías del MVP.

---

*Documento del equipo G9-LATAM-Team-46 · TechMind · Hackathon ONE G9*
