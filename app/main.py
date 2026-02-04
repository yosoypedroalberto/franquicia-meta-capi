from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# Configuración de MongoDB
MONGO_URL = os.getenv("MONGODB_URL", "mongodb+srv://owner_user:mAe1OgQplAgQCFkP@cluster0.tow6wmt.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGO_URL)
db = client["franquicia_db"]
partners_collection = db["partners"]

@app.get("/{partner_slug}", response_class=HTMLResponse)
async def read_item(request: Request, partner_slug: str):
    # 1. Buscar al socio en la base de datos
    partner = partners_collection.find_one({"slug": partner_slug})
    
    # 2. Manejo de error 404 si no existe
    if not partner:
        return HTMLResponse(content="<h1>Partner no encontrado</h1>", status_code=404)

    # 3. Construcción del Contexto (Aquí estaba el error antes)
    # Enviamos explícitamente cada variable que pide el HTML V7.0
    context = {
        "request": request,
        "partner_name": partner.get("name", "Flujo de Efectivo"),
        "pixel_id": partner.get("pixel_id", ""),
        "telegram_link": partner.get("telegram_link", "https://t.me/Flujo_Efectivo_Real_bot")
    }

    # 4. Renderizar la plantilla con los datos seguros
    return templates.TemplateResponse("index.html", context)
