import httpx
from typing import List

BASE_URL = "http://127.0.0.1:8001"
API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlcm1la29mZmRhc3RhbkBnbWFpbC5jb20iLCJyb2xlcyI6WyJST0xFX1BPUlRBTF9VU0VSIl0sImV4cCI6MTcyNjQ0OTg1NH0.X21Rr954MRA550C3JRHVBby5GwHIVSL2zwd3nFNa-58"

async def get_users() -> List[dict]:
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/users/all/", headers=headers)
        response.raise_for_status()
        return response.json()

async def get_departments() -> List[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/departments/all/")
        response.raise_for_status()
        return response.json()


