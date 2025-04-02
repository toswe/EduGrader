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
          <Route path="/course/:courseId/">
            <Route index element={<CoursePage />} />
            <Route path="new-question" element={<QuestionPage />} />
            <Route path="questions/:questionId" element={<QuestionPage />} />
            <Route path="new-test" element={<TestPage />} />
            <Route path="tests/:testId" element={<TestPage />} />
          </Route>
        </Route>

        <Route path="/login" element={<Login />} />
      </Routes>
    </AuthWrapper>
  );
}

export default App;
