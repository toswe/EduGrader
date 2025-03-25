import axios from "axios";

import { getAccessToken } from "../auth/util";

const axiosInstance = axios.create({
  baseURL: `/api`,
  headers: {
    "Content-Type": "application/json",
  },
});

axiosInstance.interceptors.request.use((config) => {
  const accessToken = getAccessToken();
  if (accessToken) {
    config.headers["Authorization"] = `Bearer ${accessToken}`;
  }
  return config;
});

export default axiosInstance;
