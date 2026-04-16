import httpx

async def mark_attendance_api(base_url: str, user_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{base_url}/api/v1/attendance/mark/{user_id}")
        r.raise_for_status()
        return r.json()