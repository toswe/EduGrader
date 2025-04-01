import axiosInstance from "./api";

import { ITest } from "../types";

export const fetchTests = async (courseId: number): Promise<ITest[]> => {
  return axiosInstance
    .get(`courses/${courseId}/tests/`)
    .then((res) => res.data);
};

export const createTest = async (
  courseId: number,
  name: string,
  questions: number[]
): Promise<ITest> => {
  return axiosInstance
    .post(`courses/${courseId}/tests/`, { name, questions })
    .then((res) => res.data);
};

export const fetchTest = async (testId: number): Promise<ITest> => {
  return axiosInstance.get(`/tests/${testId}/`).then((res) => res.data);
};

export const updateTest = async (
  testId: number,
  name: string,
  questions: number[]
): Promise<ITest> => {
  return axiosInstance
    .put(`/tests/${testId}/`, { name, questions })
    .then((res) => res.data);
};
