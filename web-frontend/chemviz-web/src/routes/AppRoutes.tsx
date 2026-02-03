import { Route, Routes } from 'react-router-dom';

import Dashboard from '../pages/Dashboard';
import History from '../pages/History';
import Login from '../pages/Login';
import Upload from '../pages/Upload';

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<Dashboard />} />
      <Route path="/upload" element={<Upload />} />
      <Route path="/history" element={<History />} />
    </Routes>
  );
}
