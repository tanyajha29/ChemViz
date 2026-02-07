import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiLogOut, FiMail, FiUser } from 'react-icons/fi';

import { fetchProfile, logout, type ProfileResponse } from '../api/auth';
import { getAuthToken } from '../api/token';

export default function Profile() {
  const navigate = useNavigate();
  const token = getAuthToken();

  const [profile, setProfile] = useState<ProfileResponse | null>(null);
  const [status, setStatus] = useState<'idle' | 'loading' | 'error'>('idle');

  const handleLogout = async () => {
    await logout();
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
    <div
      className="page fade-in"
      style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
      }}
    >
      <div className="page-header center-text">
        <h1 className="page-title">
          <FiUser className="inline-icon" />
          Profile
        </h1>
        <p className="page-subtitle">Manage your session and account access</p>
      </div>

      <div
        style={{
          flex: 1,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          width: '100%',
        }}
      >
        <section
          className="profile-card glass neon-glow fade-in fade-delay-1"
          style={{
            width: '100%',
            maxWidth: 420,
          }}
        >
          <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
            <div
              style={{
                width: 72,
                height: 72,
                borderRadius: '50%',
                margin: '0 auto',
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

          <div className="profile-row">
            <span className="profile-label">
              <FiUser className="inline-icon" />
              Username
            </span>
            <span className="profile-value">
              {profile?.username ?? (token ? 'Loading...' : 'Not logged in')}
            </span>
          </div>

          <div className="profile-row">
            <span className="profile-label">
              <FiMail className="inline-icon" />
              Email
            </span>
            <span className="profile-value">
              {profile?.email ?? (token ? 'Loading...' : 'Not logged in')}
            </span>
          </div>

          <div className="profile-row">
            <span className="profile-label">Role</span>
            <span className="profile-value">
              {profile?.role ?? (token ? 'Loading...' : 'Not logged in')}
            </span>
          </div>

          {status === 'error' && (
            <p className="error-text">
              Unable to load profile details. Please sign in again.
            </p>
          )}

          <button
            type="button"
            className="nav-button"
            onClick={handleLogout}
            style={{
              width: '100%',
              justifyContent: 'center',
              marginTop: '1rem',
            }}
          >
            <FiLogOut className="inline-icon" />
            Logout
          </button>
        </section>
      </div>
    </div>
  );
}
