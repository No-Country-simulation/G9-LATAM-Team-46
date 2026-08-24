import type { ChatMessage, ClassifyResult, RankingCategoria, ContenidoRelacionado, EjemploUso } from "../types";

/**
 * Cliente para el backend de TechMind AI (FastAPI).
 * Ver README del backend: /contenido, /chat, /health, /categorias.
 */
const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "https://hurray-amply-handgrip.ngrok-free.dev";

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

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, { headers: NGROK_HEADERS });
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
  // Hasta 4 categorías alternativas, nunca incluye la ganadora. Puede venir vacía.
  ranking_categorias: RankingCategoria[];
  // Contenido ya clasificado y similar. Puede venir vacía (no es un error).
  contenidos_relacionados: ContenidoRelacionado[];
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
    rankingCategorias: data.ranking_categorias ?? [],
    contenidosRelacionados: data.contenidos_relacionados ?? [],
  };
}

// GET /categorias — ejemplos de uso reales (con título, texto y categoría
// esperada) para los botones de ejemplo de Library.
interface CategoriasResponse {
  generado_por: string;
  total: number;
  terminos: EjemploUso[];
}

export async function getEjemplos(): Promise<EjemploUso[]> {
  const data = await get<CategoriasResponse>("/categorias");
  return data.terminos ?? [];
}

// GET /sugerencias — una sugerencia de ejemplo (título + texto) para
// prellenar el formulario. Se maneja de forma defensiva porque el shape
// exacto no está confirmado: puede venir como un objeto suelto, un array,
// o envuelto en { terminos: [...] } / { sugerencias: [...] }.
export async function getSugerencia(): Promise<EjemploUso | null> {
  const data = await get<
    EjemploUso | EjemploUso[] | { terminos: EjemploUso[] } | { sugerencias: EjemploUso[] }
  >("/sugerencias");

  if (Array.isArray(data)) {
    return data.length > 0 ? data[Math.floor(Math.random() * data.length)] : null;
  }
  if ("titulo" in data && "texto" in data) {
    return data;
  }
  const lista = "terminos" in data ? data.terminos : data.sugerencias;
  return lista?.length > 0 ? lista[Math.floor(Math.random() * lista.length)] : null;
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
