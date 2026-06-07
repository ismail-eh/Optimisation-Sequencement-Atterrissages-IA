export default function AlertBanner({ flights }) {
  const alerts = flights.filter(f =>
    ["EMERGENCY", "RADIO_FAIL", "FUEL_CRITICAL"].includes(f.priority)
  );

  if (alerts.length === 0) return null;

  const config = {
    EMERGENCY:     { color: "#ef4444", bg: "#1c0a0a", icon: "🆘", label: "MAYDAY" },
    RADIO_FAIL:    { color: "#f97316", bg: "#1c0f0a", icon: "📡", label: "RADIO FAIL" },
    FUEL_CRITICAL: { color: "#eab308", bg: "#1c1a0a", icon: "⛽", label: "FUEL CRITICAL" },
  };

  return (
    <div style={{ padding: "0 24px 12px" }}>
      {alerts.map(f => {
        const c = config[f.priority];
        return (
          <div key={f.flight_id} className="blink" style={{
            background: c.bg,
            border: `1px solid ${c.color}`,
            borderLeft: `4px solid ${c.color}`,
            borderRadius: 8,
            padding: "10px 16px",
            marginBottom: 8,
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <span style={{ fontSize: 18 }}>{c.icon}</span>
              <div>
                <span style={{ color: c.color, fontWeight: 700, fontSize: 13, letterSpacing: 1 }}>
                  {c.label}
                </span>
                <span style={{ color: "#94a3b8", fontSize: 13, marginLeft: 12 }}>
                  {f.callsign} — {f.aircraft_type}
                </span>
              </div>
            </div>
            <div style={{ color: "#94a3b8", fontSize: 12, fontFamily: "monospace" }}>
              ETA {f.eta_min?.toFixed(1)} MIN
            </div>
          </div>
        );
      })}
    </div>
  );
}