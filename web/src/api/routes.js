import axios from "axios";
const BASE_URL = "http://parole.pythonanywhere.com/api";

export const getRoutes = () => axios.get(`${BASE_URL}/routes/`);
export const addRoute = (data) => axios.post(`${BASE_URL}/routes/`, data);
export const updateRoute = (id, data) =>
  axios.put(`${BASE_URL}/routes/${id}/`, data);
export const deleteRoute = (id) => axios.delete(`${BASE_URL}/routes/${id}/`);
export const suspendRoute = (id, suspended) =>
  axios.patch(`${BASE_URL}/routes/${id}/`, { suspended });
