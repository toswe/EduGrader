import { useEffect, useReducer, useState } from "react";
import { useNavigate, useParams } from "react-router";

import { fetchQuestions } from "../../api/questions";
import { createTest, fetchTest, updateTest, deleteTest } from "../../api/tests";
import { fetchStudentTests } from "../../api/student-tests";
import { IQuestion, IStudentTest } from "../../types";

export const TestPage = () => {
  const navigate = useNavigate();
  const { courseId, testId } = useParams();

  const [errorMessage, setErrorMessage] = useState<string | unknown>("");
  const [questions, setQuestions] = useState<IQuestion[]>([]);
  const [studentTests, setStudentTests] = useState<IStudentTest[]>([]);

  const [formData, setFormData] = useReducer(
    (formData, newItem) => {
      return { ...formData, ...newItem };
    },
    { name: "", configuration: "", questions: [] }
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
            ...data,
            configuration: JSON.stringify(data.configuration, null, 2),
          });
        })
        .catch((error) => {
          setErrorMessage(error);
        });

      fetchStudentTests({ test: Number(testId) })
        .then((data) => {
          setStudentTests(data);
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
    const data = {
      ...formData,
      course: Number(courseId),
      configuration: JSON.parse(formData.configuration || "{}"),
    };
    const createOrUpdateTest = async () => {
      testId ? updateTest({ ...data, id: Number(testId) }) : createTest(data);
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
        Config:
        <br />
        <textarea
          value={formData.configuration}
          onChange={(e) => setFormData({ configuration: e.target.value })}
          rows={10}
          cols={50}
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

      <div>
        {studentTests.length > 0 && (
          <>
            <h3>Student Tests</h3>
            <ul>
              {studentTests.map((studentTest) => (
                <li key={studentTest.id}>
                  <a
                    href={`/course/${courseId}/student-tests/${studentTest.id}`}
                  >
                    {studentTest.id}
                  </a>
                </li>
              ))}
            </ul>
          </>
        )}
      </div>
    </div>
  );
};
