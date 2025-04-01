import "./App.css";
import { Route, Routes } from "react-router";

import { AuthWrapper, ProtectedRoutes } from "./auth/AuthWrapper";
import { Login } from "./pages/login";
import { Home } from "./pages/home";
import { CoursePage } from "./pages/course";
import { QuestionPage } from "./pages/question";
import { TestPage } from "./pages/test";

function App() {
  return (
    <AuthWrapper>
      <Routes>
        <Route element={<ProtectedRoutes />}>
          <Route path="/" element={<Home />} />
          <Route path="/course/:courseId" element={<CoursePage />} />
          <Route
            path="/course/:courseId/new-question"
            element={<QuestionPage />}
          />
          <Route
            path="/course/:courseId/questions/:questionId"
            element={<QuestionPage />}
          />
          <Route path="/course/:courseId/new-test" element={<TestPage />} />
          <Route
            path="/course/:courseId/tests/:testId"
            element={<TestPage />}
          />
        </Route>

        <Route path="/login" element={<Login />} />
      </Routes>
    </AuthWrapper>
  );
}

export default App;
