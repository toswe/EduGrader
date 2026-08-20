import { useEffect, useState } from "react";
import { Link, useParams } from "react-router";
import { fetchStudentTest } from "../../api/student-tests";
import { IStudentTest } from "../../types";
import { BackLink } from "../../components/BackLink";

// Both scales are 0-10: the professor grades on it directly, the LLM returns 0-100.
const formatScore = (score?: number | null) =>
  score === undefined || score === null
    ? "not graded"
    : `${Math.round(score * 10) / 10} / 10`;

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
        {studentTest.answers.map((answer, index) => {
          const grades = answer.grades ?? [];
          const llmGrade = grades[grades.length - 1];
          return (
            <div key={answer.id} className="card stack">
              <div className="card-header">
                <div>
                  <span className="field-label">Question {index + 1}</span>
                  {answer.questionText}
                </div>
                <div className="row">
                  <span className="badge">
                    Professor <b>{formatScore(answer.score)}</b>
                  </span>
                  <span className="badge">
                    LLM <b>{formatScore(llmGrade && llmGrade.score / 10)}</b>
                  </span>
                </div>
              </div>
              <div>
                <span className="field-label">Answer</span>
                <div className="answer-text">{answer.answer}</div>
              </div>
            </div>
          );
        })}
      </section>
    </div>
  );
};
