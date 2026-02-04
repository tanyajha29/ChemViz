import { useState } from 'react';

import { uploadDataset } from '../api/datasets';

export default function Upload() {
  const [file, setFile] = useState<File | null>(null);
  const [name, setName] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setMessage('');
    setError('');

    if (!file) {
      setError('Please select a CSV file to upload.');
      return;
    }

    setLoading(true);
    try {
      const result = await uploadDataset(file, name);
      setMessage(`Upload successful: ${result.name}`);
      setFile(null);
      setName('');
    } catch (err: unknown) {
      setError('Upload failed. Please check the CSV and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h1 className="page-title">Upload Dataset</h1>
      <p className="page-subtitle">
        Drag and drop or browse to upload equipment CSV files.
      </p>
      <form className="upload-card glass fade-in" onSubmit={handleSubmit}>
        <label className="field-label" htmlFor="datasetName">
          Dataset Name (optional)
        </label>
        <input
          id="datasetName"
          name="datasetName"
          value={name}
          onChange={(event) => setName(event.target.value)}
        />
        <label className="field-label" htmlFor="csvFile">
          CSV File
        </label>
        <div className="dropzone">
          <input
            id="csvFile"
            name="csvFile"
            type="file"
            accept=".csv"
            onChange={(event) => setFile(event.target.files?.[0] ?? null)}
          />
          <p>{file ? file.name : 'Drop CSV here or click to browse'}</p>
        </div>
        {error ? <p className="error-text">{error}</p> : null}
        {message ? <p className="success-text">{message}</p> : null}
        <button type="submit" className="nav-button" disabled={loading}>
          {loading ? 'Uploading...' : 'Upload'}
        </button>
      </form>
    </div>
  );
}
