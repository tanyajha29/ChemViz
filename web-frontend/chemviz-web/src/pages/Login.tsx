import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { FiLogIn, FiUser, FiLock } from 'react-icons/fi';
import { login } from '../api/auth';

export default function Login() {
  const navigate = useNavigate();
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [fieldErrors, setFieldErrors] = useState<{ identifier?: string; password?: string }>({});

  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const trimmedIdentifier = identifier.trim();
  const isEmailInput = trimmedIdentifier.includes('@');
  const isIdentifierValid =
    trimmedIdentifier.length > 0 && (!isEmailInput || emailPattern.test(trimmedIdentifier));
  const isPasswordTrimmed = password.trim() === password;
  const isPasswordValid = password.length >= 8 && isPasswordTrimmed;
  const isFormValid = isIdentifierValid && isPasswordValid;

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setSuccess('');
    setFieldErrors({});
    const nextErrors: { identifier?: string; password?: string } = {};

    if (!trimmedIdentifier) {
      nextErrors.identifier = 'Email or username is required.';
    } else if (isEmailInput && !emailPattern.test(trimmedIdentifier)) {
      nextErrors.identifier = 'Please enter a valid email address.';
    }

    if (!password) {
      nextErrors.password = 'Password is required.';
    } else if (password.length < 8) {
      nextErrors.password = 'Password must be at least 8 characters.';
    } else if (!isPasswordTrimmed) {
      nextErrors.password = 'Password cannot start or end with spaces.';
    }

    if (Object.keys(nextErrors).length) {
      setFieldErrors(nextErrors);
      return;
    }
    setLoading(true);

    try {
      await login(trimmedIdentifier, password);
      setSuccess('Login successful.');
      window.alert('Login successful.');
      navigate('/dashboard');
    } catch {
      setFieldErrors({ password: 'Invalid email or password.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrapper">
      {/* floating background shapes */}
      <div className="bg-shape shape-1" />
      <div className="bg-shape shape-2" />

      <div className="auth-card neon-glow">
        <div className="auth-header">
          <FiLogIn className="auth-icon" />
          <h1>Welcome Back</h1>
          <p>Sign in to continue to <strong>ChemViz</strong></p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="input-group">
            <FiUser className="input-icon" />
            <input
              placeholder="Email or Username"
              value={identifier}
              onChange={(e) => setIdentifier(e.target.value)}
              autoComplete="username"
              required
            />
          </div>
          {fieldErrors.identifier && (
            <p className="field-error">{fieldErrors.identifier}</p>
          )}

          <div className="input-group">
            <FiLock className="input-icon" />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              required
            />
          </div>
          {fieldErrors.password && (
            <p className="field-error">{fieldErrors.password}</p>
          )}

          {error && <p className="error-text">{error}</p>}
          {success && <p className="success-text">{success}</p>}

          <button type="submit" disabled={!isFormValid || loading}>
            {loading ? 'Signing in…' : 'Sign In'}
          </button>
        </form>

        <p className="auth-footer">
          Don’t have an account?
          <Link to="/register"> Create one</Link>
        </p>
      </div>
    </div>
  );
}
