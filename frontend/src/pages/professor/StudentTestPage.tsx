import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { fetchStudentTest } from "../../api/student-tests";
import { IStudentTest } from "../../types";

export const StudentTestPage = () => {
  const { studentTestId } = useParams();
  const [studentTest, setStudentTest] = useState<IStudentTest | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>("");

  useEffect(() => {
    if (studentTestId) {
      fetchStudentTest(Number(studentTestId))
        .then((data: IStudentTest) => {
          setStudentTest(data);
        })
        .catch((error: unknown) => {
          setErrorMessage(String(error));
        });
    }
  }, [studentTestId]);

  if (errorMessage) {
    return <div className="error">{errorMessage}</div>;
  }

  if (!studentTest) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Student Test Details</h1>
      <p>
        <strong>ID:</strong> {studentTest.id}
      </p>
      <p>
        <strong>Test:</strong> {studentTest.test}
      </p>
    </div>
  );
};
