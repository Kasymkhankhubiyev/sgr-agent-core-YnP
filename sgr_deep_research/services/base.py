import httpx
from sgr_deep_research.settings import get_config

config = get_config()


class HTTPClient:
    service_name: str = ""
    service_url: str = ""

    @classmethod
    async def request(
        cls,
        method: str,
        url: str,
        data: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: int = config.elastic.elastic_timeout,
    ):
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.request(
                method=method.upper(),
                url=url,
                json=data,
                params=params,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
