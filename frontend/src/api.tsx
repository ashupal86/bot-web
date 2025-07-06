import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

export const getContainers = async () => {
  const res = await axios.get(`${API_URL}/containers`);
  console.log(res);
  return res.data.containers;
};

export const startContainer = async (id: string) => {
  const res=await axios.get(`${API_URL}/containers/${id}/start`);
  alert(res.data.message);
};

export const stopContainer = async (id: string) => {
  const res=await axios.get(`${API_URL}/containers/${id}/stop`);
  alert(res.data.message);
};

export const getLogs = async (id: string) => {
  const res = await axios.get(`${API_URL}/containers/${id}/logs`);
  return res.data.logs;
};
