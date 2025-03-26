import axiosInstance from "./api";

import { IQuestion } from "../types";

export const fetchQuestions = async (
  courseId: number
): Promise<IQuestion[]> => {
  return axiosInstance
    .get(`courses/${courseId}/questions/`)
    .then((res) => res.data);
};

export const createQuestion = async (
  courseId: number,
  question: string,
  answer: string
): Promise<IQuestion> => {
  return axiosInstance
    .post(`courses/${courseId}/questions/`, { question, answer })
    .then((res) => res.data);
};

export const fetchQuestion = async (questionId: number): Promise<IQuestion> => {
  return axiosInstance.get(`/questions/${questionId}/`).then((res) => res.data);
};

export const updateQuestion = async (
  questionId: number,
  question: string,
  answer: string
): Promise<IQuestion> => {
  return axiosInstance
    .put(`/questions/${questionId}/`, { question, answer })
    .then((res) => res.data);
};
