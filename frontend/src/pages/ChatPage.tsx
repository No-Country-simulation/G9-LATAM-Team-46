import { useEffect, useRef, useState } from "react";
import { ArrowUp } from "lucide-react";
import { sendChatMessage } from "../lib/api";
import { getChatMessages, saveChatMessages } from "../lib/storage";
import type { ChatMessage } from "../types";

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>(() => getChatMessages());
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend() {
    const texto = input.trim();
    if (!texto || loading) return;

    const userMsg: ChatMessage = {
      id: crypto.randomUUID(),
      rol: "user",
      contenido: texto,
      createdAt: new Date().toISOString(),
    };
    // El backend no persiste conversaciones: reenviamos el historial completo
    // (guardado en cookie) en cada mensaje, tal como pide el contrato de /chat.
    const next = saveChatMessages([...messages, userMsg]);
    setMessages(next);
    setInput("");
    setLoading(true);

    try {
      const respuesta = await sendChatMessage(texto, messages);
      const assistantMsg: ChatMessage = {
        id: crypto.randomUUID(),
        rol: "assistant",
        contenido: respuesta,
        createdAt: new Date().toISOString(),
      };
      setMessages(saveChatMessages([...next, assistantMsg]));
    } catch (err) {
      const errorMsg: ChatMessage = {
        id: crypto.randomUUID(),
        rol: "assistant",
        contenido:
          err instanceof Error
            ? `Error: ${err.message}`
            : "Ocurrió un error al contactar la API.",
        createdAt: new Date().toISOString(),
      };
      setMessages(saveChatMessages([...next, errorMsg]));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex h-full flex-col">
      <div className="flex-1 overflow-y-auto px-4 py-4 sm:px-6 sm:py-6">
        {messages.length === 0 ? (
          <div className="mt-24 text-center text-sm text-muted">
            Preguntá sobre un tema técnico para empezar la conversación.
          </div>
        ) : (
          <div className="mx-auto flex max-w-3xl flex-col gap-4">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex ${msg.rol === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[88%] rounded-xl border px-4 py-3 text-sm sm:max-w-[80%] ${
                    msg.rol === "user"
                      ? "border-accent/40 bg-accent/20 text-white"
                      : "border-border bg-panel text-gray-200"
                  }`}
                >
                  <p className="whitespace-pre-wrap">{msg.contenido}</p>
                </div>
              </div>
            ))}
            <div ref={bottomRef} />
          </div>
        )}
      </div>

      <div className="border-t border-border p-3 sm:p-4">
        <div className="mx-auto flex max-w-3xl items-center gap-2 sm:gap-3">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Preguntá sobre un tema técnico..."
            className="flex-1 rounded-lg border border-border bg-panel-2 px-4 py-3 text-sm text-white placeholder:text-muted focus:border-accent"
          />
          <button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-accent text-white transition-colors hover:bg-accent-hover disabled:opacity-50"
          >
            <ArrowUp size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
