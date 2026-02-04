import { api } from './client';
import { clearAuthToken, setAuthToken } from './token';

type TokenResponse = {
  token: string;
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

export function logout() {
  clearAuthToken();
}
