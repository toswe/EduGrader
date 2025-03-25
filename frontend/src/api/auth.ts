import axiosInstance from "./api";
import { getRefreshToken } from "../auth/util";

export const login = async (username: string, password: string) =>
  axiosInstance.post("token/", { username, password });

export const logout = async () =>
  axiosInstance.post("logout/", { refresh: getRefreshToken() });
