import { useEffect, useState } from "react";
import { Link } from "react-router";

import { fetchUpcomingTests, fetchStudentTests } from "../../api/student-tests";
import { ITest, IStudentTest } from "../../types";

export const HomePage = () => {
  const [upcomingTests, setUpcomingTests] = useState<ITest[]>([]);
  const [studentTests, setStudentTests] = useState<IStudentTest[]>([]);

  useEffect(() => {
    fetchUpcomingTests().then((upcomingTests) => {
      setUpcomingTests(upcomingTests);
    });

    fetchStudentTests().then((studentTests) => {
      setStudentTests(studentTests);
    });
  }, []);

  return (
    <div className="stack-lg">
      <h1>Your tests</h1>

      <section className="stack">
        <h2>Upcoming</h2>
        {upcomingTests.map((test) => (
          <div key={test.id} className="card">
            <Link to={`/test/${test.id}`}>{test.name}</Link>
          </div>
        ))}
        {upcomingTests.length === 0 && (
          <p className="muted">No upcoming tests.</p>
        )}
      </section>

      <section className="stack">
        <h2>Completed</h2>
        {studentTests.map((test) => (
          <div key={test.id} className="card">
            Test #{test.test}
          </div>
        ))}
        {studentTests.length === 0 && (
          <p className="muted">No completed tests yet.</p>
        )}
      </section>
    </div>
  );
};
