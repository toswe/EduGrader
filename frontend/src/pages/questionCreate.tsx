import { useReducer, useState } from "react";
import { useNavigate, useParams } from "react-router";

import { createQuestion } from "../api/questions";

export const QuestionCreate = () => {
  const navigate = useNavigate();
  const { courseId } = useParams();

  const [errorMessage, setErrorMessage] = useState<string | unknown>("");
  const [formData, setFormData] = useReducer(
    (formData, newItem) => ({ ...formData, ...newItem }),
    { question: "", answer: "" }
  );

  const saveQuestion = async () => {
    createQuestion(Number(courseId), formData.question, formData.answer)
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
