# main.py (Template V7.0 context passing example)
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    partner_name = os.getenv("PARTNER_NAME", "")
    pixel_id = os.getenv("PIXEL_ID", "")
    telegram_link = os.getenv("TELEGRAM_LINK", "")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "partner_name": partner_name,
            "pixel_id": pixel_id,
            "telegram_link": telegram_link
        }
    )

@app.post("/", response_class=HTMLResponse)
async def submit_form(request: Request, name: str = Form(...), phone: str = Form(...)):
    partner_name = os.getenv("PARTNER_NAME", "")
    pixel_id = os.getenv("PIXEL_ID", "")
    telegram_link = os.getenv("TELEGRAM_LINK", "")
    # Aquí puedes agregar lógica para manejar el formulario
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "partner_name": partner_name,
            "pixel_id": pixel_id,
            "telegram_link": telegram_link,
            "form_submitted": True,
            "name": name,
            "phone": phone
        }
    )
