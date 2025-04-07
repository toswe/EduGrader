import { Route, Routes } from "react-router";
import { Home } from "../pages/home";
import { CoursePage } from "../pages/course";
import { QuestionPage } from "../pages/question";
import { TestPage } from "../pages/test";

export function ProfessorRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
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
