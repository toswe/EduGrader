import axios from "axios";

const PROTOCOL = "http";
const HOST = "localhost:8000";

export const axiosInstance = axios.create({
  baseURL: `${PROTOCOL}://${HOST}/`,
  headers: {
    "Content-Type": "application/json",
  },
});
