import { api } from './client';

export type DatasetSummary = {
  total_equipment: number;
  avg_flowrate: number | null;
  avg_pressure: number | null;
  avg_temperature: number | null;
  type_distribution: Record<string, number>;
};

export type UploadResult = {
  id: number;
  name: string;
  uploaded_at: string;
  summary: DatasetSummary;
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
