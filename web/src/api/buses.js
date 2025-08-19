import axios from 'axios';
const BASE_URL = 'http://parole.pythonanywhere.com/api';

export const getBuses = () => axios.get(`${BASE_URL}/buses/`);
export const addBus = (data) => axios.post(`${BASE_URL}/buses/`, data);
export const updateBus = (id, data) => axios.put(`${BASE_URL}/buses/${id}/`, data);
export const deleteBus = (id) => axios.delete(`${BASE_URL}/buses/${id}/`);
export const publishBus = (id, publish) => axios.patch(`${BASE_URL}/buses/${id}/`, { published: publish });