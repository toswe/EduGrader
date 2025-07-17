import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { fetchStudentTest } from "../../api/student-tests";
import { IStudentTest } from "../../types";

export const StudentTestPage = () => {
  const { courseId, studentTestId } = useParams();
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
        <strong>Test:</strong>{" "}
        <a href={`/course/${courseId}/tests/${studentTest.test}`}>
          {studentTest.test}
        </a>
      </p>
      <p>
        Answers:
        {studentTest.answers.map((answer) => (
          <div
            key={answer.id}
            style={{
              border: "1px solid black",
              margin: "10px",
              padding: "5px",
              borderRadius: "5px",
            }}
          >
            <strong>Question:</strong> {answer.questionText}
            <br />
            <strong>Answer:</strong> {answer.answer}
            <br />
            <strong>Score:</strong>{" "}
            {answer.grades && answer.grades.length > 0
              ? answer.grades[answer.grades.length - 1].score
              : "Not graded"}
          </div>
        ))}
      </p>
    </div>
  );
};
