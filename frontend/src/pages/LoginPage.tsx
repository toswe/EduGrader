import { useReducer, useState } from "react";
import { AuthData } from "../auth/AuthWrapper";
import { Navigate } from "react-router";

const LoginPage = () => {
  const { login, user } = AuthData();
  const [formData, setFormData] = useReducer(
    (formData, newItem) => {
      return { ...formData, ...newItem };
    },
    { userName: "", password: "" }
  );
  const [errorMessage, setErrorMessage] = useState<string | null | unknown>(
    null
  );

  const doLogin = async () => {
    try {
      await login(formData.userName, formData.password);
    } catch (error) {
      setErrorMessage(error);
    }
  };

  if (user.isAuthenticated) {
    return <Navigate to="/" />;
  }

  return (
    <div>
      <h2>Login page</h2>
      <div className="inputs">
        <div className="input">
          <input
            value={formData.userName}
            onChange={(e) => setFormData({ userName: e.target.value })}
            type="text"
          />
        </div>
        <div className="input">
          <input
            value={formData.password}
            onChange={(e) => setFormData({ password: e.target.value })}
            type="password"
          />
        </div>
        <div className="button">
          <button onClick={doLogin}>Log in</button>
        </div>
        {errorMessage ? (
          <div className="error">{String(errorMessage)}</div>
        ) : null}
      </div>
    </div>
  );
};

export default LoginPage;
