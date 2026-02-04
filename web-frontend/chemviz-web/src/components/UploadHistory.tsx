import { useEffect, useState } from 'react';

import { fetchReport, fetchSummaries, UploadResult } from '../api/datasets';

export default function UploadHistory() {
  const [uploads, setUploads] = useState<UploadResult[]>([]);
  const [error, setError] = useState('');
  const [downloadingId, setDownloadingId] = useState<number | null>(null);

  useEffect(() => {
    let isMounted = true;
    fetchSummaries()
      .then((results) => {
        if (!isMounted) {
          return;
        }
        setUploads(results);
      })
      .catch(() => {
        if (!isMounted) {
          return;
        }
        setError('Failed to load upload history.');
      });

    return () => {
      isMounted = false;
    };
  }, []);

  const handleDownload = async (uploadId: number, name: string) => {
    setDownloadingId(uploadId);
    setError('');
    try {
      const blob = await fetchReport(uploadId);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${name || 'chemviz-report'}.pdf`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err: unknown) {
      setError('Failed to download report.');
    } finally {
      setDownloadingId(null);
    }
  };

  return (
    <div>
      <h2 className="section-title">Recent Uploads</h2>
      {error ? <p className="error-text">{error}</p> : null}
      {!uploads.length ? <p className="empty-state">No uploads found.</p> : null}
      {uploads.length ? (
        <table className="data-table">
          <thead>
            <tr>
              <th>Dataset</th>
              <th>Uploaded</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {uploads.map((upload) => (
              <tr key={upload.id}>
                <td>{upload.name}</td>
                <td>{new Date(upload.uploaded_at).toLocaleString()}</td>
                <td>
                  <button
                    type="button"
                    className="nav-button"
                    onClick={() => handleDownload(upload.id, upload.name)}
                    disabled={downloadingId === upload.id}
                  >
                    {downloadingId === upload.id ? 'Downloading...' : 'Download PDF'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : null}
    </div>
  );
}
