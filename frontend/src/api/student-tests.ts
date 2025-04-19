import axiosInstance from "./api";
import { ITest, IStudentTest } from "../types";

export const fetchUpcomingTests = async (): Promise<ITest[]> => {
  return axiosInstance.get(`/upcoming-tests/`).then((res) => res.data);
};

export const fetchStudentTests = async (): Promise<IStudentTest[]> => {
  return axiosInstance.get(`/student-tests/`).then((res) => res.data);
};

export const createStudentTest = async (test: IStudentTest) => {
  return axiosInstance.post(`/student-tests/`, test).then((res) => res.data);
};
