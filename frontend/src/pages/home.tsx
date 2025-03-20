import { useState } from "react";
import { AuthData } from "../auth/AuthWrapper";
import { fetchHome } from "../api/home";

export const Home = () => {
  const { user, logout } = AuthData();

  const [homeDetails, setHomeDetails] = useState("");

  const fetchDetails = async () => {
    fetchHome().then((response) => setHomeDetails(response.data?.message));
  };

  return (
    <>
      <div> Hello, {user.username} </div>
      <br />
      <div>
        <button onClick={logout}> logout </button>
        <button onClick={fetchDetails}> Fetch details </button>
      </div>
      <div> {homeDetails} </div>
    </>
  );
};
