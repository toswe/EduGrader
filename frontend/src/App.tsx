import "./App.css";
import { Route, Routes } from "react-router";

import { AuthWrapper } from "./auth/AuthWrapper";
import LoginPage from "./pages/LoginPage";
import ProtectedRoutes from "./routes/ProtectedRoutes";

function App() {
  return (
    <AuthWrapper>
      <Routes>
        <Route path="*" element={<ProtectedRoutes />} />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </AuthWrapper>
  );
}

export default App;
