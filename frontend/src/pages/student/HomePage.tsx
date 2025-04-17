import { useEffect, useState } from "react";

import { AuthData } from "../../auth/AuthWrapper";
import { fetchUpcomingTests, fetchStudentTests } from "../../api/student-tests";
import { ITest, IStudentTest } from "../../types";
import { Link } from "react-router";

export const HomePage = () => {
  const { user, logout } = AuthData();

  const [upcomingTests, setUpcomingTests] = useState<ITest[]>([]);
  const [studentTests, setStudentTests] = useState<IStudentTest[]>([]);

  const fetchTests = () => {
    fetchUpcomingTests().then((upcomingTests) => {
      setUpcomingTests(upcomingTests);
    });

    fetchStudentTests().then((studentTests) => {
      setStudentTests(studentTests);
    });
  };

  useEffect(() => {
    fetchTests();
  }, []);

  return (
    <>
      <h1>Student Home</h1>
      <div> Hello, {user.username} </div>
      <br />
      <div>
        <button onClick={logout}> logout </button>
      </div>
      <br />
      <div>
        <h5>Upcoming Tests:</h5>
        {upcomingTests.map((test: any) => {
          return (
            <Link key={test.id} to={`/test/${test.id}`}>
              {test.name}
            </Link>
          );
        })}
      </div>
      <br />
      <div>
        <h5>Completed Tests:</h5>
        {studentTests.map((test: any) => {
          return <div key={test.id}>{test.test}</div>;
        })}
      </div>
    </>
  );
};
