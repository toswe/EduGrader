import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { Link } from "react-router";

import { fetchCourse } from "../api/courses";
import { fetchQuestions } from "../api/questions";
import { ICourse, IQuestion } from "../types";

export const Course = () => {
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
          <div key={question.id}>
            {/* TODO Maybe change the link path... */}
            <Link to={`/questions/${question.id}`}>{question.question}</Link>
          </div>
        ))}
      </div>
    </>
  );
};
