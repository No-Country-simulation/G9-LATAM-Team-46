import { getChatMessages, getClassifications } from "../lib/storage";

export default function AccountPage() {
  const classifications = getClassifications();
  const chatCount = getChatMessages().filter((m) => m.rol === "user").length;
  const avgConfidence = classifications.length
    ? classifications.reduce((sum, c) => sum + c.probabilidad, 0) / classifications.length
    : 0;

  return (
    <div className="p-4 sm:p-6">
      <section className="mx-auto max-w-xl rounded-xl border border-border bg-panel p-4 sm:p-6">
        <div className="flex items-center gap-4">
          <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-full bg-accent text-lg font-bold text-white">
            MR
          </div>
          <div>
            <h2 className="text-lg font-bold text-white">Maya Rendell</h2>
            <p className="text-sm text-subtle">maya.rendell@corvid.dev</p>
          </div>
        </div>

        <div className="mt-6 grid grid-cols-1 gap-3 xs:grid-cols-3 sm:gap-4">
          <Stat label="CLASIFICADAS" value={classifications.length} />
          <Stat label="CHATS" value={chatCount} />
          <Stat label="CONFIANZA PROM." value={`${avgConfidence.toFixed(1)}%`} />
        </div>

        <div className="mt-6 divide-y divide-border border-t border-border text-sm">
          <Row label="Proveedor" value="google-oauth" />
          <Row label="Miembro desde" value="2024-11-02" />
        </div>
      </section>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="rounded-lg border border-border bg-panel-2 p-4 text-center">
      <div className="font-mono text-2xl font-semibold text-warn">{value}</div>
      <div className="mt-1 font-mono text-[10px] tracking-wide text-muted">{label}</div>
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between py-3">
      <span className="text-subtle">{label}</span>
      <span className="text-white">{value}</span>
    </div>
  );
}
