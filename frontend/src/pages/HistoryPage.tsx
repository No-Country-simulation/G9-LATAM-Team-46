import { useMemo, useState } from "react";
import { Eye, Trash2 } from "lucide-react";
import { clearClassifications, getClassifications } from "../lib/storage";
import type { ClassifyResult } from "../types";

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString("es", { year: "numeric", month: "2-digit", day: "2-digit" });
}

export default function HistoryPage({ onView }: { onView: (item: ClassifyResult) => void }) {
  const [items, setItems] = useState<ClassifyResult[]>(() => getClassifications());
  const [category, setCategory] = useState("ALL");
  const [search, setSearch] = useState("");

  const categories = useMemo(
    () => ["ALL", ...Array.from(new Set(items.map((i) => i.categoria)))],
    [items],
  );

  const filtered = items.filter((item) => {
    const matchesCategory = category === "ALL" || item.categoria === category;
    const matchesSearch = item.titulo.toLowerCase().includes(search.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const avgConfidence = filtered.length
    ? filtered.reduce((sum, i) => sum + i.probabilidad, 0) / filtered.length
    : 0;

  function handleClear() {
    clearClassifications();
    setItems([]);
  }

  return (
    <div className="p-4 sm:p-6">
      <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-center sm:justify-between">
        <div className="flex flex-wrap gap-2">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setCategory(cat)}
              className={`rounded-full border px-4 py-1.5 font-mono text-xs tracking-wide transition-colors ${
                category === cat
                  ? "border-accent bg-accent text-white"
                  : "border-border text-subtle hover:text-white"
              }`}
            >
              {cat === "ALL" ? "TODAS" : cat.toUpperCase()}
            </button>
          ))}
        </div>

        <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Buscar títulos..."
            className="w-full rounded-lg border border-border bg-panel-2 px-3 py-2 text-sm text-white placeholder:text-muted focus:border-accent sm:w-56"
          />
          {items.length > 0 && (
            <button
              onClick={handleClear}
              className="flex items-center justify-center gap-1.5 rounded-lg border border-border px-3 py-2 text-xs text-subtle hover:border-red-500/40 hover:text-red-400"
            >
              <Trash2 size={14} />
              Vaciar historial
            </button>
          )}
        </div>
      </div>

      <div className="overflow-hidden rounded-xl border border-border bg-panel">
        {filtered.length === 0 ? (
          <div className="p-10 text-center text-sm text-muted">
            Todavía no hay clasificaciones. Clasificá algo en la pestaña Clasificar para verlo acá.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full min-w-[560px] text-left text-sm">
              <thead>
                <tr className="border-b border-border font-mono text-xs tracking-wide text-muted">
                  <th className="px-5 py-3 font-normal">TÍTULO</th>
                  <th className="px-5 py-3 font-normal">CATEGORÍA</th>
                  <th className="px-5 py-3 font-normal">CONFIANZA</th>
                  <th className="px-5 py-3 font-normal">FECHA</th>
                  <th className="px-5 py-3 font-normal"></th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((item) => (
                  <tr
                    key={item.id}
                    onClick={() => onView(item)}
                    className="cursor-pointer border-b border-border last:border-0 hover:bg-panel-2"
                  >
                    <td className="px-5 py-3 text-white">{item.titulo || "Sin título"}</td>
                    <td className="px-5 py-3 text-gray-300">{item.categoria}</td>
                    <td className="px-5 py-3 font-mono text-warn">
                      {item.probabilidad.toFixed(1)}%
                    </td>
                    <td className="px-5 py-3 font-mono text-subtle">
                      {formatDate(item.createdAt)}
                    </td>
                    <td className="px-5 py-3">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onView(item);
                        }}
                        className="flex items-center gap-1.5 rounded-md border border-border px-2.5 py-1 text-xs text-subtle hover:border-accent hover:text-white"
                      >
                        <Eye size={13} />
                        Ver
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {filtered.length > 0 && (
          <div className="flex items-center justify-between border-t border-border px-5 py-3 font-mono text-xs text-muted">
            <span>
              {filtered.length} de {items.length} registros
            </span>
            <span>prom. {avgConfidence.toFixed(1)}%</span>
          </div>
        )}
      </div>
    </div>
  );
}
