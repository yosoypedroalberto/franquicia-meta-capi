from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from app.config import settings
from motor.motor_asyncio import AsyncIOMotorClient
import requests, time, hashlib, uvicorn

templates = Jinja2Templates(directory="app/templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.database = app.mongodb_client.get_database("franquicia_db")
    print(f"🚀 SISTEMA NUBE INICIADO: {settings.PROJECT_NAME}")
    yield
    app.mongodb_client.close()

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

def hash_data(data):
    if not data: return None
    return hashlib.sha256(data.strip().lower().encode('utf-8')).hexdigest()

async def send_meta_event(pixel_id, event_name, user_data, custom_data):
    url = f"https://graph.facebook.com/v18.0/{pixel_id}/events"
    payload = {
        "data": [{"event_name": event_name, "event_time": int(time.time()), "user_data": user_data, "custom_data": custom_data, "action_source": "website"}],
        "access_token": settings.FB_ACCESS_TOKEN
    }
    try: requests.post(url, json=payload)
    except: pass

@app.get("/{partner_slug}", response_class=HTMLResponse)
async def track_lead(partner_slug: str, request: Request):
    partner = await app.database.partners.find_one({"slug": partner_slug})
    if not partner: raise HTTPException(status_code=404)
    user_data = {"em": hash_data("lead@test.com"), "client_ip_address": request.client.host, "client_user_agent": request.headers.get("user-agent")}
    await send_meta_event(partner["pixel_id"], "Lead", user_data, {})
    return templates.TemplateResponse("index.html", {"request": request, "pixel_id": partner["pixel_id"], "partner_name": partner["name"], "telegram_link": partner.get("telegram_link", "https://google.com")})

@app.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    return {"status": "ok"}
