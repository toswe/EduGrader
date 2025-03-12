import { createContext, useContext, useState } from "react";
import { Navigate, Outlet } from "react-router";

const AuthContext = createContext({
  user: { name: "", isAuthenticated: false },
  login: (name: string, password: string) => {},
  logout: () => {},
});

export const AuthData = () => useContext(AuthContext);

export const ProtectedRoutes = () => {
  const { user } = AuthData();
  return user.isAuthenticated ? <Outlet /> : <Navigate to="/login" />;
};

export const AuthWrapper = (props: any) => {
  const emptyUser = { name: "", isAuthenticated: false };
  const [user, setUser] = useState({ ...emptyUser });

  const login = (userName: string, password: string) => {
    return new Promise((resolve, reject) => {
      if (password === "password") {
        setUser({ name: userName, isAuthenticated: true });
        resolve("success");
      } else {
        reject("Incorrect password");
      }
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
