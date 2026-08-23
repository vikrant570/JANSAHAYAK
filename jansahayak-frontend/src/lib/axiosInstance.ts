import axios from "axios";


const url = process.env.NEXT_PUBLIC_API_BACKEND_URL
const api = axios.create({
    baseURL: url,
    withCredentials: true,
});

export default api;