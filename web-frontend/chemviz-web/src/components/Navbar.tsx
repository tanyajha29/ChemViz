import { NavLink } from 'react-router-dom';

const navItems = [
  { path: '/', label: 'Home' },
  { path: '/dashboard', label: 'Dashboard' },
  { path: '/upload', label: 'Upload' },
  { path: '/history', label: 'History' },
];

export default function Navbar() {
  return (
    <header className="nav glass">
      <div className="nav-brand">
        <img src="/logo.gif" alt="ChemViz logo" className="nav-logo" />
        <span className="nav-title">ChemViz</span>
      </div>
      <nav className="nav-links">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `nav-link ${isActive ? 'nav-link-active' : ''}`
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
      <div className="nav-actions">
        <NavLink to="/login" className="nav-link">
          Login
        </NavLink>
        <NavLink to="/register" className="nav-button">
          Register
        </NavLink>
      </div>
    </header>
  );
}
