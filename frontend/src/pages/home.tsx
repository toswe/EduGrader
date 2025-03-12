import { AuthData } from "../auth/AuthWrapper";

export const Home = () => {
  const { user } = AuthData();

  return <div> Hello, {user.username} </div>;
};
