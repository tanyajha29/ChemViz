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
    <div>
      <h1>Upload</h1>
      <p>Upload CSV files to ChemViz.</p>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="datasetName">Dataset Name (optional)</label>
        </div>
        <input
          id="datasetName"
          name="datasetName"
          value={name}
          onChange={(event) => setName(event.target.value)}
        />
        <div>
          <label htmlFor="csvFile">CSV File</label>
        </div>
        <input
          id="csvFile"
          name="csvFile"
          type="file"
          accept=".csv"
          onChange={(event) => setFile(event.target.files?.[0] ?? null)}
        />
        {error ? <p>{error}</p> : null}
        {message ? <p>{message}</p> : null}
        <button type="submit" disabled={loading}>
          {loading ? 'Uploading...' : 'Upload'}
        </button>
      </form>
    </div>
  );
}
