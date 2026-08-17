import type { ChatMessage, ClassifyResult } from "../types";

/**
 * Cliente para el backend de TechMind AI (FastAPI).
 * Ver README del backend: /contenido, /chat, /health.
 */
const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "https://nintendo-trapeze-during.ngrok-free.dev";

// El plan free de ngrok muestra una página HTML de advertencia a cualquier
// request que no venga de un navegador "normal". Este header la salta y
// deja pasar la respuesta JSON real de la API.
const NGROK_HEADERS = { "ngrok-skip-browser-warning": "true" };

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...NGROK_HEADERS },
    body: JSON.stringify(body),
  });
  if (res.status === 503) {
    throw new Error("El modelo no está disponible en este momento.");
  }
  if (!res.ok) {
    throw new Error(`Error ${res.status}: ${res.statusText}`);
  }
  return res.json() as Promise<T>;
}

// GET /health — usado por el indicador "api · connected" del navbar.
export async function checkHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${BASE_URL}/health`, { headers: NGROK_HEADERS });
    if (!res.ok) return false;
    const data = await res.json();
    return data?.status === "ok";
  } catch {
    return false;
  }
}

// POST /contenido
interface ContenidoResponse {
  categoria: string;
  probabilidad: number; // 0-1
  informacion_adicional: string[];
}

export async function classifyContent(
  titulo: string,
  texto: string,
): Promise<Omit<ClassifyResult, "id" | "createdAt">> {
  const data = await post<ContenidoResponse>("/contenido", { titulo, texto });
  return {
    titulo,
    texto,
    categoria: data.categoria,
    probabilidad: Math.round(data.probabilidad * 1000) / 10, // 0-1 -> 0-100 con 1 decimal
    keywords: data.informacion_adicional ?? [],
  };
}

// POST /chat
interface ChatResponse {
  respuesta: string;
}

export async function sendChatMessage(
  texto: string,
  historial: ChatMessage[],
): Promise<string> {
  const data = await post<ChatResponse>("/chat", {
    texto,
    historial: historial.map(({ rol, contenido }) => ({ rol, contenido })),
  });
  return data.respuesta;
}
