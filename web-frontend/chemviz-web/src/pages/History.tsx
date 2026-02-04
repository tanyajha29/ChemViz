import { FiClock } from 'react-icons/fi';

import UploadHistory from '../components/UploadHistory';

export default function History() {
  return (
    <div className="page">
      <h1 className="page-title">
        <FiClock className="inline-icon" />
        Upload History
      </h1>
      <p className="page-subtitle">
        View all previously uploaded datasets and generated reports.
      </p>

      <section className="table-card glass fade-in neon-glow">
        <UploadHistory />
      </section>
    </div>
  );
}
