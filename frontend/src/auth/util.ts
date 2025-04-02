import { jwtDecode } from "jwt-decode";

import { IJwtPayload, IUser } from "../types";

const emptyUser = { username: "", isAuthenticated: false, id: -1, type: null };

export const storeTokens = (response: any) => {
  sessionStorage.setItem("accessToken", response.data.access);
  sessionStorage.setItem("refreshToken", response.data.refresh);
};

export const removeTokens = () => {
  sessionStorage.removeItem("accessToken");
  sessionStorage.removeItem("refreshToken");
};

export const getUserFromStorage = (): IUser => {
  const token = sessionStorage.getItem("accessToken");

  if (!token) return { ...emptyUser };

  const { username, type, user_id } = jwtDecode(token) as IJwtPayload;
  return { username, type, id: Number(user_id), isAuthenticated: true };
};

export const getAccessToken = () => {
  return sessionStorage.getItem("accessToken");
};

export const getRefreshToken = () => {
  return sessionStorage.getItem("refreshToken");
};
