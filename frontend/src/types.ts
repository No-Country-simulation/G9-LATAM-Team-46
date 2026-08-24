// Categoría alternativa que no ganó, pero el modelo consideró plausible.
export interface RankingCategoria {
  categoria: string;
  probabilidad: number; // 0-1
}

// Contenido ya clasificado y parecido al que se acaba de enviar.
export interface ContenidoRelacionado {
  titulo: string;
  categoria: string;
  similitud: number; // 0-1
}

// Ejemplo de uso real que devuelve el backend (GET /categorias), para
// prellenar el formulario de clasificación con un caso de muestra.
export interface EjemploUso {
  titulo: string;
  texto: string;
  categoria: string;
}

export interface ClassifyResult {
  id: string;
  titulo: string;
  texto: string;
  categoria: string;
  probabilidad: number; // 0-100 (ya convertido para mostrar; la API devuelve 0-1)
  keywords: string[]; // viene de informacion_adicional
  rankingCategorias: RankingCategoria[]; // hasta 4, puede venir vacío, nunca incluye la ganadora
  contenidosRelacionados: ContenidoRelacionado[]; // puede venir vacío
  createdAt: string; // ISO date
}

export interface ChatMessage {
  id: string;
  rol: "user" | "assistant";
  contenido: string;
  createdAt: string;
}
