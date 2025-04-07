import "./App.css";
import { Route, Routes } from "react-router";

import { AuthWrapper } from "./auth/AuthWrapper";
import { Login } from "./pages/login";
import ProtectedRoutes from "./routes/ProtectedRoutes";

function App() {
  return (
    <AuthWrapper>
      <Routes>
        <Route path="*" element={<ProtectedRoutes />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </AuthWrapper>
  );
}

export default App;
