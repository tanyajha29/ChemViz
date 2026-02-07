import { useState } from 'react';
import { FiClipboard, FiUploadCloud } from 'react-icons/fi';

import { uploadDataset } from '../api/datasets';

export default function Upload() {
  const [file, setFile] = useState<File | null>(null);
  const [name, setName] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const maxFileSizeMb = 5;
  const maxFileSize = maxFileSizeMb * 1024 * 1024;

  const isCsvFile = file ? file.name.toLowerCase().endsWith('.csv') : false;
  const isSizeValid = file ? file.size <= maxFileSize : false;
  const isFileValid = !!file && isCsvFile && isSizeValid;
  const fileSizeLabel = file ? `${(file.size / (1024 * 1024)).toFixed(2)} MB` : '';

  const handleFileChange = (nextFile: File | null) => {
    setError('');
    setMessage('');
    setFile(nextFile);
    if (!nextFile) {
      return;
    }
    if (!nextFile.name.toLowerCase().endsWith('.csv')) {
      setError('Invalid file type. Please upload a .csv file.');
      return;
    }
    if (nextFile.size > maxFileSize) {
      setError(`File is too large. Max size is ${maxFileSizeMb} MB.`);
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setMessage('');
    setError('');

    if (!file) {
      setError('Please select a CSV file to upload.');
      return;
    }

    if (!isCsvFile) {
      setError('Invalid file type. Please upload a .csv file.');
      return;
    }

    if (!isSizeValid) {
      setError(`File is too large. Max size is ${maxFileSizeMb} MB.`);
      return;
    }

    setLoading(true);
    try {
      const result = await uploadDataset(file, name);
      setMessage(`Upload successful: ${result.name}`);
      window.dispatchEvent(new Event('datasets:updated'));
      setFile(null);
      setName('');
    } catch (err: any) {
      const data = err?.response?.data;
      if (data?.error) {
        setError(String(data.error));
      } else {
        setError('Upload failed. Please check the CSV and try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">Upload Dataset</h1>
        <p className="page-subtitle">
          Drag and drop or browse to upload equipment CSV files.
        </p>
      </div>

      <div className="upload-layout">
        <form className="upload-card glass fade-in neon-glow" onSubmit={handleSubmit}>
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
              onChange={(event) => handleFileChange(event.target.files?.[0] ?? null)}
            />
            <div className="dropzone-icon">
              <FiUploadCloud />
            </div>
            <p>
              {file
                ? `${file.name} (${fileSizeLabel})`
                : 'Drop CSV here or click to browse'}
            </p>
            <span className="dropzone-hint">
              Required columns: Equipment Name, Type, Flowrate, Pressure,
              Temperature
            </span>
          </div>

          <div className="upload-actions">
            <button
              type="submit"
              className="nav-button"
              disabled={!isFileValid || loading}
            >
              {loading ? 'Uploading...' : 'Upload'}
            </button>
            <span className="upload-meta-chip">CSV only</span>
            <span className="upload-meta-chip">Max {maxFileSizeMb} MB</span>
            <span className="upload-meta-chip">Max 5 uploads stored</span>
          </div>

          {error ? <p className="error-text">{error}</p> : null}
          {message ? <p className="success-text">{message}</p> : null}
        </form>

        <aside className="upload-side glass fade-in neon-glow">
          <h2 className="section-title">
            <FiClipboard className="inline-icon" />
            Upload Checklist
          </h2>
          <ul className="upload-checklist">
            <li>Use the official column headers.</li>
            <li>Validate Flowrate, Pressure, Temperature values.</li>
            <li>Keep datasets scoped to one experiment.</li>
            <li>Download PDF reports after upload.</li>
          </ul>
        </aside>
      </div>
    </div>
  );
}

