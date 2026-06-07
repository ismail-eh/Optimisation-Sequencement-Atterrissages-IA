import { MapContainer, TileLayer, CircleMarker, Tooltip, Circle } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const AIRPORT = { lat: 27.1518, lon: -13.4156 };

const priorityColor = {
  EMERGENCY:     "#ef4444",
  RADIO_FAIL:    "#f97316",
  FUEL_CRITICAL: "#eab308",
  NORMAL:        "#00ff88",
};

export default function RadarMap({ flights }) {
  return (
    <div style={{
      margin: "0 24px 16px",
      borderRadius: 12,
      overflow: "hidden",
      border: "1px solid #1e3a5f",
      height: 420,
      position: "relative",
    }}>
      <div style={{
        position: "absolute", top: 10, left: 10, zIndex: 1000,
        background: "#0a0e1acc",
        border: "1px solid #1e3a5f",
        borderRadius: 6,
        padding: "6px 12px",
        fontSize: 11,
        color: "#00ff88",
        letterSpacing: 1,
        fontFamily: "monospace",
      }}>
        📡 TMA LAÂYOUNE — RADIUS 50NM
      </div>

      <MapContainer
        key="radar-map"
        center={[AIRPORT.lat, AIRPORT.lon]}
        zoom={7}
        scrollWheelZoom={true}
        style={{ height: "100%", width: "100%" }}>
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          attribution="CartoDB"
        />

        {/* TMA Circle */}
        <Circle
          center={[AIRPORT.lat, AIRPORT.lon]}
          radius={92600}
          pathOptions={{ color: "#00d4ff22", fillColor: "#00d4ff05", weight: 1, dashArray: "5,5" }}
        />

        {/* Airport */}
        <CircleMarker
          center={[AIRPORT.lat, AIRPORT.lon]}
          radius={8}
          pathOptions={{ color: "#00d4ff", fillColor: "#00d4ff", fillOpacity: 1 }}>
          <Tooltip permanent direction="right">
            <span style={{ fontSize: 11, fontFamily: "monospace" }}>✈ GLMM</span>
          </Tooltip>
        </CircleMarker>

        {/* Flights */}
        {flights.map(f => (
          <CircleMarker
            key={f.flight_id}
            center={[f.lat, f.lon]}
            radius={6}
            pathOptions={{
              color: priorityColor[f.priority] || "#00ff88",
              fillColor: priorityColor[f.priority] || "#00ff88",
              fillOpacity: 0.85,
              weight: 1.5,
            }}>
            <Tooltip>
              <div style={{ fontFamily: "monospace", fontSize: 12 }}>
                <div style={{ fontWeight: 700, marginBottom: 4 }}>{f.callsign}</div>
                <div>TYPE: {f.aircraft_type}</div>
                <div>ALT: {f.altitude_ft?.toFixed(0)} FT</div>
                <div>SPD: {f.speed_kt?.toFixed(0)} KT</div>
                <div>ETA: {f.eta_min?.toFixed(1)} MIN</div>
                <div style={{ color: priorityColor[f.priority], marginTop: 4 }}>
                  {f.priority}
                </div>
              </div>
            </Tooltip>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
}