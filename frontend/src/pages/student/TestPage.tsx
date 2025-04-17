import { useEffect, useState } from "react";
import { useParams } from "react-router";

import { fetchTestWithQuestions } from "../../api/tests";
import { ITestQuestions } from "../../types";

export const TestPage = () => {
  const { testId } = useParams();

  const [test, setTest] = useState<ITestQuestions | null>(null);

  useEffect(() => {
    // TODO Handle this, maybe redirect
    if (!testId) return;

    fetchTestWithQuestions(Number(testId)).then((testData) => {
      setTest({
        ...testData,
        questions: testData.questions.map((q) => ({ ...q, answer: "" })),
      });
    });
  }, [testId]);

  const handleChange = (questionId: number, value: string) => {
    if (!test) return;

    const newQuestions = test.questions.map((q) =>
      q.id === questionId ? { ...q, answer: value } : q
    );

    setTest({ ...test, questions: newQuestions });
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
      <div>
        <h3>{test.name}</h3>
      </div>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSubmit();
        }}
      >
        {test.questions.map((question) => (
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
