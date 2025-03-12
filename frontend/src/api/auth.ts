import { axiosInstance } from "./api";

export const login = async (username: string, password: string) =>
  axiosInstance.post("token/", { username, password });
