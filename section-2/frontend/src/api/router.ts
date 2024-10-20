// src/axiosConfig.ts

import axios from 'axios';
import { getToken, refreshToken } from './auth';



// Create an instance of axios with the baseURL from the environment variables
const api = axios.create({
  baseURL: import.meta.env.VITE_PUBLIC_URL, // Use env variable for base URL
});

// Request interceptor to add the Authorization header if the token exists
api.interceptors.request.use(
  async (config) => {
    const token = getToken();
    
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to refresh the token on 401 response
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If the error is due to an expired token and the request hasn't been retried
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Attempt to refresh the token
        const newToken = await refreshToken();
        if (newToken) {
          axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
          originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
          return api(originalRequest); // Retry the original request with the new token
        }
      } catch (error) {
        return Promise.reject(error);
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;
