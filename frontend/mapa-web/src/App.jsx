import React from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "./App.css";

const iconEmpresa = new L.Icon({
  iconUrl: "/marcador.png", // Debe existir en public
  iconSize: [30, 30],
  iconAnchor: [15, 30],
  popupAnchor: [0, -30],
});

function App() {
  const centerBC = [30.8406, -115.2838];

  return (
    <div className="app-container">
      <h2 style={{ textAlign: "center" }}>Mapa de prueba Baja California</h2>
      <MapContainer center={centerBC} zoom={7} className="mapa">
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; OpenStreetMap'
        />
        <Marker position={centerBC} icon={iconEmpresa}>
          <Popup>Marcador de prueba en BC</Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}

export default App;
