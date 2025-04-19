import { useEffect, useState } from "react";
import { useParams } from "react-router";

import { fetchTestWithQuestions } from "../../api/tests";
import { ITestQuestions, IStudentTest } from "../../types";

const createStudentTest = (test: ITestQuestions): IStudentTest => {
  return {
    test: test.id,
    answers: test.questions.map((q) => ({
      id: q.id,
      question: q.question,
      answer: "",
    })),
  };
};

export const TestPage = () => {
  const { testId } = useParams();

  const [test, setTest] = useState<IStudentTest | null>(null);

  useEffect(() => {
    // TODO Handle this, maybe redirect
    if (!testId) return;

    fetchTestWithQuestions(Number(testId)).then((testData) => {
      setTest(createStudentTest(testData));
    });
  }, [testId]);

  const handleChange = (questionId: number, value: string) => {
    if (!test) return;

    const newAnswers = test.answers.map((q) =>
      q.id === questionId ? { ...q, answer: value } : q
    );

    setTest({ ...test, answers: newAnswers });
  };

  const handleSubmit = () => {
    if (!test) return;
    console.log("Submitted test:", test);
  };

  if (!test) {
    return <div>Loading...</div>;
  }

  return (
    <>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSubmit();
        }}
      >
        {test.answers.map((question) => (
          <div key={question.id}>
            {question.question}
            <br />
            <textarea
              value={question.answer || ""}
              onChange={(e) => handleChange(question.id, e.target.value)}
            />
          </div>
        ))}
        <button type="submit">Submit</button>
      </form>
    </>
  );
};
