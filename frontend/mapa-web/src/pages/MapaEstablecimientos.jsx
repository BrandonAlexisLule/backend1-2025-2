import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export default function MapaEstablecimientos({ empresas }) {
  if (!empresas || empresas.length === 0) {
    return <p>No hay establecimientos para mostrar.</p>;
  }

  // Centro inicial basado en la primera empresa
  const centro = [
    parseFloat(empresas[0].latitud),
    parseFloat(empresas[0].longitud),
  ];

  return (
    <div style={{ height: "500px", width: "100%", marginTop: "20px" }}>
      <MapContainer center={centro} zoom={13} style={{ height: "100%", width: "100%" }}>
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {empresas.map((e) => (
          <Marker
            key={e.id}
            position={[parseFloat(e.latitud), parseFloat(e.longitud)]}
          >
            <Popup>
              <strong>{e.nom_estab}</strong>
              <br />
              Actividad: {e.nombre_act}
              <br />
              Dirección: {e.nom_vial} {e.numero_ext}
              <br />
              Colonia: {e.nomb_asent}
              <br />
              Municipio: {e.municipio}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
