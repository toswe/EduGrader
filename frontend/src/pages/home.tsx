import { useState, useEffect } from "react";
import { Link } from "react-router";

import { AuthData } from "../auth/AuthWrapper";
import { fetchHome } from "../api/home";
import { fetchCourses } from "../api/courses";
import { ICourse } from "../types";

export const Home = () => {
  const { user, logout } = AuthData();

  const [homeDetails, setHomeDetails] = useState("");
  const [courses, setCourses] = useState<ICourse[]>([]);

  const fetchDetails = async () => {
    fetchHome().then((response) => setHomeDetails(response.data?.message));
  };

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
        <button onClick={fetchDetails}> Fetch details </button>
      </div>
      <div> {homeDetails} </div>
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
