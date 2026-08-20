import { Link } from "react-router";

import { AuthData } from "../auth/AuthWrapper";

export function Layout({ children }: { children: React.ReactNode }) {
  const { user, logout } = AuthData();

  return (
    <>
      <header className="app-header">
        <Link to="/" className="brand">
          EduGrader
        </Link>
        <div className="row">
          <span className="muted">{user.username}</span>
          <button className="secondary" onClick={logout}>
            Log out
          </button>
        </div>
      </header>
      <main className="app-main">{children}</main>
    </>
  );
}
