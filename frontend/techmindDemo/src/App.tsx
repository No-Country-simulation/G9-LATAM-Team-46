function App() {
  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <div className="flex w-full max-w-4xl gap-4">
        {/* Chat */}
        <div className="flex-1 flex flex-col rounded-2xl border border-white/5 bg-slate-900/60 shadow-xl backdrop-blur-sm">
          <div className="flex-1 px-6 py-8">
            <p className="text-sm text-slate-500">No hay mensajes todavía.</p>
          </div>

          <div className="border-t border-white/5 p-4">
            <input
              type="text"
              placeholder="Escribe un mensaje..."
              className="w-full rounded-lg bg-slate-800/80 px-4 py-2.5 text-sm text-slate-200 placeholder:text-slate-500 outline-none ring-1 ring-white/5 focus:ring-2 focus:ring-indigo-500 transition-shadow"
            />
          </div>
        </div>

        {/* Menú */}
        <aside className="w-56 shrink-0 rounded-2xl border border-white/5 bg-slate-900/60 p-4 shadow-xl backdrop-blur-sm">
          <h2 className="text-xs font-semibold uppercase tracking-wide text-slate-400 mb-3">
            Menú
          </h2>
          <nav className="flex flex-col gap-1">
            <button className="text-left text-sm text-slate-300 rounded-md px-2.5 py-1.5 hover:bg-white/5 transition-colors">
              Nueva conversación
            </button>
            <button className="text-left text-sm text-slate-300 rounded-md px-2.5 py-1.5 hover:bg-white/5 transition-colors">
              Historial
            </button>
            <button className="text-left text-sm text-slate-300 rounded-md px-2.5 py-1.5 hover:bg-white/5 transition-colors">
              Ajustes
            </button>
          </nav>
        </aside>
      </div>
    </div>
  )
}

export default App