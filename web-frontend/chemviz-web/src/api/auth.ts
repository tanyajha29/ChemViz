import { api } from './client';
import { clearAuthToken, setAuthToken } from './token';

type TokenResponse = {
  token: string;
};

export type ProfileResponse = {
  id: number;
  username: string;
  email: string;
  role: string;
  last_login: string | null;
};

export async function login(username: string, password: string) {
  const response = await api.post<TokenResponse>('/api/auth/token/', {
    username,
    password,
  });
  setAuthToken(response.data.token);
  return response.data.token;
}

export async function registerUser(
  username: string,
  email: string,
  password: string
) {
  const response = await api.post<TokenResponse>('/api/auth/register/', {
    username,
    email,
    password,
  });
  setAuthToken(response.data.token);
  return response.data.token;
}

export async function logout() {
  try {
    await api.post('/api/auth/logout/');
  } finally {
    clearAuthToken();
  }
}

export async function fetchProfile() {
  const response = await api.get<ProfileResponse>('/api/auth/me/');
  return response.data;
}
