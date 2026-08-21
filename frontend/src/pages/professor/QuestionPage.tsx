import { useReducer, useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router";

import {
  createQuestion,
  fetchQuestion,
  updateQuestion,
  deleteQuestion,
} from "../../api/questions";
import { BackLink } from "../../components/BackLink";

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

  const makeRequestAndRedirect = async (apiRequest: () => Promise<void>) => {
    apiRequest()
      .then(() => {
        navigate(`/course/${courseId}`);
      })
      .catch((error) => {
        setErrorMessage(error);
      });
  };

  const saveQuestion = async () => {
    const createOrUpdateQuestion = async () => {
      questionId
        ? updateQuestion(Number(questionId), formData.question, formData.answer)
        : createQuestion(Number(courseId), formData.question, formData.answer);
    };

    makeRequestAndRedirect(() => createOrUpdateQuestion());
  };

  const removeQuestion = async () => {
    makeRequestAndRedirect(() => deleteQuestion(Number(questionId)));
  };

  return (
    <div className="stack-lg">
      <BackLink to={`/course/${courseId}`}>Back to course</BackLink>
      <h1>{questionId ? "Edit question" : "New question"}</h1>

      <div className="stack">
        <div>
          <label htmlFor="question">Question</label>
          <textarea
            id="question"
            value={formData.question}
            onChange={(e) => setFormData({ question: e.target.value })}
          />
        </div>
        <div>
          <label htmlFor="answer">Answer</label>
          <textarea
            id="answer"
            value={formData.answer}
            onChange={(e) => setFormData({ answer: e.target.value })}
          />
        </div>
        <div className="row">
          <button
            onClick={saveQuestion}
            disabled={!formData.question || !formData.answer}
          >
            Save
          </button>
          {questionId && (
            <button className="danger" onClick={removeQuestion}>
              Delete
            </button>
          )}
        </div>
        {errorMessage ? (
          <div className="error">{String(errorMessage)}</div>
        ) : null}
      </div>
    </div>
  );
};
