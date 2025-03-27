import axiosInstance from "./api";

import { ITest } from "../types";

export const fetchTests = async (courseId: number): Promise<ITest[]> => {
  return axiosInstance
    .get(`courses/${courseId}/tests/`)
    .then((res) => res.data);
};
