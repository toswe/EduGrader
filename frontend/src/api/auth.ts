import { axiosInstance } from "./api";
import { getRefreshToken } from "../auth/util";

export const login = async (username: string, password: string) =>
  axiosInstance.post("token/", { username, password }).then((response) => {
    const bearer = `Bearer ${response.data.access}`;
    axiosInstance.defaults.headers["Authorization"] = bearer;
    return response;
  });

export const logout = async () => {
  axiosInstance.post("logout/", { refresh: getRefreshToken() }).then(() => {
    delete axiosInstance.defaults.headers["Authorization"];
  });
};
