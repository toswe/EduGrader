import { useEffect, useReducer, useState } from "react";
import { useNavigate, useParams } from "react-router";

import { fetchQuestions } from "../api/questions";
import { createTest, fetchTest, updateTest, deleteTest } from "../api/tests";
import { IQuestion } from "../types";

export const TestPage = () => {
  const navigate = useNavigate();
  const { courseId, testId } = useParams();

  const [errorMessage, setErrorMessage] = useState<string | unknown>("");
  const [questions, setQuestions] = useState<IQuestion[]>([]);

  const [formData, setFormData] = useReducer(
    (formData, newItem) => {
      return { ...formData, ...newItem };
    },
    { name: "", questions: [] }
  );

  useEffect(() => {
    if (courseId) {
      fetchQuestions(Number(courseId)).then((data) => {
        setQuestions(data);
      });
    }
  }, [courseId]);

  useEffect(() => {
    if (testId) {
      fetchTest(Number(testId))
        .then((data) => {
          setFormData({
            name: data.name,
            questions: data.questions.map((question) => question),
          });
        })
        .catch((error) => {
          setErrorMessage(error);
        });
    }
  }, [testId]);

  const makeRequestAndRedirect = async (apiRequest: () => Promise<void>) => {
    apiRequest()
      .then(() => {
        navigate(`/course/${courseId}`);
      })
      .catch((error) => {
        setErrorMessage(error);
      });
  };

  const saveTest = async () => {
    const createOrUpdateTest = async () => {
      testId
        ? updateTest(Number(testId), formData.name, formData.questions)
        : createTest(Number(courseId), formData.name, formData.questions);
    };
    makeRequestAndRedirect(() => createOrUpdateTest());
  };

  const removeTest = async () => {
    makeRequestAndRedirect(() => deleteTest(Number(testId)));
  };

  return (
    <div>
      <div>
        <input
          value={formData.name}
          onChange={(e) => setFormData({ name: e.target.value })}
          type="text"
        />
      </div>
      <div>
        <select
          value={formData.questions}
          multiple
          onChange={(e) =>
            setFormData({
              questions: Array.from(e.target.selectedOptions, (option) =>
                Number(option.value)
              ),
            })
          }
        >
          {questions.map((question) => (
            <option key={question.id} value={question.id}>
              {question.question}
            </option>
          ))}
        </select>
      </div>
      <div>
        <button
          onClick={saveTest}
          disabled={!formData.name || !formData.questions.length}
        >
          Save
        </button>
        {testId && <button onClick={removeTest}>Delete</button>}
      </div>
      {errorMessage ? (
        <div className="error">{String(errorMessage)}</div>
      ) : null}
    </div>
  );
};
