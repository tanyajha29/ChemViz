import { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
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

import { fetchReport, fetchSummaries } from '../api/datasets';
import { getAuthToken } from '../api/token';

const navItems = [
  { path: '/', label: 'Home', icon: <FiHome /> },
  { path: '/dashboard', label: 'Dashboard', icon: <FiGrid /> },
  { path: '/upload', label: 'Upload', icon: <FiUploadCloud /> },
  { path: '/history', label: 'History', icon: <FiClock /> },
];

export default function Navbar() {
  const navigate = useNavigate();
  const token = getAuthToken();
  const [downloading, setDownloading] = useState(false);

  const handleDownload = async () => {
    if (!token) {
      navigate('/login');
      return;
    }

    setDownloading(true);
    try {
      const summaries = await fetchSummaries();
      const latest = summaries[0];
      if (!latest) {
        window.alert('No reports available yet.');
        return;
      }

      const blob = await fetchReport(latest.id);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `chemviz-report-${latest.id}.pdf`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      window.alert('Unable to download report. Please try again.');
    } finally {
      setDownloading(false);
    }
  };

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
        {token ? (
          <>
            <button
              type="button"
              className="nav-button"
              onClick={handleDownload}
              disabled={downloading}
            >
              <span className="nav-icon">
                <FiDownload />
              </span>
              {downloading ? 'Downloading...' : 'Download'}
            </button>
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
              Login
            </NavLink>
            <NavLink to="/register" className="nav-button">
              <span className="nav-icon">
                <FiUserPlus />
              </span>
              Register
            </NavLink>
          </>
        )}
      </div>
    </header>
  );
}
