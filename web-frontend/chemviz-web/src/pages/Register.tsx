import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { registerUser } from '../api/auth';

export default function Register() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError('');
    setLoading(true);

    try {
      await registerUser(username, email, password);
      navigate('/dashboard');
    } catch (err: unknown) {
      setError('Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="auth-card glass fade-in">
        <h1 className="page-title">Create Account</h1>
        <p className="page-subtitle">Start using ChemViz in minutes.</p>
        <form onSubmit={handleSubmit}>
          <label className="field-label" htmlFor="username">
            Username
          </label>
          <input
            id="username"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
          />
          <label className="field-label" htmlFor="email">
            Email (optional)
          </label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />
          <label className="field-label" htmlFor="password">
            Password
          </label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
          {error ? <p className="error-text">{error}</p> : null}
          <button type="submit" className="nav-button" disabled={loading}>
            {loading ? 'Creating...' : 'Register'}
          </button>
        </form>
      </div>
    </div>
  );
}
