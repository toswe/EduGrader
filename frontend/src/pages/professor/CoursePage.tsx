import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { Link } from "react-router";

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
    if (courseId) {
      fetchCourse(Number(courseId)).then((data) => {
        setCourse(data);
      });

      fetchQuestions(Number(courseId)).then((data) => {
        setQuestions(data);
      });

      fetchTests(Number(courseId)).then((data) => {
        setTests(data);
      });

      fetchStudentTests({ course: Number(courseId) }).then((data) => {
        setStudentTests(data);
      });
    }
  }, []);

  return (
    <>
      <div>
        <h3>{course?.name} </h3>
      </div>
      <div>
        <h4>Questions</h4>
        {questions.map((question) => (
          <div
            key={question.id}
            style={{
              border: "1px solid black",
              margin: "10px",
              padding: "5px",
              borderRadius: "5px",
            }}
          >
            <strong>{question.question}</strong>
            <br />
            <span>{question.answer}</span>
            <br />
            <Link to={`/course/${courseId}/questions/${question.id}`}>
              <button>Edit</button>
            </Link>
          </div>
        ))}
      </div>
      <div>
        <Link to={`/course/${courseId}/new-question`}>
          <button>Create question</button>
        </Link>
      </div>
      <div>
        <h4>Tests</h4>
        {tests.map((test) => (
          <div
            key={test.id}
            style={{
              border: "1px solid black",
              margin: "10px",
              padding: "5px",
              borderRadius: "5px",
            }}
          >
            <strong>{test.name}</strong>
            <br />
            <Link to={`/course/${courseId}/tests/${test.id}`}>
              <button>Edit</button>
            </Link>
          </div>
        ))}
      </div>
      <div>
        <Link to={`/course/${courseId}/new-test`}>
          <button>Create test</button>
        </Link>
      </div>
      <div>
        <h4>Student Tests</h4>
        {studentTests.map((studentTest) => (
          <div
            key={studentTest.id}
            style={{
              border: "1px solid black",
              margin: "10px",
              padding: "5px",
              borderRadius: "5px",
            }}
          >
            <a href={`/course/${courseId}/student-tests/${studentTest.id}`}>{studentTest.id}</a>
          </div>
        ))}
      </div>
    </>
  );
};
