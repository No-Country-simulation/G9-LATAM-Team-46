export interface ClassifyResult {
  id: string;
  titulo: string;
  texto: string;
  categoria: string;
  probabilidad: number; // 0-100 (ya convertido para mostrar; la API devuelve 0-1)
  keywords: string[]; // viene de informacion_adicional
  createdAt: string; // ISO date
}

export interface ChatMessage {
  id: string;
  rol: "user" | "assistant";
  contenido: string;
  createdAt: string;
}
