import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FiLock, FiMail, FiUser, FiUserPlus } from 'react-icons/fi';

import { registerUser } from '../api/auth';

export default function Register() {
  const navigate = useNavigate();
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const namePattern = /^[A-Za-z ]+$/;
  const trimmedFullName = fullName.trim();
  const trimmedEmail = email.trim().toLowerCase();
  const isNameValid =
    trimmedFullName.length >= 2 && namePattern.test(trimmedFullName);
  const isEmailValid = emailPattern.test(trimmedEmail);
  const hasUpper = /[A-Z]/.test(password);
  const hasLower = /[a-z]/.test(password);
  const hasNumber = /\d/.test(password);
  const hasSpaces = /\s/.test(password);
  const isPasswordValid =
    password.length >= 8 && hasUpper && hasLower && hasNumber && !hasSpaces;
  const isConfirmValid = password === confirmPassword && confirmPassword.length > 0;
  const isFormValid = isNameValid && isEmailValid && isPasswordValid && isConfirmValid;

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError('');
    setSuccess('');
    if (!trimmedFullName || !trimmedEmail || !password) {
      setError('Full name, email, and password are required.');
      return;
    }

    if (!isNameValid) {
      setError('Full name must be at least 2 characters and use letters only.');
      return;
    }

    if (!emailPattern.test(trimmedEmail)) {
      setError('Please enter a valid email address.');
      return;
    }

    if (!isPasswordValid) {
      setError(
        'Password must be at least 8 characters and include uppercase, lowercase, and a number (no spaces).'
      );
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setLoading(true);

    try {
      await registerUser(trimmedFullName, trimmedEmail, password, confirmPassword);
      setSuccess('Account created successfully.');
      window.alert('Account created successfully.');
      navigate('/dashboard');
    } catch (err: any) {
      const data = err?.response?.data;
      if (data && typeof data === 'object') {
        const firstMessage = Object.values(data)[0];
        if (typeof firstMessage === 'string') {
          setError(firstMessage);
          return;
        }
      }
      setError('Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="bg-shape shape-1" />
      <div className="bg-shape shape-2" />

      <div className="auth-card neon-glow">
        <div className="auth-header">
          <FiUserPlus className="auth-icon" />
          <h1>Create Account</h1>
          <p>
            Start using <strong>ChemViz</strong> today
          </p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="input-group">
            <FiUser className="input-icon" />
            <input
              placeholder="Full Name"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <FiMail className="input-icon" />
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <FiLock className="input-icon" />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <FiLock className="input-icon" />
            <input
              type="password"
              placeholder="Confirm password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>

          {error && <p className="error-text">{error}</p>}
          {success && <p className="success-text">{success}</p>}

          <button type="submit" disabled={!isFormValid || loading}>
            {loading ? 'Creating account…' : 'Register'}
          </button>
        </form>

        <p className="auth-footer">
          Already have an account?
          <Link to="/login"> Sign in</Link>
        </p>
      </div>
    </div>
  );
}
