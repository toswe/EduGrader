import axiosInstance from "./api";
import camelcaseKeys from "camelcase-keys";

import { IStudentAnswer } from "../types";

export const updateStudentAnswerScore = async (
  answerId: number,
  score: number
): Promise<IStudentAnswer> => {
  return axiosInstance
    .patch(`/student-answers/${answerId}/`, { score })
    .then((res) => camelcaseKeys(res.data, { deep: true, lowercase: true }));
};
