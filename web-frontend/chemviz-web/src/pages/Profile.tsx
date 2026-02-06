import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiLogOut, FiUser } from 'react-icons/fi';

import { fetchProfile, logout, type ProfileResponse } from '../api/auth';
import { getAuthToken } from '../api/token';

export default function Profile() {
  const navigate = useNavigate();
  const token = getAuthToken();
  const [profile, setProfile] = useState<ProfileResponse | null>(null);
  const [status, setStatus] = useState<'idle' | 'loading' | 'error'>('idle');

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  useEffect(() => {
    let isMounted = true;

    if (!token) {
      setProfile(null);
      setStatus('idle');
      return () => {
        isMounted = false;
      };
    }

    setStatus('loading');
    fetchProfile()
      .then((data) => {
        if (!isMounted) return;
        setProfile(data);
        setStatus('idle');
      })
      .catch(() => {
        if (!isMounted) return;
        setProfile(null);
        setStatus('error');
      });

    return () => {
      isMounted = false;
    };
  }, [token]);

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
          <span className="profile-label">Username</span>
          <span className="profile-value">
            {profile?.username ?? (token ? 'Loading...' : 'Not logged in')}
          </span>
        </div>
        <div className="profile-row">
          <span className="profile-label">Email</span>
          <span className="profile-value">
            {profile?.email ?? (token ? 'Loading...' : 'Not logged in')}
          </span>
        </div>
        {status === 'error' && (
          <p className="error-text">
            Unable to load profile details. Please sign in again.
          </p>
        )}
        <button type="button" className="nav-button" onClick={handleLogout}>
          <FiLogOut className="inline-icon" />
          Logout
        </button>
      </section>
    </div>
  );
}
