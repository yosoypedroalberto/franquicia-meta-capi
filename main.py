# Código funcional V7.0 ajustado para templates

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Configuración de CORS (opcional, puedes ajustar los orígenes permitidos)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos (si tienes una carpeta 'static')
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuración de templates (asegúrate de tener la carpeta 'templates')
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/pedro", response_class=HTMLResponse)
def pedro(request: Request):
    return templates.TemplateResponse("pedro.html", {"request": request})

@app.post("/procesar_formulario", response_class=HTMLResponse)
def procesar_formulario(request: Request, nombre: str = Form(...), edad: int = Form(...)):
    # Aquí puedes procesar los datos del formulario
    mensaje = f"¡Hola, {nombre}! Tienes {edad} años."
    return templates.TemplateResponse("resultado.html", {"request": request, "mensaje": mensaje})

# Puedes agregar más rutas según tus necesidades

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
