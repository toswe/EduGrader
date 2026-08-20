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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    setFormData({ [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    login(formData.userName, formData.password).catch((error) => {
      setErrorMessage(error);
    });
  };

  if (user.isAuthenticated) {
    return <Navigate to="/" />;
  }

  return (
    <main className="app-main narrow">
      <h1>EduGrader</h1>
      <form className="stack" onSubmit={handleSubmit}>
        <div>
          <label htmlFor="userName">Username</label>
          <input
            id="userName"
            value={formData.userName}
            name="userName"
            type="text"
            autoComplete="username"
            onChange={handleChange}
          />
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input
            id="password"
            value={formData.password}
            name="password"
            type="password"
            autoComplete="current-password"
            onChange={handleChange}
          />
        </div>
        <div>
          <button type="submit">Log in</button>
        </div>
        {errorMessage ? (
          <div className="error">{String(errorMessage)}</div>
        ) : null}
      </form>
    </main>
  );
};

export default LoginPage;
