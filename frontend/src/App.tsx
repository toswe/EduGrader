import "./App.css";
import { Route, Routes } from "react-router";

import { AuthWrapper, ProtectedRoutes } from "./auth/AuthWrapper";
import { Login } from "./pages/login";
import { Home } from "./pages/home";
import { Course } from "./pages/course";

function App() {
  return (
    <AuthWrapper>
      <Routes>
        <Route element={<ProtectedRoutes />}>
          <Route path="/" element={<Home />} />
          <Route path="/course/:courseId" element={<Course />} />
        </Route>

        <Route path="/login" element={<Login />} />
      </Routes>
    </AuthWrapper>
  );
}

export default App;
