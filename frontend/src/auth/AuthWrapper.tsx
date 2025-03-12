import { createContext, useContext, useState } from "react";
import { Navigate, Outlet } from "react-router";

import { login as loginApi } from "../api/auth";

const AuthContext = createContext({
  user: { username: "", isAuthenticated: false },
  login: (username: string, password: string) => {},
  logout: () => {},
});

export const AuthData = () => useContext(AuthContext);

export const ProtectedRoutes = () => {
  const { user } = AuthData();
  return user.isAuthenticated ? <Outlet /> : <Navigate to="/login" />;
};

export const AuthWrapper = (props: any) => {
  const emptyUser = { username: "", isAuthenticated: false };
  const [user, setUser] = useState({ ...emptyUser });

  const login = (username: string, password: string) => {
    return loginApi(username, password).then(() => {
      setUser({ username, isAuthenticated: true });
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
