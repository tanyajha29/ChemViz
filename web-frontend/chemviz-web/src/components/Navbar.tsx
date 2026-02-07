import { NavLink } from 'react-router-dom';
import {
  FiClock,
  FiDownload,
  FiGrid,
  FiHome,
  FiLogIn,
  FiUploadCloud,
  FiUser,
  FiUserPlus,
} from 'react-icons/fi';

import { getAuthToken } from '../api/token';

const navItems = [
  { path: '/', label: 'Home', icon: <FiHome /> },
  { path: '/dashboard', label: 'Dashboard', icon: <FiGrid /> },
  { path: '/upload', label: 'Upload', icon: <FiUploadCloud /> },
  { path: '/history', label: 'History', icon: <FiClock /> },
];

export default function Navbar() {
  const token = getAuthToken();
  const downloadUrl =
    'https://github.com/tanyajha29/ChemViz/releases/latest/download/ChemVizDesktop.exe';

  return (
    <header className="nav glass">
      <div className="nav-brand">
        <div className="nav-logo-badge">CV</div>
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
        <a
          href={downloadUrl}
          className="nav-button"
          target="_blank"
          rel="noreferrer"
        >
          <span className="nav-icon">
            <FiDownload />
          </span>
          Download App
        </a>
        {token ? (
          <>
            <NavLink to="/profile" className="nav-link">
              <span className="nav-icon">
                <FiUser />
              </span>
              Profile
            </NavLink>
          </>
        ) : (
          <>
            <NavLink to="/login" className="nav-link">
              <span className="nav-icon">
                <FiLogIn />
              </span>
              Sign In
            </NavLink>
            <NavLink to="/register" className="nav-button">
              <span className="nav-icon">
                <FiUserPlus />
              </span>
              Sign Up
            </NavLink>
          </>
        )}
      </div>
    </header>
  );
}
