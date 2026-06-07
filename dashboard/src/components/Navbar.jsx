export default function Navbar({ liveMode, onToggleLive }) {
  const now = new Date().toUTCString().slice(0, 25);

  return (
    <nav style={{
      background: "linear-gradient(90deg, #0a0e1a 0%, #0f1e35 100%)",
      borderBottom: "1px solid #1e3a5f",
      padding: "0 24px",
      height: 60,
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      position: "sticky",
      top: 0,
      zIndex: 1000,
    }}>
      {/* Left */}
      <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
        <div style={{
          width: 36, height: 36,
          background: "radial-gradient(circle, #00ff8820, #00ff8805)",
          border: "1px solid #00ff88",
          borderRadius: "50%",
          display: "flex", alignItems: "center", justifyContent: "center",
          fontSize: 18,
        }}>✈</div>
        <div>
          <div style={{ color: "#00ff88", fontWeight: 700, fontSize: 15, letterSpacing: 1 }}>
            Optimisation de Séquencement des Atterrissages
          </div>
          <div style={{ color: "#64748b", fontSize: 11 }}>
            Aéroport Hassan I — Laâyoune
          </div>
        </div>
      </div>

      {/* Center */}
      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <div style={{
          width: 8, height: 8, borderRadius: "50%",
          background: liveMode ? "#00ff88" : "#64748b",
        }} className={liveMode ? "radar-pulse" : ""} />
        <span style={{ color: liveMode ? "#00ff88" : "#64748b", fontSize: 12, letterSpacing: 2 }}>
          {liveMode ? "LIVE" : "STATIC"}
        </span>
      </div>

      {/* Right */}
      <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
        <span style={{ color: "#475569", fontSize: 12, fontFamily: "monospace" }}>
          UTC {now}
        </span>
        <button onClick={onToggleLive} style={{
          background: liveMode
            ? "linear-gradient(135deg, #7f1d1d, #991b1b)"
            : "linear-gradient(135deg, #064e3b, #065f46)",
          border: `1px solid ${liveMode ? "#ef4444" : "#00ff88"}`,
          color: liveMode ? "#ef4444" : "#00ff88",
          padding: "6px 16px",
          borderRadius: 6,
          fontSize: 12,
          fontWeight: 700,
          cursor: "pointer",
          letterSpacing: 1,
        }}>
          {liveMode ? "■ STOP" : "▶ LIVE"}
        </button>
      </div>
    </nav>
  );
}