import { useParams } from "react-router";

import { fetchTestWithQuestions } from "../../api/tests";
import { IQuestion, ITestQuestions } from "../../types";
import { useEffect, useState } from "react";

export const TestPage = () => {
  const { testId } = useParams();

  const [test, setTest] = useState<ITestQuestions | null>(null);
  const [answers, setAnswers] = useState<IQuestion[]>([]);

  const fetchTestData = async () => {
    if (!testId) {
      return;
    }

    fetchTestWithQuestions(Number(testId)).then((test) => {
      setTest(test);
      const initialAnswers = test.questions.map((question) => ({
        ...question,
        answer: "",
      }));
      setAnswers(initialAnswers);
    });
  };

  const handleInputChange = (index: number, value: string) => {
    const updatedAnswers = [...answers];
    updatedAnswers[index].answer = value;
    setAnswers(updatedAnswers);
  };

  const handleSubmit = () => {
    console.log("Submitted answers:", answers);
  };

  useEffect(() => {
    fetchTestData();
  }, []);

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
        {test.questions.map((question, index) => (
          <div key={index}>
            {question.question}
            <br />
            <textarea
              value={answers[index]?.answer || ""}
              onChange={(e) => handleInputChange(index, e.target.value)}
            />
          </div>
        ))}
        <button type="submit">Submit</button>
      </form>
    </>
  );
};

/// TODO Try to refactor this to only use one state variable
