import { useReducer, useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router";

import {
  createQuestion,
  fetchQuestion,
  updateQuestion,
} from "../api/questions";

export const QuestionPage = () => {
  const navigate = useNavigate();
  const { courseId, questionId } = useParams();

  const [errorMessage, setErrorMessage] = useState<string | unknown>("");
  const [formData, setFormData] = useReducer(
    (formData, newItem) => ({ ...formData, ...newItem }),
    { question: "", answer: "" }
  );

  useEffect(() => {
    if (questionId) {
      fetchQuestion(Number(questionId)).then((data) => {
        setFormData({ ...data });
      });
    }
  }, [questionId]);

  const saveQuestion = async () => {
    const createOrUpdateQuestion = async () => {
      questionId
        ? updateQuestion(Number(questionId), formData.question, formData.answer)
        : createQuestion(Number(courseId), formData.question, formData.answer);
    };

    createOrUpdateQuestion()
      .then(() => {
        navigate(`/course/${courseId}`);
      })
      .catch((error) => {
        setErrorMessage(error);
      });
  };

  return (
    <div>
      <h2>New Question</h2>
      <div className="inputs">
        <div className="input">
          <label>Question</label>
          <br />
          <textarea
            value={formData.question}
            onChange={(e) => setFormData({ question: e.target.value })}
          />
        </div>
        <div className="input">
          <label>Answer</label>
          <br />
          <textarea
            value={formData.answer}
            onChange={(e) => setFormData({ answer: e.target.value })}
          />
        </div>
        {formData.question && formData.answer && (
          <div className="button">
            <button onClick={saveQuestion}>Save</button>
          </div>
        )}
        {errorMessage ? (
          <div className="error">{String(errorMessage)}</div>
        ) : null}
      </div>
    </div>
  );
};
