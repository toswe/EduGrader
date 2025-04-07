import axiosInstance from "./api";
import { IStudentTest } from "../types";

export const fetchStudentTests = async (): Promise<IStudentTest[]> => {
  return axiosInstance.get(`/student-tests/`).then((res) => res.data);
};
