# FastAPI backend for franquicia-meta-capi
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates configuration
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/pedro", response_class=HTMLResponse)
def pedro(request: Request):
    return templates.TemplateResponse("pedro.html", {"request": request})

@app.post("/procesar_formulario", response_class=HTMLResponse)
def procesar_formulario(request: Request, nombre: str = Form(...), edad: int = Form(...)):
    mensaje = f"¡Hola, {nombre}! Tienes {edad} años."
    return templates.TemplateResponse("resultado.html", {"request": request, "mensaje": mensaje})

# Add more routes as needed

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
