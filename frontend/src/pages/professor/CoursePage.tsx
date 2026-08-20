import { useEffect, useState } from "react";
import { Link, useParams } from "react-router";

import { fetchCourse } from "../../api/courses";
import { fetchQuestions } from "../../api/questions";
import { fetchTests } from "../../api/tests";
import { fetchStudentTests } from "../../api/student-tests";
import { ICourse, IQuestion, IStudentTest, ITest } from "../../types";

export const CoursePage = () => {
  const { courseId } = useParams();

  const [course, setCourse] = useState<ICourse | null>(null);
  const [questions, setQuestions] = useState<IQuestion[]>([]);
  const [tests, setTests] = useState<ITest[]>([]);
  const [studentTests, setStudentTests] = useState<IStudentTest[]>([]);

  useEffect(() => {
    if (!courseId) return;

    fetchCourse(Number(courseId)).then(setCourse);
    fetchQuestions(Number(courseId)).then(setQuestions);
    fetchTests(Number(courseId)).then(setTests);
    fetchStudentTests({ course: Number(courseId) }).then(setStudentTests);
  }, [courseId]);

  return (
    <div className="stack-lg">
      <h1>{course?.name}</h1>

      <div className="columns">
        <section className="stack">
          <h2>Questions</h2>
          {questions.map((question) => (
            <div key={question.id} className="card stack">
              <Link to={`/course/${courseId}/questions/${question.id}`}>
                {question.question}
              </Link>
              <span className="muted">{question.answer}</span>
            </div>
          ))}
          {questions.length === 0 && <p className="muted">No questions yet.</p>}
          <div>
            <Link to={`/course/${courseId}/new-question`}>
              <button>Create question</button>
            </Link>
          </div>
        </section>

        <section className="stack">
          <h2>Tests</h2>
          {tests.map((test) => (
            <div key={test.id} className="card">
              <Link to={`/course/${courseId}/tests/${test.id}`}>
                {test.name}
              </Link>
            </div>
          ))}
          {tests.length === 0 && <p className="muted">No tests yet.</p>}
          <div>
            <Link to={`/course/${courseId}/new-test`}>
              <button>Create test</button>
            </Link>
          </div>
        </section>
      </div>

      <section className="stack">
        <h2>Submitted tests</h2>
        {studentTests.map((studentTest) => (
          <div key={studentTest.id} className="card">
            <Link to={`/course/${courseId}/student-tests/${studentTest.id}`}>
              Submission #{studentTest.id}
            </Link>
          </div>
        ))}
        {studentTests.length === 0 && (
          <p className="muted">No submissions yet.</p>
        )}
      </section>
    </div>
  );
};
