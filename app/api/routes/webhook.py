from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse
from app.core.config import settings

router = APIRouter()

@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(default=None, alias="hub.mode"),
    hub_challenge: str = Query(default=None, alias="hub.challenge"),
    hub_verify_token: str = Query(default=None, alias="hub.verify_token")
):

    if hub_mode == "subscribe" and hub_verify_token == settings.verify_token:
        return PlainTextResponse(content=hub_challenge)

    raise HTTPException(status_code=403, detail="Invalid verify token")


@router.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()

    print("-------------WEBHOOK RECEIVED-------------------")
    print(payload)
    print("--------------------------------")

    return {"status": "received"}