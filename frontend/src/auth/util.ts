import { jwtDecode } from "jwt-decode";

interface JwtPayload {
  user_id: string;
  username: string;
}
const emptyUser = { username: "", isAuthenticated: false };

export const storeTokens = (response: any) => {
  sessionStorage.setItem("accessToken", response.data.access);
  sessionStorage.setItem("refreshToken", response.data.refresh);
};

export const removeTokens = () => {
  sessionStorage.removeItem("accessToken");
  sessionStorage.removeItem("refreshToken");
};

export const getUserFromStorage = () => {
  const token = sessionStorage.getItem("accessToken");

  if (!token) return { ...emptyUser };

  const { username } = jwtDecode(token) as JwtPayload;
  return { username, isAuthenticated: true };
};

export const getRefreshToken = () => {
  return sessionStorage.getItem("refreshToken");
};
