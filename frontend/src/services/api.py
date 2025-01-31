import httpx
from typing import Optional, List, Dict, Any
from ..config import settings

class APIClient:
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.token: Optional[str] = None
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=30.0,
            verify=settings.VERIFY_SSL,
            follow_redirects=True
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def login(self, username: str, password: str) -> Dict[str, str]:
        try:
            response = await self.client.post(
                "/auth/token",
                json={"username": username, "password": password}
            )
            response.raise_for_status()
            data = response.json()
            self.token = data["access_token"]
            return data
        except httpx.HTTPError as e:
            raise APIError("Login failed", "AUTH_ERROR", getattr(e.response, 'status_code', 500))

    def get_headers(self) -> Dict[str, str]:
        headers = {
            "Accept": "application/json",
            "User-Agent": "MediTech-Client/1.0"
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def _make_request(self, method: str, url: str, **kwargs) -> Any:
        try:
            response = await self.client.request(
                method,
                url,
                headers=self.get_headers(),
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            self.handle_error(e.response)

    # Patients
    async def get_patients(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        return await self._make_request(
            "GET",
            "/patients",
            params={"skip": skip, "limit": limit}
        )

    async def create_patient(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._make_request(
            "POST",
            "/patients",
            json=data
        )

    # Appointments
    async def get_appointments(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        response = await self.client.get(
            "/appointments",
            headers=self.get_headers(),
            params={"skip": skip, "limit": limit}
        )
        return response.json()

    async def create_appointment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = await self.client.post(
            "/appointments",
            headers=self.get_headers(),
            json=data
        )
        return response.json()

    # Examinations
    async def get_examinations(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        response = await self.client.get(
            "/examinations",
            headers=self.get_headers(),
            params={"skip": skip, "limit": limit}
        )
        return response.json()

    async def create_examination(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = await self.client.post(
            "/examinations",
            headers=self.get_headers(),
            json=data
        )
        return response.json()

    # Reports
    async def get_health_reports(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        response = await self.client.get(
            "/reports/health",
            headers=self.get_headers(),
            params={"skip": skip, "limit": limit}
        )
        return response.json()

    async def create_health_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = await self.client.post(
            "/reports/health",
            headers=self.get_headers(),
            json=data
        )
        return response.json()

    async def download_report_pdf(self, report_id: str) -> bytes:
        response = await self.client.get(
            f"/reports/health/{report_id}/pdf",
            headers=self.get_headers()
        )
        return response.content

    # UI Settings
    async def get_themes(self) -> List[Dict[str, Any]]:
        response = await self.client.get(
            "/settings/themes",
            headers=self.get_headers()
        )
        return response.json()

    async def update_accessibility(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        response = await self.client.put(
            "/settings/accessibility",
            headers=self.get_headers(),
            json=settings
        )
        return response.json()

    # Error Handling
    def handle_error(self, response: httpx.Response) -> None:
        try:
            error = response.json()
        except ValueError:
            error = {"message": "Unknown error", "code": "ERROR"}
        
        status_code = response.status_code
        if status_code == 401:
            raise APIError("Unauthorized", "AUTH_ERROR", status_code)
        elif status_code == 403:
            raise APIError("Forbidden", "FORBIDDEN", status_code)
        elif status_code == 404:
            raise APIError("Resource not found", "NOT_FOUND", status_code)
        elif status_code >= 500:
            raise APIError("Server error", "SERVER_ERROR", status_code)
        else:
            raise APIError(
                error.get("message", "Unknown error"),
                error.get("code", "ERROR"),
                status_code
            )

class APIError(Exception):
    def __init__(self, message: str, code: str, status_code: int):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(f"{message} (Code: {code}, Status: {status_code})") 