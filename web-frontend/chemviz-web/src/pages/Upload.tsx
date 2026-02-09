import { useState } from 'react';
import { FiClipboard, FiUploadCloud } from 'react-icons/fi';

import { uploadDataset, RowError, ValidationSummary } from '../api/datasets';

export default function Upload() {
  const [file, setFile] = useState<File | null>(null);
  const [name, setName] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [validation, setValidation] = useState<ValidationSummary | null>(null);
  const [rowErrors, setRowErrors] = useState<RowError[]>([]);
  const maxFileSizeMb = 5;
  const maxFileSize = maxFileSizeMb * 1024 * 1024;

  const isCsvFile = file ? file.name.toLowerCase().endsWith('.csv') : false;
  const isSizeValid = file ? file.size <= maxFileSize : false;
  const isFileValid = !!file && isCsvFile && isSizeValid;
  const fileSizeLabel = file ? `${(file.size / (1024 * 1024)).toFixed(2)} MB` : '';

  const handleFileChange = (nextFile: File | null) => {
    setError('');
    setMessage('');
    setValidation(null);
    setRowErrors([]);
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
    setValidation(null);
    setRowErrors([]);

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
      const validationSummary =
        result.validation_summary ?? result.summary?.validation ?? null;
      setValidation(validationSummary);
      setRowErrors(validationSummary?.row_errors ?? []);
      setMessage(`Upload successful: ${result.name}`);
      window.dispatchEvent(new Event('datasets:updated'));
      setFile(null);
      setName('');
    } catch (err: any) {
      const data = err?.response?.data;
      if (data?.validation_summary) {
        setValidation(data.validation_summary);
        setRowErrors(data.validation_summary.row_errors ?? []);
      }
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

      {validation ? (
        <section className="table-card glass fade-in neon-glow">
          <h2 className="section-title">Validation Summary</h2>
          <div className="validation-grid">
            <div>
              <span className="validation-label">Total Rows</span>
              <strong>{validation.total_rows}</strong>
            </div>
            <div>
              <span className="validation-label">Accepted Rows</span>
              <strong>{validation.accepted_rows}</strong>
            </div>
            <div>
              <span className="validation-label">Rejected Rows</span>
              <strong>{validation.rejected_rows}</strong>
            </div>
          </div>

          <div className="validation-details">
            <div>
              <h3>Missing Values</h3>
              <ul>
                {Object.entries(validation.missing_values || {}).map(([key, value]) => (
                  <li key={`missing-${key}`}>
                    {key}: {value}
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h3>Invalid Values</h3>
              <ul>
                {Object.entries(validation.invalid_values || {}).map(([key, value]) => (
                  <li key={`invalid-${key}`}>
                    {key}: {value}
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h3>Out of Range</h3>
              <ul>
                {Object.entries(validation.out_of_range || {}).map(([key, value]) => (
                  <li key={`range-${key}`}>
                    {key}: {value}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {rowErrors.length ? (
            <div className="validation-errors">
              <h3>Row Level Issues (first {rowErrors.length})</h3>
              <ul>
                {rowErrors.map((issue, idx) => (
                  <li key={`${issue.row}-${issue.column}-${idx}`}>
                    Row {issue.row}: {issue.column} - {issue.message}
                  </li>
                ))}
              </ul>
            </div>
          ) : null}
        </section>
      ) : null}
    </div>
  );
}

