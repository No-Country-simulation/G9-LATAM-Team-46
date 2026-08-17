# techmind-frontend

Front-end para el backend FastAPI de TechMind AI (Hackathon ONE G9). Vite + React + TypeScript + Tailwind v4. Diseño responsivo (móvil, tablet, desktop).

## Qué se simplificó respecto al diseño original
- **History** vive 100% en el navegador: lista las clasificaciones de Library guardadas localmente (el backend no las persiste). Tiene filtro por categoría, búsqueda por título, botón **View** para volver a mostrar una clasificación completa en Library, y botón para vaciar el historial. No incluye mensajes de chat.
- **Account** ya no tiene formulario de login: el backend todavía no tiene `/login` activo (está en "Pendiente" en su README), así que solo se muestra un perfil mock + stats calculadas desde lo guardado localmente.
- **Chat**: sin sidebar de conversaciones pasadas (un solo hilo continuo), y sin badge de categoría/confianza en los mensajes, porque `/chat` solo devuelve `respuesta` (no clasifica visiblemente cada turno).
- El indicador **"api · connected"** del navbar ahora es real: hace `GET /health` al montar la app.
- Un solo cliente `src/lib/api.ts` con tres funciones (`classifyContent`, `sendChatMessage`, `checkHealth`).

## Persistencia local (`localStorage`)
`src/lib/storage.ts` guarda en el navegador:
- Últimas 50 clasificaciones (título, texto completo, categoría, confianza, keywords) → `tm_classifications`
- Últimos 60 mensajes de chat → `tm_chat_messages`

Se usa `localStorage` en vez de cookies porque las cookies tienen un límite práctico de ~4KB por cookie — insuficiente para guardar textos considerables. `localStorage` da ~5-10MB por sitio, así que el contenido completo de cada clasificación se guarda tal cual. Si en algún momento se llega a llenar (poco probable), se van descartando automáticamente los registros más viejos en vez de perder el que se acaba de guardar.

Click en cualquier fila de **History** (o el botón **View**) vuelve a la pestaña Library y muestra esa clasificación completa: título, texto original y resultado (categoría, confianza, keywords), con una etiqueta "from history" para distinguirla de una clasificación nueva.

El campo `historial` que pide `POST /chat` se arma a partir de los mensajes guardados — el front es responsable de reenviarlo en cada turno, tal como indica el backend.

## Contrato real de la API (según el README del backend)

```
GET  /health                 -> { "status": "ok" }

POST /contenido
Body: { "titulo": string, "texto": string }
Resp: {
  "categoria": string,
  "probabilidad": number,              // 0-1 (el front lo convierte a % para el anillo)
  "informacion_adicional": string[]    // keywords
}
Errores: 422 si titulo/texto vacíos · 503 si el modelo no está disponible

POST /chat
Body: {
  "texto": string,
  "historial"?: [{ "rol": "user"|"assistant", "contenido": string }]
}
Resp: { "respuesta": string }
```

Notas del backend que ya están contempladas en el front:
- `/chat` nunca devuelve 500 por fallas de DeepSeek — siempre 200 con un mensaje genérico, así que no hace falta un manejo especial de ese caso.
- `/contenido` puede devolver 503 si el modelo no cargó — se muestra como error en el formulario.

## Variables de entorno
Copia `.env.example` a `.env`:
```
VITE_API_BASE_URL=http://127.0.0.1:8000
```
En producción, cambia esto por la URL donde esté desplegado el backend en la nube. CORS del backend ya acepta `http://localhost:5173` (puerto por defecto de Vite).

## Correr el proyecto
```bash
npm install
cp .env.example .env
npm run dev
```

## Deploy en Vercel
1. Importa el repo en Vercel (detecta Vite automáticamente; `vercel.json` ya define `buildCommand`/`outputDirectory` por las dudas).
2. En **Settings → Environment Variables** agrega `VITE_API_BASE_URL` apuntando a la URL pública del backend.
3. El nombre del proyecto en Vercel debe ser `techmind-frontend` para que la URL resultante (`https://techmind-frontend.vercel.app` o el dominio que uses) coincida con la que el backend tiene whitelisteada.

**⚠️ Importante — CORS del backend:** ahora mismo `main.py` solo permite `http://localhost:3000` y `http://localhost:5173`. La URL de producción de Vercel (`https://techmind-frontend.vercel.app` o el dominio custom que uses) **no va a funcionar hasta que el equipo de backend la agregue a `allow_origins`**. Avísales antes de dar el deploy por terminado.

## Diseño responsivo
- El navbar se apila en dos filas en pantallas chicas (logo+estado arriba, tabs abajo con scroll horizontal si no entran) y vuelve a una sola fila en `sm:` (≥640px) en adelante.
- El layout general usa `100vh` con flexbox en `App.tsx`, así que Chat siempre ocupa el alto disponible sin importar cuánto mida el navbar en cada breakpoint.
- Library: formulario y resultado se apilan en una columna en móvil, dos columnas desde `md:` (≥768px).
- History: la tabla tiene scroll horizontal propio en pantallas angostas para no romper el layout.
- Account: las 3 tarjetas de stats pasan a una columna por fila en teléfonos muy chicos (<420px) y a 3 columnas desde ahí.

## Pendiente cuando el backend lo tenga listo
- Agregar el dominio de Vercel al CORS del backend (ver arriba).
- Conectar `AccountPage` a `/login` real cuando esté disponible (hoy es un perfil mock).
- Si en el futuro `/chat` empieza a devolver categoría/confianza por turno, es fácil volver a mostrarlas en la burbuja (se puede ver cómo se hacía en `ChatPage.tsx` del commit anterior).
