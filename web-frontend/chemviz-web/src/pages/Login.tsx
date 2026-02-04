import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { FiLogIn } from 'react-icons/fi';

import { login } from '../api/auth';

export default function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(username, password);
      navigate('/dashboard');
    } catch (err: unknown) {
      setError('Login failed. Check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="auth-card glass fade-in neon-glow">
        <h1 className="page-title">
          <FiLogIn className="inline-icon" />
          Welcome Back
        </h1>
        <p className="page-subtitle">Sign in to access ChemViz.</p>
        <form onSubmit={handleSubmit}>
          <label className="field-label" htmlFor="username">
            Username
          </label>
          <input
            id="username"
            name="username"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            autoComplete="username"
          />
          <label className="field-label" htmlFor="password">
            Password
          </label>
          <input
            id="password"
            name="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            autoComplete="current-password"
          />
          {error ? <p className="error-text">{error}</p> : null}
          <button type="submit" className="nav-button" disabled={loading}>
            <FiLogIn className="inline-icon" />
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
      </div>
    </div>
  );
}
