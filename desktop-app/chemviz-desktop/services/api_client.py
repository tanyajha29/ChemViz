import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import requests


TOKEN_PATH = Path(__file__).resolve().parent.parent / "data" / "token.json"


def _save_token(token: str) -> None:
    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_PATH.write_text(json.dumps({"token": token}), encoding="utf-8")


def _load_token() -> Optional[str]:
    if not TOKEN_PATH.exists():
        return None
    try:
        data = json.loads(TOKEN_PATH.read_text(encoding="utf-8"))
        return data.get("token")
    except json.JSONDecodeError:
        return None


def _clear_token() -> None:
    if TOKEN_PATH.exists():
        TOKEN_PATH.unlink()


@dataclass
class ApiClient:
    base_url: str = "http://127.0.0.1:8000"
    token: Optional[str] = None

    def __post_init__(self) -> None:
        if self.token is None:
            self.token = _load_token()

    def _headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = {}
        if self.token:
            headers["Authorization"] = f"Token {self.token}"
        return headers

    def login(self, username: str, password: str) -> str:
        response = requests.post(
            f"{self.base_url}/api/auth/token/",
            json={"username": username, "password": password},
            timeout=15,
        )
        response.raise_for_status()
        token = response.json().get("token")
        if not token:
            raise ValueError("Token not returned by server.")
        self.token = token
        _save_token(token)
        return token

    def logout(self) -> None:
        self.token = None
        _clear_token()

    def fetch_summaries(self) -> Dict[str, Any]:
        response = requests.get(
            f"{self.base_url}/api/datasets/summaries/",
            headers=self._headers(),
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    def fetch_profile(self) -> Dict[str, Any]:
        response = requests.get(
            f"{self.base_url}/api/auth/me/",
            headers=self._headers(),
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    def upload_csv(self, file_path: str, name: Optional[str] = None) -> Dict[str, Any]:
        with open(file_path, "rb") as handle:
            files = {"file": handle}
            data = {}
            if name:
                data["name"] = name
            response = requests.post(
                f"{self.base_url}/api/datasets/upload/",
                headers=self._headers(),
                files=files,
                data=data,
                timeout=30,
            )
        response.raise_for_status()
        return response.json()


client = ApiClient()
