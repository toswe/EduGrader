import { Route, Routes } from "react-router";
import HomePage from "../pages/student/HomePage";

export function StudentRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
    </Routes>
  );
}
