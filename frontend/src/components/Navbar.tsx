import { useEffect, useState } from "react";
import { Library, MessageSquare, User, History, Circle } from "lucide-react";
import type { ReactNode } from "react";
import { checkHealth } from "../lib/api";

export type Tab = "library" | "history" | "chat" | "account";

const TABS: { id: Tab; label: string; icon: ReactNode }[] = [
  { id: "library", label: "CLASIFICAR", icon: <Library size={14} /> },
  { id: "history", label: "BIBLIOTECA", icon: <History size={14} /> },
  { id: "chat", label: "CHAT", icon: <MessageSquare size={14} /> },
  { id: "account", label: "CUENTA", icon: <User size={14} /> },
];

export default function Navbar({
  active,
  onChange,
}: {
  active: Tab;
  onChange: (tab: Tab) => void;
}) {
  const [online, setOnline] = useState<boolean | null>(null);

  useEffect(() => {
    let cancelled = false;
    checkHealth().then((ok) => {
      if (!cancelled) setOnline(ok);
    });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <header className="flex shrink-0 flex-wrap items-center justify-between gap-x-4 gap-y-3 border-b border-border px-4 py-3 sm:flex-nowrap sm:px-6 sm:py-4">
      <div className="flex items-center gap-2 sm:gap-3">
        <div className="h-7 w-7 shrink-0 rounded-md bg-accent sm:h-8 sm:w-8" />
        <span className="text-base font-bold text-white sm:text-lg">TechMind AI</span>
        <span className="hidden rounded border border-border px-2 py-0.5 font-mono text-xs text-subtle sm:inline">
          v2.4
        </span>
      </div>

      {/* Estado de la API: 1ra fila en móvil, extremo derecho en desktop */}
      <div className="order-2 flex items-center gap-1.5 font-mono text-xs text-subtle sm:order-3">
        <span className="hidden sm:inline">
          api · {online === null ? "verificando..." : online ? "conectado" : "desconectado"}
        </span>
        <Circle
          size={8}
          className={
            online === null
              ? "fill-muted text-muted"
              : online
                ? "fill-ok text-ok"
                : "fill-red-500 text-red-500"
          }
        />
      </div>

      {/* Tabs: ocupan todo el ancho y se apilan debajo en móvil, scroll horizontal si no entran */}
      <nav className="order-3 flex w-full items-center gap-1 overflow-x-auto sm:order-2 sm:w-auto sm:overflow-visible">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onChange(tab.id)}
            className={`flex shrink-0 items-center gap-2 rounded-md px-3 py-2 font-mono text-xs tracking-wide transition-colors sm:px-4 ${
              active === tab.id ? "bg-accent text-white" : "text-subtle hover:text-white"
            }`}
          >
            {tab.icon}
            {tab.label}
          </button>
        ))}
      </nav>
    </header>
  );
}
