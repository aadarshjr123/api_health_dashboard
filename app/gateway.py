from fastapi import FastAPI, Request
import httpx

gateway = FastAPI()


@gateway.api_route("/{path:path}", methods=["GET", "POST"])
async def proxy(request: Request, path: str):
    target = f"http://api:8000/{path}"

    # Forward Authorization header if it exists
    headers = {}
    auth_header = request.headers.get("Authorization")
    if auth_header:
        headers["Authorization"] = auth_header

    async with httpx.AsyncClient() as client:

        if request.method == "GET":
            resp = await client.get(
                target, params=request.query_params, headers=headers
            )

        else:  # POST
            # Safe JSON extraction
            try:
                body = await request.json()
            except:
                body = None

            if body:
                resp = await client.post(
                    target, json=body, headers=headers, params=request.query_params
                )
            else:
                # POST with NO body → just forward query params
                resp = await client.post(
                    target, headers=headers, params=request.query_params
                )

    return resp.json()
