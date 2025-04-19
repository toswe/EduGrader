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
    <div>
      <h2>Login page</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <input
            value={formData.userName}
            name="userName"
            type="text"
            onChange={handleChange}
          />
        </div>
        <div>
          <input
            value={formData.password}
            name="password"
            type="password"
            onChange={handleChange}
          />
        </div>
        <div>
          <button type="submit">Log in</button>
        </div>
        {errorMessage ? <div>{String(errorMessage)}</div> : null}
      </form>
    </div>
  );
};

export default LoginPage;
