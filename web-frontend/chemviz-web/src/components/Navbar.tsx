import { NavLink } from 'react-router-dom';
import { FiClock, FiGrid, FiHome, FiLogIn, FiUploadCloud, FiUser, FiUserPlus } from 'react-icons/fi';

const navItems = [
  { path: '/', label: 'Home', icon: <FiHome /> },
  { path: '/dashboard', label: 'Dashboard', icon: <FiGrid /> },
  { path: '/upload', label: 'Upload', icon: <FiUploadCloud /> },
  { path: '/history', label: 'History', icon: <FiClock /> },
  { path: '/profile', label: 'Profile', icon: <FiUser /> },
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
            <span className="nav-icon">{item.icon}</span>
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="nav-actions">
        <NavLink to="/login" className="nav-link">
          <span className="nav-icon">
            <FiLogIn />
          </span>
          Login
        </NavLink>
        <NavLink to="/register" className="nav-button">
          <span className="nav-icon">
            <FiUserPlus />
          </span>
          Register
        </NavLink>
      </div>
    </header>
  );
}
