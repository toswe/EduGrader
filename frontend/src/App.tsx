import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router";

import { AuthWrapper, ProtectedRoutes } from "./auth/AuthWrapper";
import { Login } from "./pages/login";
import { Home } from "./pages/home";

function App() {
  return (
    <AuthWrapper>
      <BrowserRouter>
        <Routes>
          <Route element={<ProtectedRoutes />}>
            <Route path="/" element={<Home />} />
          </Route>

          <Route path="/login" element={<Login />} />
        </Routes>
      </BrowserRouter>
    </AuthWrapper>
  );
}

export default App;
