import { Route, Routes } from "react-router";
import {
  HomePage,
  CoursePage,
  QuestionPage,
  TestPage,
  StudentTestPage,
} from "../pages/professor";

export function ProfessorRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/course/:courseId/">
        <Route index element={<CoursePage />} />
        <Route path="new-question" element={<QuestionPage />} />
        <Route path="questions/:questionId" element={<QuestionPage />} />
        <Route path="new-test" element={<TestPage />} />
        <Route path="tests/:testId" element={<TestPage />} />
        <Route path="student-tests/:studentTestId" element={<StudentTestPage />} />
      </Route>
    </Routes>
  );
}
