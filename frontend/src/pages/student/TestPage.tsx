import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { useNavigate } from "react-router";

import { fetchTestWithQuestions } from "../../api/tests";
import { createStudentTest } from "../../api/student-tests";
import { ITestQuestions, IStudentTest } from "../../types";
import { BackLink } from "../../components/BackLink";

const initStudentTest = (test: ITestQuestions): IStudentTest => {
  return {
    test: test.id,
    answers: test.questions.map((q) => ({
      question: q.id,
      questionText: q.question,
      answer: "",
      score: 0,
    })),
  };
};

export const TestPage = () => {
  const { testId } = useParams();
  const navigate = useNavigate();

  const [test, setTest] = useState<IStudentTest | null>(null);

  useEffect(() => {
    // TODO Handle this, maybe redirect
    if (!testId) return;

    fetchTestWithQuestions(Number(testId)).then((testData) => {
      setTest(initStudentTest(testData));
    });
  }, [testId]);

  const handleChange = (questionId: number, value: string) => {
    if (!test) return;

    const newAnswers = test.answers.map((q) =>
      q.question === questionId ? { ...q, answer: value } : q
    );

    setTest({ ...test, answers: newAnswers });
  };

  const handleSubmit = () => {
    if (!test) return;
    createStudentTest(test).then(() => navigate("/"));
  };

  if (!test) {
    return <p className="muted">Loading…</p>;
  }

  return (
    <form
      className="stack-lg"
      onSubmit={(e) => {
        e.preventDefault();
        handleSubmit();
      }}
    >
      <BackLink to="/">Back to tests</BackLink>
      <h1>Test</h1>
      <div className="stack">
        {test.answers.map((answer) => (
          <div key={answer.question} className="card">
            <label htmlFor={`answer-${answer.question}`}>
              {answer.questionText}
            </label>
            <textarea
              id={`answer-${answer.question}`}
              value={answer.answer || ""}
              onChange={(e) => handleChange(answer.question, e.target.value)}
            />
          </div>
        ))}
      </div>
      <div>
        <button type="submit">Submit</button>
      </div>
    </form>
  );
};
