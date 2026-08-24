import { useEffect, useState } from "react";
import { classifyContent, getEjemplos, getSugerencia } from "../lib/api";
import { getClassifications, saveClassification } from "../lib/storage";
import ConfidenceRing from "../components/ConfidenceRing";
import type { ClassifyResult, EjemploUso } from "../types";

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
  const [ejemplos, setEjemplos] = useState<EjemploUso[]>([]);
  const [loadingSugerencia, setLoadingSugerencia] = useState(false);

  // Ejemplos reales para los chips. Si falla (backend caído, endpoint no
  // disponible), simplemente no se muestran — no es un flujo crítico.
  useEffect(() => {
    getEjemplos()
      .then(setEjemplos)
      .catch(() => setEjemplos([]));
  }, []);

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

  async function classify(tituloVal: string, textoVal: string) {
    if (!textoVal.trim()) return;
    setLoading(true);
    setError(null);
    setViewingSaved(false);
    try {
      const data = await classifyContent(tituloVal, textoVal);
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

  function handleSubmit() {
    classify(titulo, texto);
  }

  function handleEjemploClick(ejemplo: EjemploUso) {
    setTitulo(ejemplo.titulo);
    setTexto(ejemplo.texto);
    classify(ejemplo.titulo, ejemplo.texto);
  }

  // No hay endpoint de detalle para un contenido relacionado: se reenvía su
  // título como una nueva consulta a POST /contenido.
  function handleRelacionadoClick(tituloRelacionado: string) {
    setTitulo(tituloRelacionado);
    setTexto(tituloRelacionado);
    classify(tituloRelacionado, tituloRelacionado);
  }

  function handleClear() {
    setTitulo("");
    setTexto("");
    setError(null);
    setViewingSaved(false);
  }

  // Solo llena los recuadros con la sugerencia — no clasifica automáticamente.
  async function handleSugerenciaClick() {
    setLoadingSugerencia(true);
    setError(null);
    try {
      const sugerencia = await getSugerencia();
      if (sugerencia) {
        setTitulo(sugerencia.titulo);
        setTexto(sugerencia.texto);
        setViewingSaved(false);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo obtener una sugerencia.");
    } finally {
      setLoadingSugerencia(false);
    }
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

        {ejemplos.length > 0 && (
          <div className="mt-4">
            <span className="font-mono text-xs tracking-wide text-muted">EJEMPLOS DE USO</span>
            <div className="mt-2 flex flex-wrap gap-2">
              {ejemplos.map((ejemplo, i) => (
                <button
                  key={`${ejemplo.titulo}-${i}`}
                  type="button"
                  onClick={() => handleEjemploClick(ejemplo)}
                  disabled={loading}
                  title={ejemplo.texto}
                  className="group flex items-center gap-1.5 rounded-full border border-border px-3 py-1 font-mono text-xs text-subtle transition-colors hover:border-accent hover:text-white disabled:opacity-50"
                >
                  {ejemplo.titulo}
                  <span className="text-muted group-hover:text-accent">· {ejemplo.categoria}</span>
                </button>
              ))}
            </div>
          </div>
        )}

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

        <button
          onClick={handleSugerenciaClick}
          disabled={loadingSugerencia}
          className="mt-3 w-full rounded-lg border border-dashed border-border px-5 py-2.5 text-sm font-semibold text-subtle transition-colors hover:border-accent hover:text-white disabled:opacity-50"
        >
          {loadingSugerencia ? "Buscando sugerencia..." : "💡 Probar con una sugerencia"}
        </button>
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

            {(result.rankingCategorias?.length ?? 0) > 0 && (
              <div className="mt-6">
                <span className="font-mono text-xs tracking-wide text-muted">
                  OTRAS CATEGORÍAS POSIBLES
                </span>
                <div className="mt-2 flex flex-col gap-1.5">
                  {(result.rankingCategorias ?? []).map((c) => (
                    <div
                      key={c.categoria}
                      className="flex items-center justify-between rounded-md border border-border bg-panel-2 px-3 py-1.5"
                    >
                      <span className="text-sm text-gray-300">{c.categoria}</span>
                      <span className="font-mono text-xs text-muted">
                        {(c.probabilidad * 100).toFixed(1)}%
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

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

            {(result.contenidosRelacionados?.length ?? 0) > 0 && (
              <div className="mt-6">
                <span className="font-mono text-xs tracking-wide text-muted">
                  CONTENIDO RELACIONADO
                </span>
                <div className="mt-2 flex flex-col gap-2">
                  {(result.contenidosRelacionados ?? []).map((rel, i) => (
                    <button
                      key={`${rel.titulo}-${i}`}
                      type="button"
                      onClick={() => handleRelacionadoClick(rel.titulo)}
                      disabled={loading}
                      className="flex w-full items-center justify-between gap-3 rounded-md border border-border bg-panel-2 px-3 py-2 text-left transition-colors hover:border-accent disabled:opacity-50"
                    >
                      <div className="min-w-0">
                        <p className="truncate text-sm text-white">{rel.titulo}</p>
                        <p className="font-mono text-xs text-muted">{rel.categoria}</p>
                      </div>
                      <span className="shrink-0 font-mono text-xs text-subtle">
                        {(rel.similitud * 100).toFixed(1)}%
                      </span>
                    </button>
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
