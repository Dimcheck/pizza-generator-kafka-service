import json
import urllib.parse as u_parse

from fastapi.exceptions import HTTPException
from httpx import AsyncClient


class Communication:
    def __init__(self, url):
        self.url = url

    async def get_response(self, retries: int = 3, timeout: int = 5):
        try:
            async with AsyncClient() as client:
                data = await client.get(self.url, timeout=timeout)
                return json.loads(data.content)
        except Exception as e:
            raise HTTPException(status_code=400, detail=e)

    async def get_response_with_params(self, retries: int = 3, **kwargs):
        self.url = f"{self.url}?{u_parse.urlencode(kwargs)}"
        return await self.get_response(retries)

