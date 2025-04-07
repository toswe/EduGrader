import { useEffect, useState } from "react";

import { AuthData } from "../../auth/AuthWrapper";
import { fetchStudentTests } from "../../api/student-tests";
import { IStudentTest } from "../../types";

export const HomePage = () => {
  const { user, logout } = AuthData();

  const [studentTests, setStudentTests] = useState<IStudentTest[]>([]);

  const fetchTests = async () => {
    const tests = await fetchStudentTests();
    setStudentTests(tests);
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
        {studentTests.map((test: any) => {
          return <div key={test.id}>{test.test}</div>;
        })}
      </div>
    </>
  );
};
