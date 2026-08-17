import { useEffect, useState } from "react";
import { classifyContent } from "../lib/api";
import { getClassifications, saveClassification } from "../lib/storage";
import ConfidenceRing from "../components/ConfidenceRing";
import type { ClassifyResult } from "../types";

export default function LibraryPage({
  presetResult,
}: {
  presetResult?: ClassifyResult | null;
}) {
  const [titulo, setTitulo] = useState("");
  const [texto, setTexto] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ClassifyResult | null>(
    () => getClassifications()[0] ?? null,
  );
  const [viewingSaved, setViewingSaved] = useState(false);

  // Cuando llega una clasificación elegida desde History, la mostramos acá
  // (resultado + el título/texto originales) en vez de perder lo que el
  // usuario tenía escrito en el formulario.
  useEffect(() => {
    if (!presetResult) return;
    setResult(presetResult);
    setTitulo(presetResult.titulo);
    setTexto(presetResult.texto);
    setViewingSaved(true);
  }, [presetResult]);

  async function handleSubmit() {
    if (!texto.trim()) return;
    setLoading(true);
    setError(null);
    setViewingSaved(false);
    try {
      const data = await classifyContent(titulo, texto);
      const saved: ClassifyResult = {
        ...data,
        id: crypto.randomUUID(),
        createdAt: new Date().toISOString(),
      };
      saveClassification(saved);
      setResult(saved);
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo clasificar el contenido.");
    } finally {
      setLoading(false);
    }
  }

  function handleClear() {
    setTitulo("");
    setTexto("");
    setError(null);
    setViewingSaved(false);
  }

  return (
    <div className="grid gap-4 p-4 sm:gap-6 sm:p-6 md:grid-cols-2">
      {/* Formulario */}
      <section className="rounded-xl border border-border bg-panel p-4 sm:p-6">
        <h2 className="text-lg font-bold text-white">Clasificar contenido</h2>
        <p className="mt-1 text-sm text-subtle">
          Pega un documento técnico, changelog o publicación. El modelo devuelve una categoría
          principal con su nivel de confianza y palabras clave extraídas.
        </p>

        <label className="mt-6 block font-mono text-xs tracking-wide text-muted">TÍTULO</label>
        <input
          value={titulo}
          onChange={(e) => {
            setTitulo(e.target.value);
            setViewingSaved(false);
          }}
          placeholder="Introducción a FastAPI"
          className="mt-2 w-full rounded-lg border border-border bg-panel-2 px-3 py-2 text-sm text-white placeholder:text-muted focus:border-accent"
        />

        <div className="mt-6 flex items-center justify-between">
          <label className="font-mono text-xs tracking-wide text-muted">CONTENIDO</label>
          <span className="font-mono text-xs text-muted">{texto.length} / 4000</span>
        </div>
        <textarea
          value={texto}
          onChange={(e) => {
            setTexto(e.target.value.slice(0, 4000));
            setViewingSaved(false);
          }}
          rows={10}
          placeholder="Pega tu contenido aquí..."
          className="mt-2 w-full resize-none rounded-lg border border-border bg-panel-2 px-3 py-2 font-mono text-sm text-white placeholder:text-muted focus:border-accent"
        />

        {error && <p className="mt-3 text-sm text-red-400">{error}</p>}

        <div className="mt-6 flex flex-col gap-3 sm:flex-row">
          <button
            onClick={handleSubmit}
            disabled={loading || !texto.trim()}
            className="rounded-lg bg-accent px-5 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-accent-hover disabled:opacity-50"
          >
            {loading ? "Procesando..." : "Clasificar y guardar"}
          </button>
          <button
            onClick={handleClear}
            className="rounded-lg border border-border px-5 py-2.5 text-sm font-semibold text-subtle hover:text-white"
          >
            Limpiar
          </button>
        </div>
      </section>

      {/* Resultado */}
      <section className="rounded-xl border border-border bg-panel p-4 sm:p-6">
        <div className="flex items-center justify-between">
          <span className="font-mono text-xs tracking-wide text-muted">RESULTADO</span>
          {viewingSaved && (
            <span className="rounded border border-border px-2 py-0.5 font-mono text-xs text-subtle">
              desde el historial
            </span>
          )}
        </div>

        {!result ? (
          <div className="mt-16 text-center text-sm text-muted">
            Clasifica contenido para ver un resultado acá.
          </div>
        ) : (
          <>
            <div className="mt-4 flex flex-col items-center gap-4 text-center sm:flex-row sm:items-center sm:gap-6 sm:text-left">
              <ConfidenceRing value={result.probabilidad} />
              <div>
                <span className="font-mono text-xs tracking-wide text-muted">
                  CATEGORÍA PRINCIPAL
                </span>
                <div className="mt-2 inline-block rounded-full border border-warn/40 px-4 py-1 font-mono text-sm text-warn">
                  {result.categoria.toUpperCase()}
                </div>
              </div>
            </div>

            {result.keywords.length > 0 && (
              <div className="mt-6">
                <span className="font-mono text-xs tracking-wide text-muted">PALABRAS CLAVE</span>
                <div className="mt-2 flex flex-wrap gap-2">
                  {result.keywords.map((kw) => (
                    <span
                      key={kw}
                      className="rounded-md border border-border bg-panel-2 px-3 py-1 font-mono text-xs text-gray-300"
                    >
                      {kw}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </section>
    </div>
  );
}
