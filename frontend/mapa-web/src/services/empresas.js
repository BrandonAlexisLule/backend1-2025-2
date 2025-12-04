import axios from "axios";

const API_URL = "http://127.0.0.1:5000/api";

//Función que va a buscar y devolver los datos
export const buscarEmpresas = async (municipio, id_actividad) => {
  const params = {};

  if (municipio) params.municipio = municipio;
  if (id_actividad) params.id_actividad = id_actividad;

  const respuesta = await axios.get(`${API_URL}/empresas`, { params });
  return respuesta.data;
};

export const detalleEmpresa = async (id) => {
  const respuesta = await axios.get(`${API_URL}/empresas/${id}`);
  return respuesta.data;
};
