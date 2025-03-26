import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { Link } from "react-router";

import { fetchCourse } from "../api/courses";
import { fetchQuestions } from "../api/questions";
import { ICourse, IQuestion } from "../types";

export const CoursePage = () => {
  const { courseId } = useParams();

  const [course, setCourse] = useState<ICourse | null>(null);
  const [questions, setQuestions] = useState<IQuestion[]>([]);

  useEffect(() => {
    if (courseId) {
      fetchCourse(Number(courseId)).then((data) => {
        setCourse(data);
      });

      fetchQuestions(Number(courseId)).then((data) => {
        setQuestions(data);
      });
    }
  }, []);

  return (
    <>
      <div>
        <h3>{course?.name} </h3>
      </div>
      <div>
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
    </>
  );
};
