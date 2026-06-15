import httpx
from fastapi import FastAPI, Query, Response

app = FastAPI(title="proxy-checker")


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/health")
async def check_socks(
    proxy: str = Query(...),
    check_url: str = Query(default="https://ifconfig.me/ip"),
    timeout: float = Query(default=5.0),
):
    try:
        async with httpx.AsyncClient(proxy=proxy) as client:
            r = await client.get(check_url, timeout=timeout)
            return {
                "status": "ok",
                "proxy": proxy,
                "check_url": check_url,
                "timeout": timeout,
                "response": r.text.strip(),
            }
    except Exception as e:
        return Response(status_code=503, content=str(e))
