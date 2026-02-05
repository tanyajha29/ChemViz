import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import Navbar from './components/Navbar';
import AppRoutes from './routes/AppRoutes';

function AuthListener() {
  const navigate = useNavigate();

  useEffect(() => {
    const handler = () => navigate('/login');
    window.addEventListener('auth:logout', handler);
    return () => window.removeEventListener('auth:logout', handler);
  }, [navigate]);

  return null;
}

export default function App() {
  return (
    <div>
      <AuthListener />
      <Navbar />
      <AppRoutes />
    </div>
  );
}
