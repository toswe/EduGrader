import { useState, useEffect } from "react";
import { Link } from "react-router";

import { AuthData } from "../../auth/AuthWrapper";
import { fetchCourses } from "../../api/courses";
import { ICourse } from "../../types";

export const HomePage = () => {
  const { user, logout } = AuthData();

  const [courses, setCourses] = useState<ICourse[]>([]);
  useEffect(() => {
    fetchCourses().then((data) => {
      setCourses(data);
    });
  }, []);

  return (
    <>
      <div> Hello, {user.username} </div>
      <br />
      <div>
        <button onClick={logout}> logout </button>
      </div>
      <br />
      <div>
        {courses.map((course: any) => (
          <div key={course.id}>
            <Link to={`/course/${course.id}`}>{course.name}</Link>
          </div>
        ))}
      </div>
    </>
  );
};
