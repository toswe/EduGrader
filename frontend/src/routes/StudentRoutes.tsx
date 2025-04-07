import { Route, Routes } from "react-router";
import { Home } from "../pages/student/home";

export function StudentRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
    </Routes>
  );
}
