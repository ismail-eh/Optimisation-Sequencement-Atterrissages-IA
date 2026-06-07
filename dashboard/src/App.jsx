import { useState, useEffect, useRef } from "react";
import { getFlights, getSequence } from "./services/api";
import Navbar from "./components/Navbar";
import AlertBanner from "./components/AlertBanner";
import MetricsCards from "./components/MetricsCards";
import RadarMap from "./components/RadarMap";
import SequenceTable from "./components/SequenceTable";

const SCENARIOS  = ["normal", "dense", "emergency"];
const ALGORITHMS = ["greedy", "genetic", "fcfs"];

export default function App() {
  const [scenario,  setScenario]  = useState("normal");
  const [algorithm, setAlgorithm] = useState("greedy");
  const [flights,   setFlights]   = useState([]);
  const [sequence,  setSequence]  = useState([]);
  const [metrics,   setMetrics]   = useState(null);
  const [loading,   setLoading]   = useState(false);
  const [liveMode,  setLiveMode]  = useState(false);
  const wsRef = useRef(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [f, s] = await Promise.all([
        getFlights(scenario),
        getSequence(scenario, algorithm),
      ]);
      setFlights(f.flights);
      setSequence(s.sequence);
      setMetrics(s.metrics);
    } catch (e) {
      console.error("API error:", e);
    }
    setLoading(false);
  };

  useEffect(() => { fetchData(); }, [scenario, algorithm]);

  useEffect(() => {
    if (liveMode) {
      wsRef.current = new WebSocket("ws://localhost:8000/ws/live");
      wsRef.current.onmessage = (e) => {
        const data = JSON.parse(e.data);
        setFlights(data.flights);
        setSequence(data.sequence);
        setMetrics(data.metrics);
      };
      wsRef.current.onerror = () => setLiveMode(false);
    } else {
      wsRef.current?.close();
    }
    return () => wsRef.current?.close();
  }, [liveMode]);

  return (
    <div style={{ minHeight: "100vh", background: "#0a0e1a" }}>
      <Navbar liveMode={liveMode} onToggleLive={() => setLiveMode(!liveMode)} />

      {/* Controls */}
      <div style={{
        padding: "16px 24px",
        display: "flex",
        alignItems: "center",
        gap: 16,
        borderBottom: "1px solid #1e3a5f22",
      }}>
        <div>
          <label style={{ color: "#475569", fontSize: 10, letterSpacing: 2, display: "block", marginBottom: 6 }}>
            SCÉNARIO
          </label>
          <select value={scenario} onChange={e => setScenario(e.target.value)} style={{
            background: "#111827", border: "1px solid #1e3a5f",
            color: "#e2e8f0", padding: "8px 14px",
            borderRadius: 6, fontSize: 13, cursor: "pointer",
          }}>
            {SCENARIOS.map(s => <option key={s} value={s}>{s.toUpperCase()}</option>)}
          </select>
        </div>

        <div>
          <label style={{ color: "#475569", fontSize: 10, letterSpacing: 2, display: "block", marginBottom: 6 }}>
            ALGORITHME
          </label>
          <select value={algorithm} onChange={e => setAlgorithm(e.target.value)} style={{
            background: "#111827", border: "1px solid #1e3a5f",
            color: "#e2e8f0", padding: "8px 14px",
            borderRadius: 6, fontSize: 13, cursor: "pointer",
          }}>
            {ALGORITHMS.map(a => <option key={a} value={a}>{a.toUpperCase()}</option>)}
          </select>
        </div>

        <div style={{ marginTop: 20 }}>
          <button onClick={fetchData} style={{
            background: loading ? "#1e3a5f" : "linear-gradient(135deg, #064e3b, #065f46)",
            border: "1px solid #00ff88",
            color: "#00ff88",
            padding: "8px 20px",
            borderRadius: 6,
            fontSize: 13,
            fontWeight: 700,
            cursor: "pointer",
            letterSpacing: 1,
          }}>
            {loading ? "⟳ LOADING..." : "⟳ REFRESH"}
          </button>
        </div>

        {/* Status */}
        <div style={{ marginLeft: "auto", display: "flex", gap: 20 }}>
          {[
            { label: "ALGORITHME", value: algorithm.toUpperCase(), color: "#00ff88" },
            { label: "SCÉNARIO",   value: scenario.toUpperCase(),  color: "#00d4ff" },
            { label: "VOLS",       value: flights.length,          color: "#eab308" },
          ].map(s => (
            <div key={s.label} style={{ textAlign: "right" }}>
              <div style={{ color: "#475569", fontSize: 10, letterSpacing: 1 }}>{s.label}</div>
              <div style={{ color: s.color, fontSize: 14, fontWeight: 700, fontFamily: "monospace" }}>
                {s.value}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Alerts */}
      <div style={{ paddingTop: 12 }}>
        <AlertBanner flights={flights} />
      </div>

      {/* Metrics */}
      <MetricsCards metrics={metrics} flightCount={flights.length} />

      {/* Radar Map */}
      <RadarMap flights={flights} />

      {/* Sequence Table */}
      <SequenceTable sequence={sequence} algorithm={algorithm} />

      {/* Footer */}
      <div style={{
        textAlign: "center",
        padding: "20px 24px",
        color: "#1e3a5f",
        fontSize: 11,
        letterSpacing: 1,
        borderTop: "1px solid #1e3a5f33",
      }}>
        ONDA — Service Technique de Navigation Aérienne · Aéroport Hassan I — Laâyoune
      </div>
    </div>
  );
}