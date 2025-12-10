import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import axios from "axios";
import "leaflet/dist/leaflet.css";

// Icono de marcador
const iconoEmpresa = new L.Icon({
  iconUrl: "https://cdn-icons-png.flaticon.com/512/684/684908.png",
  iconSize: [30, 30],
  iconAnchor: [15, 30],
  popupAnchor: [0, -30],
});

function App() {
  const [empresas, setEmpresas] = useState([]);
  const [municipios, setMunicipios] = useState([]);
  const [actividades, setActividades] = useState([]);
  const [filtroMunicipio, setFiltroMunicipio] = useState("");
  const [filtroActividad, setFiltroActividad] = useState("");

  const centroBC = [30.8406, -115.2837]; // Coordenadas de Baja California
  const zoomBC = 6;

  // Cargar datos al inicio
  useEffect(() => {
    async function cargarDatos() {
      try {
        const res = await axios.get("http://localhost:5000/denue_inegi/consultarEmpresas");
        const datos = res.data;
        setEmpresas(datos);

        const municipiosUnicos = [...new Set(datos.map(e => e.municipio))];
        setMunicipios(municipiosUnicos);

        const actividadesUnicas = [...new Set(datos.map(e => JSON.stringify({ nombre: e.nombre_act, codigo: e.codigo_act })))]
          .map(a => JSON.parse(a));
        setActividades(actividadesUnicas);

      } catch (error) {
        console.error("Error cargando datos:", error);
      }
    }
    cargarDatos();
  }, []);

  const buscarEmpresas = async () => {
    try {
      const params = {};
      if (filtroMunicipio) params.municipio = filtroMunicipio;
      if (filtroActividad) params.id_actividad = filtroActividad;

      const res = await axios.get("http://localhost:5000/denue_inegi/consultarEmpresas", { params });
      setEmpresas(res.data);
    } catch (error) {
      console.error("Error buscando empresas:", error);
      setEmpresas([]);
    }
  };

  return (
    <div style={{ width: "100%", height: "100%", display: "flex", flexDirection: "column" }}>
      
      {/* Contenedor de filtros */}
      <div style={{
        display: "flex",
        gap: "15px",
        padding: "10px",
        backgroundColor: "#e5e5e5",
        boxShadow: "0px 2px 8px rgba(0,0,0,0.2)",
        alignItems: "center"
      }}>

      <div>
        <label>Municipio: </label>
        <select
          className="filtros"
          value={filtroMunicipio}
          onChange={e => setFiltroMunicipio(e.target.value)}
        >
          <option value="">Todos</option>
          {municipios.map((m, i) => (
            <option key={i} value={m}>{m}</option>
          ))}
        </select>
      </div>

      <div>
        <label>Actividad: </label>
        <select
          className="filtros select-actividad"
          value={filtroActividad}
          onChange={e => setFiltroActividad(e.target.value)}
        >
          <option value="">Todas</option>
          {actividades.map((a, i) => (
            <option key={i} value={a.codigo}>{a.nombre}</option>
          ))}
        </select>
      </div>
        <div>
          <button className="boton-Buscar" onClick={buscarEmpresas} >Buscar</button>
        </div>
      </div>

      {/* Mapa ocupa 70-75% de la pantalla */}
      <div style={{ flexGrow: 1 }}>
        <MapContainer center={centroBC} zoom={zoomBC} scrollWheelZoom={true} style={{ width: "100%", height: "100%" }}>
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          />
          {empresas.map(e => (
            <Marker key={e.id} position={[e.latitud, e.longitud]} icon={iconoEmpresa}>
              <Popup>
                <strong>{e.nom_estab}</strong><br />
                {e.nombre_act}<br />
                {e.municipio}
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}

export default App;
