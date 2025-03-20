import { createContext, useContext, useState } from "react";
import { Navigate, Outlet } from "react-router";
import { jwtDecode } from "jwt-decode";

import {
  login as makeLoginRequest,
  logout as makeLogoutRequest,
} from "../api/auth";

interface JwtPayload {
  user_id: string;
  username: string;
}
const emptyUser = { username: "", isAuthenticated: false };

const AuthContext = createContext({
  user: { ...emptyUser },
  login: (_username: string, _password: string) => {},
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

const removeTokens = () => {
  sessionStorage.removeItem("accessToken");
  sessionStorage.removeItem("refreshToken");
};

const getUserFromSessionStorage = () => {
  const token = sessionStorage.getItem("accessToken");

  if (!token) return { ...emptyUser };

  const { username } = jwtDecode(token) as JwtPayload;
  return { username, isAuthenticated: true };
};

export const AuthWrapper = (props: any) => {
  const [user, setUser] = useState(getUserFromSessionStorage());

  const login = (username: string, password: string) => {
    return makeLoginRequest(username, password).then((response) => {
      storeTokens(response);
      setUser(getUserFromSessionStorage());
    });
  };

  const logout = () => {
    makeLogoutRequest().then(() => {
      removeTokens();
      setUser(getUserFromSessionStorage());
    });
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {props.children}
    </AuthContext.Provider>
  );
};
