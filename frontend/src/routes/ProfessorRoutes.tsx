import { Route, Routes } from "react-router";

import HomePage from "../pages/professor/HomePage";
import CoursePage from "../pages/professor/CoursePage";
import QuestionPage from "../pages/professor/QuestionPage";
import TestPage from "../pages/professor/TestPage";

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
      </Route>
    </Routes>
  );
}
