import type { ClassifyResult, ChatMessage } from "../types";

/**
 * Persistencia en localStorage del navegador (sin backend de historial).
 * A diferencia de las cookies (~4KB por cookie, insuficiente para textos
 * largos), localStorage da ~5-10MB por sitio, suficiente para guardar
 * el contenido completo de cada clasificación.
 */
const CLASSIFICATIONS_KEY = "tm_classifications";
const CHAT_KEY = "tm_chat_messages";
const MAX_CLASSIFICATIONS = 50;
const MAX_CHAT_MESSAGES = 60;

function readJSON<T>(key: string, fallback: T): T {
  try {
    const raw = localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
}

// Si el storage está lleno (QuotaExceededError) o en modo privado bloqueado,
// vamos descartando los registros más viejos hasta que entre, en vez de
// perder silenciosamente el que se acaba de guardar.
function writeWithFallback<T>(key: string, items: T[]): T[] {
  let list = items;
  while (list.length > 0) {
    try {
      localStorage.setItem(key, JSON.stringify(list));
      return list;
    } catch {
      list = list.slice(0, Math.ceil(list.length / 2));
    }
  }
  try {
    localStorage.removeItem(key);
  } catch {
    /* ignore */
  }
  return [];
}

// Registros guardados antes de sumar ranking_categorias/contenidos_relacionados
// al backend no tienen esos campos: se normalizan acá para que el resto de la
// app pueda asumir siempre arrays (nunca undefined).
function normalizeClassification(item: ClassifyResult): ClassifyResult {
  return {
    ...item,
    keywords: item.keywords ?? [],
    rankingCategorias: item.rankingCategorias ?? [],
    contenidosRelacionados: item.contenidosRelacionados ?? [],
  };
}

export function getClassifications(): ClassifyResult[] {
  return readJSON<ClassifyResult[]>(CLASSIFICATIONS_KEY, []).map(normalizeClassification);
}

export function saveClassification(result: ClassifyResult) {
  const current = getClassifications();
  const next = [result, ...current].slice(0, MAX_CLASSIFICATIONS);
  return writeWithFallback(CLASSIFICATIONS_KEY, next);
}

export function clearClassifications() {
  localStorage.removeItem(CLASSIFICATIONS_KEY);
}

export function getChatMessages(): ChatMessage[] {
  return readJSON<ChatMessage[]>(CHAT_KEY, []);
}

export function saveChatMessages(messages: ChatMessage[]) {
  const trimmed = messages.slice(-MAX_CHAT_MESSAGES);
  return writeWithFallback(CHAT_KEY, trimmed);
}

export function clearChatMessages() {
  localStorage.removeItem(CHAT_KEY);
}
