import { useEffect, useReducer, useState } from "react";
import { Link, useNavigate, useParams } from "react-router";

import { fetchQuestions } from "../../api/questions";
import { createTest, fetchTest, updateTest, deleteTest } from "../../api/tests";
import { fetchStudentTests } from "../../api/student-tests";
import { IQuestion, IStudentTest } from "../../types";
import { BackLink } from "../../components/BackLink";

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
    <div className="stack-lg">
      <BackLink to={`/course/${courseId}`}>Back to course</BackLink>
      <h1>{testId ? "Edit test" : "New test"}</h1>

      <div className="stack">
        <div>
          <label htmlFor="name">Name</label>
          <input
            id="name"
            value={formData.name}
            onChange={(e) => setFormData({ name: e.target.value })}
            type="text"
          />
        </div>
        <div>
          <label htmlFor="configuration">Configuration (JSON)</label>
          <textarea
            id="configuration"
            value={formData.configuration}
            onChange={(e) => setFormData({ configuration: e.target.value })}
            rows={10}
          />
        </div>
        <div>
          <label htmlFor="questions">Questions</label>
          <select
            id="questions"
            value={formData.questions}
            multiple
            size={8}
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
        <div className="row">
          <button
            onClick={saveTest}
            disabled={!formData.name || !formData.questions.length}
          >
            Save
          </button>
          {testId && (
            <button className="danger" onClick={removeTest}>
              Delete
            </button>
          )}
        </div>
        {errorMessage ? (
          <div className="error">{String(errorMessage)}</div>
        ) : null}
      </div>

      {studentTests.length > 0 && (
        <section className="stack">
          <h2>Submitted tests</h2>
          {studentTests.map((studentTest) => (
            <div key={studentTest.id} className="card">
              <Link to={`/course/${courseId}/student-tests/${studentTest.id}`}>
                Submission #{studentTest.id}
              </Link>
            </div>
          ))}
        </section>
      )}
    </div>
  );
};
