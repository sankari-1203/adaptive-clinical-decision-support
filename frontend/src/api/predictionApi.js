/**
 * API client service for Adaptive Clinical Decision Support System backend.
 */
import axios from 'axios';

const API_BASE =
  import.meta.env?.VITE_API_BASE ||
  (typeof window !== 'undefined' &&
  (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? ''
    : 'https://adaptive-clinical-decision-support.onrender.com');

const client = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getHealth = async () => {
  const response = await client.get('/api/health');
  return response.data;
};

export const getDiseases = async () => {
  const response = await client.get('/api/diseases');
  return response.data;
};

export const getModelStatus = async (disease) => {
  const response = await client.get(`/api/models/${disease}`);
  return response.data;
};

export const predictDisease = async (disease, patientData) => {
  const response = await client.post(`/api/predict/${disease}`, patientData);
  return response.data;
};
