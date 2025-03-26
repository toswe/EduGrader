import { createContext, useContext, useState } from "react";
import { Navigate, Outlet } from "react-router";
import { getUserFromStorage, removeTokens, storeTokens } from "./util";

import {
  login as makeLoginRequest,
  logout as makeLogoutRequest,
} from "../api/auth";

const AuthContext = createContext({
  user: getUserFromStorage(),
  login: (_username: string, _password: string) => {},
  logout: () => {},
});

export const AuthData = () => useContext(AuthContext);

export const ProtectedRoutes = () => {
  const { user } = AuthData();
  return user.isAuthenticated ? <Outlet /> : <Navigate to="/login" />;
};

export const AuthWrapper = (props: any) => {
  const [user, setUser] = useState(getUserFromStorage());

  const login = (username: string, password: string) => {
    return makeLoginRequest(username, password).then((response) => {
      storeTokens(response);
      setUser(getUserFromStorage());
    });
  };

  const logout = () => {
    makeLogoutRequest().then(() => {
      removeTokens();
      setUser(getUserFromStorage());
    });
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {props.children}
    </AuthContext.Provider>
  );
};
