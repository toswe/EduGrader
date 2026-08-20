import { useEffect, useState } from "react";
import { Link, useParams } from "react-router";
import { fetchStudentTest } from "../../api/student-tests";
import { IStudentTest } from "../../types";
import { BackLink } from "../../components/BackLink";

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
    return <p className="muted">Loading…</p>;
  }

  return (
    <div className="stack-lg">
      <BackLink to={`/course/${courseId}`}>Back to course</BackLink>
      <h1>Submission #{studentTest.id}</h1>
      <p className="muted">
        Test:{" "}
        <Link to={`/course/${courseId}/tests/${studentTest.test}`}>
          {studentTest.testName ?? `#${studentTest.test}`}
        </Link>
      </p>

      <section className="stack">
        <h2>Answers</h2>
        {studentTest.answers.map((answer) => (
          <div key={answer.id} className="card stack">
            <div>
              <span className="field-label">Question</span>
              {answer.questionText}
            </div>
            <div>
              <span className="field-label">Answer</span>
              {answer.answer}
            </div>
            <div className="row">
              <div>
                <span className="field-label">Professor grade</span>
                {answer.score}
              </div>
              <div>
                <span className="field-label">LLM score</span>
                {answer.grades && answer.grades.length > 0
                  ? answer.grades[answer.grades.length - 1].score / 10
                  : "Not graded"}
              </div>
            </div>
          </div>
        ))}
      </section>
    </div>
  );
};
