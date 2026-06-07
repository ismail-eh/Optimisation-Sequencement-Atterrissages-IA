const priorityConfig = {
  EMERGENCY: { color: "#ef4444", bg: "#1c0a0a", icon: "🆘" },
  RADIO_FAIL: { color: "#f97316", bg: "#1c0f0a", icon: "📡" },
  FUEL_CRITICAL: { color: "#eab308", bg: "#1c1a0a", icon: "⛽" },
  NORMAL: { color: "#00ff88", bg: "#0a1c12", icon: "✅" },
};

const wakeColor = {
  SUPER: "#ef4444",
  HEAVY: "#f97316",
  MEDIUM: "#00d4ff",
  LIGHT: "#00ff88",
};

export default function SequenceTable({ sequence, algorithm }) {
  if (!sequence || sequence.length === 0)
    return <p style={{ color: "#475569", padding: 16 }}>Aucune séquence disponible.</p>;

  return (
    <div style={{ margin: "0 24px 16px", border: "1px solid #1e3a5f", borderRadius: 12, overflow: "hidden" }}>
      {/* Header */}
      <div style={{
        background: "#111827",
        borderBottom: "1px solid #1e3a5f",
        padding: "12px 20px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
      }}>
        <span style={{ color: "#00ff88", fontSize: 12, fontWeight: 700, letterSpacing: 2 }}>
          📋 SÉQUENCE D'ATTERRISSAGE OPTIMISÉE
        </span>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <span style={{ color: "#475569", fontSize: 11 }}>{sequence.length} vols</span>
          <span style={{
            background: "#0a1c12", border: "1px solid #00ff88",
            color: "#00ff88", padding: "2px 10px",
            borderRadius: 4, fontSize: 11, letterSpacing: 1,
          }}>
            {algorithm?.toUpperCase()}
          </span>
        </div>
      </div>

      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
        <thead>
          <tr style={{ background: "#0f172a" }}>
            {[
              { label: "#", tip: "Ordre atterrissage" },
              { label: "VOL", tip: "Indicatif" },
              { label: "TYPE", tip: "Type aéronef" },
              { label: "CAT", tip: "Catégorie ICAO" },
              { label: "WAKE", tip: "Classe turbulence" },
              { label: "ALT (FT)", tip: "Altitude actuelle" },
              { label: "SPD (KT)", tip: "Vitesse sol" },
              { label: "ETA (MIN)", tip: "Temps arrivée estimé" },
              { label: "SCHEDULÉ", tip: "Heure atterrissage planifiée" },
              { label: "ATTENTE", tip: "Délai d'attente" },
              { label: "SQUAWK", tip: "Code transpondeur" },
              { label: "PRIORITÉ", tip: "Niveau de priorité" },
            ].map(h => (
              <th key={h.label} title={h.tip} style={{
                padding: "10px 14px",
                textAlign: "left",
                color: "#475569",
                fontSize: 10,
                letterSpacing: 1.5,
                fontWeight: 600,
                borderBottom: "1px solid #1e3a5f",
                whiteSpace: "nowrap",
              }}>{h.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sequence.map((f, i) => {
            const wait = f.scheduled_eta != null ? Math.max(0, f.scheduled_eta - f.eta_min).toFixed(1) : "-";
            const pc = priorityConfig[f.priority] || priorityConfig.NORMAL;
            const isUrgent = ["EMERGENCY", "RADIO_FAIL", "FUEL_CRITICAL"].includes(f.priority);

            return (
              <tr key={f.flight_id} style={{
                background: isUrgent ? `${pc.bg}` : i % 2 === 0 ? "#111827" : "#0f172a",
                borderBottom: "1px solid #1e3a5f22",
                borderLeft: isUrgent ? `3px solid ${pc.color}` : "3px solid transparent",
              }}>
                {/* Ordre */}
                <td style={{ padding: "10px 14px", color: "#00d4ff", fontWeight: 700, fontFamily: "monospace", fontSize: 16 }}>
                  {f.sequence_pos}
                </td>
                {/* Callsign */}
                <td style={{ padding: "10px 14px", color: "#e2e8f0", fontFamily: "monospace", fontWeight: 700, fontSize: 14 }}>
                  {f.callsign}
                </td>
                {/* Type */}
                <td style={{ padding: "10px 14px", color: "#94a3b8" }}>
                  {f.aircraft_type}
                </td>
                {/* Catégorie */}
                <td style={{ padding: "10px 14px" }}>
                  <span style={{
                    background: "#1e3a5f",
                    color: "#00d4ff",
                    padding: "2px 8px",
                    borderRadius: 4,
                    fontSize: 12,
                    fontWeight: 700,
                    fontFamily: "monospace",
                  }}>
                    {f.category}
                  </span>
                </td>
                {/* Wake */}
                <td style={{ padding: "10px 14px" }}>
                  <span style={{
                    color: wakeColor[f.wake_class] || "#94a3b8",
                    fontSize: 12,
                    fontWeight: 700,
                    fontFamily: "monospace",
                  }}>
                    {f.wake_class}
                  </span>
                </td>
                {/* Altitude */}
                <td style={{ padding: "10px 14px", color: "#94a3b8", fontFamily: "monospace" }}>
                  {f.altitude_ft?.toFixed(0)}
                </td>
                {/* Speed */}
                <td style={{ padding: "10px 14px", color: "#94a3b8", fontFamily: "monospace" }}>
                  {f.speed_kt?.toFixed(0)}
                </td>
                {/* ETA */}
                <td style={{ padding: "10px 14px", color: "#e2e8f0", fontFamily: "monospace", fontWeight: 600 }}>
                  {f.eta_min?.toFixed(2)}
                </td>
                {/* Schedulé */}
                <td style={{ padding: "10px 14px", color: "#00ff88", fontFamily: "monospace", fontWeight: 700 }}>
                  {f.scheduled_eta?.toFixed(2) ?? f.eta_min?.toFixed(2)}
                </td>
                {/* Attente */}
                <td style={{ padding: "10px 14px", fontFamily: "monospace" }}>
                  <span style={{ color: parseFloat(wait) > 0 ? "#eab308" : "#00ff88", fontWeight: 600 }}>
                    {wait} MIN
                  </span>
                </td>
                {/* Squawk */}
                <td style={{ padding: "10px 14px" }}>
                  <span style={{
                    fontFamily: "monospace",
                    fontSize: 13,
                    color: f.squawk === "7700" || f.squawk === "7500" ? "#ef4444" :
                      f.squawk === "7600" ? "#f97316" : "#475569",
                    fontWeight: ["7700", "7600", "7500"].includes(f.squawk) ? 700 : 400,
                  }}>
                    {f.squawk}
                  </span>
                </td>
                {/* Priorité */}
                <td style={{ padding: "10px 14px" }}>
                  <span style={{
                    background: pc.bg,
                    border: `1px solid ${pc.color}`,
                    color: pc.color,
                    padding: "3px 8px",
                    borderRadius: 4,
                    fontSize: 10,
                    fontWeight: 700,
                    letterSpacing: 1,
                    whiteSpace: "nowrap",
                  }}>
                    {pc.icon} {f.priority}
                  </span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}