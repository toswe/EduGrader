import axios from "axios";

import { getAccessToken, removeTokens } from "../auth/util";

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

axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    // TODO Maybe remove tokens for other status codes as well
    if (error.response && error.response.status === 401) {
      removeTokens();
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
