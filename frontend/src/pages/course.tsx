import { useEffect, useState } from "react";
import { useParams } from "react-router";

import { fetchCourse } from "../api/courses";
import { ICourse } from "../types";

export const Course = () => {
  const { courseId } = useParams();
  const [course, setCourse] = useState<ICourse | null>(null);

  useEffect(() => {
    if (courseId) {
      fetchCourse(Number(courseId)).then((data) => {
        setCourse(data);
      });
    }
  }, []);

  return (
    <>
      <div>
        <h3>{course?.name} </h3>
      </div>
    </>
  );
};
