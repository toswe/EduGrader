import axiosInstance from "./api";
import { ICourse } from "../types";

export const fetchCourses = async (): Promise<ICourse[]> => {
  return axiosInstance.get("courses/").then((res) => res.data);
};

export const fetchCourse = async (courseId: number): Promise<ICourse> =>
  axiosInstance.get(`courses/${courseId}/`).then((res) => res.data);
