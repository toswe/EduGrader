import { AuthData } from "../../auth/AuthWrapper";

export const HomePage = () => {
  const { user, logout } = AuthData();

  return (
    <>
      <h1>Student Home</h1>
      <div> Hello, {user.username} </div>
      <br />
      <div>
        <button onClick={logout}> logout </button>
      </div>
    </>
  );
};
