import axiosInstance from "./api";

import { ITest, ITestQuestions } from "../types";

export const fetchTests = async (courseId: number): Promise<ITest[]> => {
  return axiosInstance
    .get(`courses/${courseId}/tests/`)
    .then((res) => res.data);
};

export const createTest = async (
  data: ITest | Omit<ITest, "id">,
): Promise<ITest> => {
  return axiosInstance
    .post(`courses/${data.course}/tests/`, data) // TODO Change this route to be more RESTful
    .then((res) => res.data);
};

export const fetchTest = async (testId: number): Promise<ITest> => {
  return axiosInstance.get(`/tests/${testId}/`).then((res) => res.data);
};

export const fetchTestWithQuestions = async (
  testId: number
): Promise<ITestQuestions> => {
  return axiosInstance
    .get(`/tests/${testId}/?full_data=true`)
    .then((res) => res.data);
};

export const updateTest = async (
  data: ITest,
): Promise<ITest> => {
  return axiosInstance
    .put(`/tests/${data.id}/`, data)
    .then((res) => res.data);
};

export const deleteTest = async (testId: number): Promise<void> => {
  return axiosInstance.delete(`/tests/${testId}/`);
};
