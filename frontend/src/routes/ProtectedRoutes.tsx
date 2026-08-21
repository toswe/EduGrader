import { Navigate } from "react-router";

import { AuthData } from "../auth/AuthWrapper";
import { Layout } from "../components/Layout";
import { ProfessorRoutes } from "./ProfessorRoutes";
import { StudentRoutes } from "./StudentRoutes";

function ProtectedRoutes() {
  const { user } = AuthData();

  if (!user || !user.isAuthenticated) {
    return <Navigate to="/login" />;
  }

  return (
    <Layout>
      {user.type === "PROFESSOR" ? <ProfessorRoutes /> : <StudentRoutes />}
    </Layout>
  );
}

export default ProtectedRoutes;
