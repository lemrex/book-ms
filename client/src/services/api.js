// src/services/api.js
import axios from 'axios';
import dotenv from 'dotenv';

// Load environment variables from the .env file
dotenv.config();

console.log('Login API Base URL:', process.env.LOGIN_API_BASE_URL);
console.log('Other API Base URL:', process.env.OTHER_API_BASE_URL);

// // Axios instance for login
// const loginApi = axios.create({
//   baseURL: process.env.LOGIN_API_BASE_URL, // Base URL for login
// });

// // Axios instance for other API calls
// const api = axios.create({
//   baseURL: process.env.OTHER_API_BASE_URL, // Base URL for all other endpoints
// });

// Axios instance for login
const loginApi = axios.create({
    baseURL: 'http://localhost:3000', // Base URL for login
  });
  
  // Axios instance for other API calls
  const api = axios.create({
    baseURL: 'http://localhost:3001', // Base URL for all other endpoints
  });

// Interceptor to add token to other API requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const register = async (username, password) => {
  const response = await loginApi.post('/auth/register', { username, password });
  return response.data;
};

// Function for login (using loginApi instance)
export const login = async (username, password) => {
  const response = await loginApi.post('/auth/login', { username, password });
  return response.data.token;
};

// Function for getting books (using api instance)
export const getBooks = async () => {
  const response = await api.get('/books');
  return response.data;
};

// Function for adding a book (using api instance)
export const addBook = async (bookData) => {
  const response = await api.post('/books', bookData);
  return response.data;
};
