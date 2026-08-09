# Guía de ramas — G9-LATAM-Team-46 (TechMind AI)

Cómo trabajar con Git en este repositorio, paso a paso.

## Ramas activas por área

| Rama | Área |
|---|---|
| `feat/dataset` | Dataset (Persona 2) |
| `feat/eda` | Análisis exploratorio (Persona 3) |
| `feat/ml-nlp` | Modelo de clasificación y NLP (Persona 4/5) |
| `feat/backend` | API REST (Persona 6) |
| `feat/devops` | Despliegue en OCI (Persona 7) |
| `feat/frontend` | Interfaz (Persona 8) |

`main` es la rama principal. Nadie hace push directo ahí, todo pasa por Pull Request.

## Configuración inicial (solo la primera vez)

Si es la primera vez que vas a trabajar con este repositorio en tu computador, empieza aquí. Si ya lo tienes clonado, salta directo a "Flujo de trabajo".

1. **Clona el repositorio oficial** (una sola vez, en la carpeta donde quieras tener el proyecto):
   ```bash
   git clone https://github.com/No-Country-simulation/G9-LATAM-Team-46.git
   cd G9-LATAM-Team-46
   ```

2. **Verifica que estás parado en la raíz correcta del repo**:
   ```bash
   git rev-parse --show-toplevel
   ```
   Debe mostrar la ruta donde acabas de clonar, terminando en `G9-LATAM-Team-46`. Si te muestra otra ruta (por ejemplo tu carpeta de usuario completa), significa que hay un repositorio Git de otra carpeta interfiriendo — no sigas, pide ayuda antes de continuar.

3. **Revisa qué ramas existen** (incluyendo las remotas, que quizás no tengas descargadas todavía):
   ```bash
   git branch -a
   ```
   Vas a ver las ramas de cada área listadas como `remotes/origin/feat/...`. Que aparezcan ahí no significa que ya las tengas para trabajar — el siguiente paso crea tu copia local.

4. **Crea tu copia local de la rama de tu área**, basada en la remota:
   ```bash
   git checkout -b feat/<tu-área> origin/feat/<tu-área>
   ```
   Ejemplo, si eres de dataset:
   ```bash
   git checkout -b feat/dataset origin/feat/dataset
   ```

5. **Confirma en qué rama quedaste parado**:
   ```bash
   git branch
   ```
   Debe aparecer un asterisco `*` junto al nombre de tu rama.

A partir de aquí, sigue con el flujo de trabajo normal (siguiente sección) cada vez que vuelvas a trabajar.

## Si ya tenías trabajo avanzado en otra carpeta, antes de crear tu rama

Es normal que algunos hayan empezado a programar en una carpeta local suelta, sin haber clonado el repo desde el principio. Si es tu caso, no lo pierdas — se puede incorporar:

1. Sigue los pasos 1 a 5 de "Configuración inicial" para tener el repo clonado y tu rama creada correctamente.
2. Copia tus archivos de trabajo (código, no carpetas como `venv/` o `.git/` de tu carpeta vieja) hacia adentro de la carpeta correspondiente del repo recién clonado. Por ejemplo, si eres de backend:
   ```bash
   Copy-Item -Path C:\ruta\a\tu\carpeta-vieja\* -Destination C:\ruta\al\repo\G9-LATAM-Team-46\backend -Recurse -Exclude venv,.git
   ```
3. Verifica qué se va a agregar antes de comprometerlo:
   ```bash
   git status
   ```
   Revisa con calma que no aparezca `venv/`, `.git/`, ni archivos personales que no correspondan al proyecto.
4. Si todo se ve bien, confirma los cambios:
   ```bash
   git add .
   git commit -m "feat: incorpora avance previo de <tu-área>"
   git push origin feat/<tu-área>
   ```

Si tenías además un repositorio Git separado ya iniciado en tu carpeta vieja (con commits propios), avisa antes de este paso — hay una forma de traer ese historial también, en vez de solo copiar los archivos sueltos.

## Flujo de trabajo

Esto es lo que repites cada vez que vuelvas a trabajar en el proyecto, ya con todo configurado.

1. **Actualiza tu copia local de `main`** antes de empezar a trabajar:
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Cambia a la rama de tu área** (no crees una nueva, ya existen):
   ```bash
   git checkout feat/<tu-área>
   git pull origin feat/<tu-área>
   ```

3. **Trabaja y confirma tus cambios con commits descriptivos**, usando el formato `tipo: descripción corta`:
   - `feat:` algo nuevo
   - `fix:` corrección de un error
   - `docs:` documentación
   - `refactor:` cambios internos sin alterar comportamiento
   - `test:` pruebas

   Ejemplo:
   ```bash
   git add .
   git commit -m "feat: agrega endpoint de clasificación"
   ```

4. **Sube tu rama al repositorio oficial**:
   ```bash
   git push origin feat/<tu-área>
   ```

5. **Abre un Pull Request** hacia `main` desde GitHub, describiendo brevemente qué incluye el cambio.

6. **Espera revisión** antes de mergear. Aunque tengas permisos de administrador, no te auto-apruebes ni mergees sin que alguien más lo revise.

## Si tu rama se queda desactualizada respecto a `main`

Cuando `main` avanza con cambios de otras áreas, actualiza tu rama antes de seguir trabajando o antes de abrir el PR:

```bash
git checkout feat/<tu-área>
git merge main
```

Si aparecen conflictos, resuélvelos localmente antes de hacer push.

## Preguntas frecuentes

**¿Puedo crear una rama nueva si mi tarea no calza con ninguna de las existentes?**
Sí, siguiendo el mismo patrón: `feat/<área>-<detalle>`, por ejemplo `feat/backend-tests`.

**¿Qué hago si terminé mi parte y quiero seguir aportando?**
Habla con el área correspondiente antes de tocar su rama directamente — evita hacer cambios sin avisar a quien la está llevando.

**¿Dónde reporto si algo del flujo no está funcionando?**
En el canal del equipo, para que se ajuste esta guía si hace falta.
