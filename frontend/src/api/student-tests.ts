import axiosInstance from "./api";
import snakecaseKeys from "snakecase-keys";
import camelcaseKeys from "camelcase-keys";
import { ITest, IStudentTest } from "../types";

export const fetchUpcomingTests = async (): Promise<ITest[]> => {
  return axiosInstance.get(`/upcoming-tests/`).then((res) => res.data);
};

export const fetchStudentTests = async (
  params: { test?: number; course?: number } = {}
): Promise<IStudentTest[]> => {
  return axiosInstance
    .get(`/student-tests/`, { params })
    .then((res) => res.data);
};

export const createStudentTest = async (test: IStudentTest) => {
  return axiosInstance
    .post(`/student-tests/`, snakecaseKeys({ ...test }, { deep: true }))
    .then((res) => camelcaseKeys(res.data, { deep: true, lowercase: true }));
};

export const fetchStudentTest = async (id: number): Promise<IStudentTest> => {
  return axiosInstance.get(`/student-tests/${id}/`).then((res) => res.data);
};
