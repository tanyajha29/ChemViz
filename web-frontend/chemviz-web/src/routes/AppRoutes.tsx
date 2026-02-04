import { Route, Routes } from 'react-router-dom';

import Dashboard from '../pages/Dashboard';
import History from '../pages/History';
import Home from '../pages/Home';
import Login from '../pages/Login';
import Register from '../pages/Register';
import Upload from '../pages/Upload';

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/upload" element={<Upload />} />
      <Route path="/history" element={<History />} />
    </Routes>
  );
}
