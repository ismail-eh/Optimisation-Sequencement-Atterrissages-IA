export default function MetricsCards({ metrics, flightCount }) {
    const cards = [
        { label: "VOLS EN APPROCHE", value: flightCount || 0, unit: "AC", color: "#00d4ff", icon: "✈" },
        { label: "TOTAL ATTENTE", value: metrics?.total_wait_min ?? "-", unit: "MIN", color: "#00ff88", icon: "⏱" },
        { label: "MOY ATTENTE", value: metrics?.avg_wait_min ?? "-", unit: "MIN", color: "#00ff88", icon: "📊" },
        { label: "SÉPARATION MIN", value: metrics?.min_separation ?? "-", unit: "MIN", color: "#00d4ff", icon: "↔" },
    ];

    return (
        <div style={{
            display: "grid",
            gridTemplateColumns: "repeat(4, 1fr)",
            gap: 12,
            padding: "0 24px 16px",
        }}>
            {cards.map(card => (
                <div key={card.label} style={{
                    background: "#111827",
                    border: "1px solid #1e3a5f",
                    borderRadius: 10,
                    padding: "16px 20px",
                    position: "relative",
                    overflow: "hidden",
                }}>
                    <div style={{
                        position: "absolute", top: 0, left: 0, right: 0, height: 2,
                        background: `linear-gradient(90deg, ${card.color}, transparent)`,
                    }} />
                    <div style={{ color: "#475569", fontSize: 10, letterSpacing: 2, marginBottom: 8 }}>
                        {card.icon} {card.label}
                    </div>
                    <div style={{ display: "flex", alignItems: "baseline", gap: 6 }}>
                        <span style={{ color: card.color, fontSize: 28, fontWeight: 700, fontFamily: "monospace" }}>
                            {typeof card.value === "number" ? card.value.toFixed(2) : card.value}
                        </span>
                        <span style={{ color: "#475569", fontSize: 12 }}>{card.unit}</span>
                    </div>
                </div>
            ))}
        </div>
    );
}