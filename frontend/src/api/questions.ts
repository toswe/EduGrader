import axiosInstance from "./api";

import { IQuestion } from "../types";

export const fetchQuestions = async (
  courseId: number
): Promise<IQuestion[]> => {
  return axiosInstance
    .get(`courses/${courseId}/questions/`)
    .then((res) => res.data);
};
