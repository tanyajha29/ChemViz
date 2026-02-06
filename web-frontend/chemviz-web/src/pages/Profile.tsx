import { useNavigate } from 'react-router-dom';
import { FiLogOut, FiUser } from 'react-icons/fi';

import { logout } from '../api/auth';
import { getAuthToken } from '../api/token';

export default function Profile() {
  const navigate = useNavigate();
  const token = getAuthToken();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">
          <FiUser className="inline-icon" />
          Profile
        </h1>
        <p className="page-subtitle">
          Manage your session and account access.
        </p>
      </div>

      <section className="profile-card glass neon-glow">
        <div className="profile-row">
          <span className="profile-label">Auth Token</span>
          <span className="profile-value">
            {token ? `${token.slice(0, 8)}…` : 'Not logged in'}
          </span>
        </div>
        <button type="button" className="nav-button" onClick={handleLogout}>
          <FiLogOut className="inline-icon" />
          Logout
        </button>
      </section>
    </div>
  );
}
