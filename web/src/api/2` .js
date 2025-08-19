import axios from "axios";
const BASE_URL = "http://parole.pythonanywhere.com/api";

export const getAnalytics = () => axios.get(`${BASE_URL}/analytics/`);
