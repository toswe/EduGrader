import { createContext, useContext, useState } from "react";
import { Navigate, Outlet } from "react-router";
import { jwtDecode } from "jwt-decode";

import { login as loginApi } from "../api/auth";

interface JwtPayload {
  user_id: string;
  username: string;
}
const emptyUser = { username: "", isAuthenticated: false };

const AuthContext = createContext({
  user: { ...emptyUser },
  login: (username: string, password: string) => {},
  logout: () => {},
});

export const AuthData = () => useContext(AuthContext);

export const ProtectedRoutes = () => {
  const { user } = AuthData();
  return user.isAuthenticated ? <Outlet /> : <Navigate to="/login" />;
};

const storeTokens = (response: any) => {
  sessionStorage.setItem("accessToken", response.data.access);
  sessionStorage.setItem("refreshToken", response.data.refresh);
};

const getUserFromAccessToken = () => {
  const token = sessionStorage.getItem("accessToken");

  if (!token) return { ...emptyUser };

  const { username } = jwtDecode(token) as JwtPayload;
  return { username, isAuthenticated: true };
};

export const AuthWrapper = (props: any) => {
  const [user, setUser] = useState(getUserFromAccessToken());

  const login = (username: string, password: string) => {
    return loginApi(username, password).then((response) => {
      storeTokens(response);
      setUser(getUserFromAccessToken());
    });
  };

  const logout = () => {
    setUser({ ...emptyUser });
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {props.children}
    </AuthContext.Provider>
  );
};
