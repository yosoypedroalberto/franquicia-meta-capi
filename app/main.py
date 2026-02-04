# main.py (Template V7.0 context passing)
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
import os

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["franquicia_db"]
partners_collection = db["partners"]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, partner: str = None):
    partner_data = None
    if partner:
        partner_data = partners_collection.find_one({"name": partner})
    context = {
        "request": request,
        "partner_name": partner_data["name"] if partner_data else None,
        "pixel_id": partner_data["pixel_id"] if partner_data else None,
        "telegram_link": partner_data["telegram_link"] if partner_data else None,
    }
    return templates.TemplateResponse("index.html", context)

@app.post("/", response_class=HTMLResponse)
async def submit_form(request: Request, partner: str = Form(...)):
    partner_data = partners_collection.find_one({"name": partner})
    context = {
        "request": request,
        "partner_name": partner_data["name"] if partner_data else None,
        "pixel_id": partner_data["pixel_id"] if partner_data else None,
        "telegram_link": partner_data["telegram_link"] if partner_data else None,
    }
    return templates.TemplateResponse("index.html", context)
