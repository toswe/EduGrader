import { Route, Routes } from "react-router";
import { HomePage, TestPage } from "../pages/student";

export function StudentRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/test/:testId" element={<TestPage />} />
    </Routes>
  );
}
