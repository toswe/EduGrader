import axiosInstance from "./api";

export const fetchHome = async () => axiosInstance.get("home/");
