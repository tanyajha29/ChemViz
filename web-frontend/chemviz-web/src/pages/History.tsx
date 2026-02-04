import UploadHistory from '../components/UploadHistory';

export default function History() {
  return (
    <div className="page">
      <h1 className="page-title">Upload History</h1>
      <p className="page-subtitle">
        View all previously uploaded datasets and generated reports.
      </p>

      <section className="table-card glass fade-in">
        <UploadHistory />
      </section>
    </div>
  );
}
