import { useEffect, useState } from "react";
import { Link, useParams } from "react-router";
import { fetchStudentTest } from "../../api/student-tests";
import { updateStudentAnswerScore } from "../../api/student-answers";
import { IStudentAnswer, IStudentTest } from "../../types";
import { BackLink } from "../../components/BackLink";

// Both scales are 0-10: the professor grades on it directly, the LLM returns 0-100.
const formatScore = (score?: number | null) =>
  score === undefined || score === null
    ? "not graded"
    : `${Math.round(score * 10) / 10} / 10`;

const AnswerCard = ({
  answer,
  index,
}: {
  answer: IStudentAnswer;
  index: number;
}) => {
  const [score, setScore] = useState(answer.score ?? "");
  const [errorMessage, setErrorMessage] = useState<string | unknown>("");

  const grades = answer.grades ?? [];
  const llmGrade = grades[grades.length - 1];

  const saveScore = async () => {
    updateStudentAnswerScore(Number(answer.id), Number(score)).catch(
      (error) => {
        setErrorMessage(error);
      }
    );
  };

  return (
    <div className="card stack">
      <div className="card-header">
        <div>
          <span className="field-label">Question {index + 1}</span>
          {answer.questionText}
        </div>
        <div className="row">
          <span className="badge">
            LLM <b>{formatScore(llmGrade && llmGrade.score / 10)}</b>
          </span>
        </div>
      </div>
      <div>
        <span className="field-label">Answer</span>
        <div className="answer-text">{answer.answer}</div>
      </div>
      <div className="row">
        <label htmlFor={`score-${answer.id}`}>Grade</label>
        <input
          id={`score-${answer.id}`}
          className="score-input"
          value={score}
          type="number"
          min="0"
          max="10"
          step="0.1"
          onChange={(e) => setScore(e.target.value)}
        />
        <span className="muted">/ 10</span>
        <button onClick={saveScore} disabled={score === ""}>
          Save
        </button>
      </div>
      {errorMessage ? (
        <div className="error">{String(errorMessage)}</div>
      ) : null}
    </div>
  );
};

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
        {studentTest.answers.map((answer, index) => (
          <AnswerCard key={answer.id} answer={answer} index={index} />
        ))}
      </section>
    </div>
  );
};
