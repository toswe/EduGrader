import { Link } from "react-router";

export function BackLink({ to, children }: { to: string; children: React.ReactNode }) {
  return (
    <Link to={to} className="back-link">
      ← {children}
    </Link>
  );
}
