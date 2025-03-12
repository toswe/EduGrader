import { AuthData } from "../auth/AuthWrapper";

export const Home = () => {
  const { user, logout } = AuthData();

  return (
    <>
      <div> Hello, {user.username} </div>
      <br />
      <div>
        <button onClick={logout}> logout </button>
      </div>
    </>
  );
};
