import { useState } from "react";
import { buscarEmpresas } from "../services/empresas";
import MapaEstablecimientos from "./MapaEstablecimientos";

const Busqueda = () => {
  const [municipio, setMunicipio] = useState("");
  const [actividad, setActividad] = useState("");
  const [empresas, setEmpresas] = useState([]);

  const hacerBusqueda = async () => {
    const datos = await buscarEmpresas(municipio, actividad);
    console.log(datos)
    setEmpresas(datos);
  };

  return (
    <div>
      <h1>Buscar establecimientos</h1>

      <div>
        <input
          type="text"
          placeholder="Municipio"
          value={municipio}
          onChange={(e) => setMunicipio(e.target.value)}
        />

        <input
          type="text"
          placeholder="Actividad"
          value={actividad}
          onChange={(e) => setActividad(e.target.value)}
        />

        <button onClick={hacerBusqueda}>Buscar</button>
      </div>

      <MapaEstablecimientos empresas={empresas} />
    </div>
  );
};

export default Busqueda;
