import { Navigate } from "react-router";

import { AuthData } from "../auth/AuthWrapper";
import { ProfessorRoutes } from "./ProfessorRoutes";
import { StudentRoutes } from "./StudentRoutes";

function ProtectedRoutes() {
  const { user } = AuthData();

  if (!user || !user.isAuthenticated) {
    return <Navigate to="/login" />;
  }

  return (
    <>{user.type === "PROFESSOR" ? <ProfessorRoutes /> : <StudentRoutes />}</>
  );
}

export default ProtectedRoutes;
