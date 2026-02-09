import { api } from './client';

export type DatasetSummary = {
  total_equipment: number;
  avg_flowrate: number | null;
  avg_pressure: number | null;
  avg_temperature: number | null;
  type_distribution: Record<string, number>;
  row_count?: number;
  file_size_bytes?: number;
  validation?: ValidationSummary;
};

export type RowError = {
  row: number;
  column: string;
  message: string;
};

export type ValidationSummary = {
  total_rows: number;
  accepted_rows: number;
  rejected_rows: number;
  missing_values: Record<string, number>;
  invalid_values: Record<string, number>;
  out_of_range: Record<string, number>;
  row_errors?: RowError[];
};

export type UploadResult = {
  id: number;
  name: string;
  uploaded_at: string;
  summary: DatasetSummary;
  uploaded_by?: string;
  row_count?: number;
  file_size_bytes?: number;
  accepted_rows?: number;
  rejected_rows?: number;
  validation_summary?: ValidationSummary;
};

export async function uploadDataset(file: File, name?: string) {
  const formData = new FormData();
  formData.append('file', file);
  if (name) {
    formData.append('name', name);
  }

  const response = await api.post<UploadResult>('/api/datasets/upload/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });

  return response.data;
}

export async function fetchSummaries() {
  const response = await api.get<{ results: UploadResult[] }>(
    '/api/datasets/summaries/'
  );
  return response.data.results;
}

export async function fetchReport(uploadId: number) {
  const response = await api.get(`/api/datasets/report/${uploadId}/`, {
    responseType: 'blob',
  });
  return response.data as Blob;
}

export type LatestDataset = {
  id: number;
  name: string;
  uploaded_at: string;
  rows: Array<{
    'Equipment Name': string;
    Type: string;
    Flowrate: number;
    Pressure: number;
    Temperature: number;
  }>;
};

export async function fetchLatestRows() {
  const response = await api.get<LatestDataset>('/api/datasets/latest/');
  return response.data;
}
