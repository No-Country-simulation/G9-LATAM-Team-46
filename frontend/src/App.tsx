import { useState } from "react";
import Navbar, { type Tab } from "./components/Navbar";
import LibraryPage from "./pages/LibraryPage";
import HistoryPage from "./pages/HistoryPage";
import ChatPage from "./pages/ChatPage";
import AccountPage from "./pages/AccountPage";
import type { ClassifyResult } from "./types";

export default function App() {
  const [tab, setTab] = useState<Tab>("library");
  // Clasificación elegida en History para volver a mostrarla en Library.
  const [viewedResult, setViewedResult] = useState<ClassifyResult | null>(null);

  function handleView(result: ClassifyResult) {
    setViewedResult({ ...result });
    setTab("library");
  }

  return (
    <div className="flex h-screen flex-col bg-base">
      <Navbar active={tab} onChange={setTab} />
      {/* Chat maneja su propio scroll interno; el resto se desplaza como bloque */}
      <main className={`flex-1 ${tab === "chat" ? "overflow-hidden" : "overflow-y-auto"}`}>
        {tab === "library" && <LibraryPage presetResult={viewedResult} />}
        {tab === "history" && <HistoryPage onView={handleView} />}
        {tab === "chat" && <ChatPage />}
        {tab === "account" && <AccountPage />}
      </main>
    </div>
  );
}
