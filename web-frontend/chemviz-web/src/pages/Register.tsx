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
  const [fieldErrors, setFieldErrors] = useState<{
    fullName?: string;
    email?: string;
    password?: string;
    confirm?: string;
  }>({});

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
    setFieldErrors({});
    const nextErrors: {
      fullName?: string;
      email?: string;
      password?: string;
      confirm?: string;
    } = {};

    if (!trimmedFullName) {
      nextErrors.fullName = 'Full name is required.';
    } else if (!isNameValid) {
      nextErrors.fullName = 'Full name must be 2+ characters (letters and spaces).';
    }

    if (!trimmedEmail) {
      nextErrors.email = 'Email is required.';
    } else if (!emailPattern.test(trimmedEmail)) {
      nextErrors.email = 'Please enter a valid email address.';
    }

    if (!password) {
      nextErrors.password = 'Password is required.';
    } else if (!isPasswordValid) {
      nextErrors.password =
        'Password must be 8+ chars with uppercase, lowercase, number (no spaces).';
    }

    if (!confirmPassword) {
      nextErrors.confirm = 'Confirm password is required.';
    } else if (password !== confirmPassword) {
      nextErrors.confirm = 'Passwords do not match.';
    }

    if (Object.keys(nextErrors).length) {
      setFieldErrors(nextErrors);
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
        const serverErrors: typeof nextErrors = {};
        if (data.full_name) serverErrors.fullName = data.full_name;
        if (data.email) serverErrors.email = data.email;
        if (data.password) serverErrors.password = data.password;
        if (data.confirm_password) serverErrors.confirm = data.confirm_password;
        if (Object.keys(serverErrors).length) {
          setFieldErrors(serverErrors);
          return;
        }
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
          {fieldErrors.fullName && (
            <p className="field-error">{fieldErrors.fullName}</p>
          )}

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
          {fieldErrors.email && (
            <p className="field-error">{fieldErrors.email}</p>
          )}

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
          {fieldErrors.password && (
            <p className="field-error">{fieldErrors.password}</p>
          )}

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
          {fieldErrors.confirm && (
            <p className="field-error">{fieldErrors.confirm}</p>
          )}

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
