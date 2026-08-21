import { useState, useEffect } from "react";
import { Link } from "react-router";

import { fetchCourses } from "../../api/courses";
import { ICourse } from "../../types";

export const HomePage = () => {
  const [courses, setCourses] = useState<ICourse[]>([]);
  useEffect(() => {
    fetchCourses().then((data) => {
      setCourses(data);
    });
  }, []);

  return (
    <div className="stack-lg">
      <h1>Courses</h1>
      <div className="stack">
        {courses.map((course) => (
          <div key={course.id} className="card">
            <Link to={`/course/${course.id}`}>{course.name}</Link>
          </div>
        ))}
        {courses.length === 0 && <p className="muted">No courses yet.</p>}
      </div>
    </div>
  );
};
