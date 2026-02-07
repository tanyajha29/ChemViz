import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiLogOut, FiUser, FiMail } from 'react-icons/fi';

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
    <div className="page fade-in">
      {/* Header */}
      <div className="page-header center-text">
        <h1 className="page-title">
          <FiUser className="inline-icon" />
          Profile
        </h1>
        <p className="page-subtitle">
          Manage your session and account access
        </p>
      </div>

      {/* Profile Card */}
      <section className="profile-card glass neon-glow fade-in fade-delay-1">
        {/* Avatar */}
        <div className="center-text">
          <div
            style={{
              width: 72,
              height: 72,
              borderRadius: '50%',
              margin: '0 auto 1rem',
              display: 'grid',
              placeItems: 'center',
              fontSize: '1.8rem',
              fontWeight: 800,
              color: '#000',
              background:
                'linear-gradient(135deg, var(--accent-purple), var(--accent-blue))',
              boxShadow: '0 0 24px rgba(124,58,237,0.45)',
            }}
          >
            {profile?.username?.[0]?.toUpperCase() ?? 'U'}
          </div>
        </div>

        {/* User Info */}
        <div className="profile-row">
          <span className="profile-label">
            <FiUser className="inline-icon" />
            Username
          </span>
          <span className="profile-value">
            {profile?.username ?? (token ? 'Loading…' : 'Not logged in')}
          </span>
        </div>

        <div className="profile-row">
          <span className="profile-label">
            <FiMail className="inline-icon" />
            Email
          </span>
          <span className="profile-value">
            {profile?.email ?? (token ? 'Loading…' : 'Not logged in')}
          </span>
        </div>

        {/* Status */}
        {status === 'error' && (
          <p className="error-text">
            Unable to load profile details. Please sign in again.
          </p>
        )}

        {/* Logout */}
        <button
          type="button"
          className="nav-button"
          onClick={handleLogout}
          style={{ justifyContent: 'center', marginTop: '0.6rem' }}
        >
          <FiLogOut className="inline-icon" />
          Logout
        </button>
      </section>
    </div>
  );
}