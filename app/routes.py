from fastapi import APIRouter, HTTPException, Depends, Header, Request
from app.schemas import PartnerCreate, PartnerDB
from app.config import settings
from typing import List

# Creamos el "Enrutador" (como un pasillo de oficinas)
router = APIRouter()

# --- SEGURIDAD ---
# Este es el guardia. Verifica que quien llama tenga la llave maestra.
async def verify_admin_key(x_admin_token: str = Header(...)):
    if x_admin_token != settings.ADMIN_SECRET_KEY:
        raise HTTPException(status_code=403, detail="⛔ ACCESO DENEGADO: Llave maestra incorrecta")
    return x_admin_token

# --- ENDPOINT 1: CREAR SOCIO ---
# POST /admin/partners
@router.post("/partners", response_model=PartnerDB, status_code=201)
async def create_partner(
    partner: PartnerCreate, 
    request: Request, 
    authorized: str = Depends(verify_admin_key)
):
    """
    Registra un nuevo socio en la Base de Datos.
    Requiere Header 'x-admin-token' con la clave secreta.
    """
    db = request.app.mongodb["partners"] # Accedemos a la colección 'partners'

    # 1. Verificar si ya existe alguien con ese 'slug' (ej: juan)
    existing_partner = await db.find_one({"slug": partner.slug})
    if existing_partner:
        raise HTTPException(status_code=400, detail=f"El slug '{partner.slug}' ya está ocupado.")

    # 2. Convertir datos a formato diccionario para Mongo
    new_partner = partner.model_dump()
    
    # 3. Guardar en MongoDB
    result = await db.insert_one(new_partner)
    
    # 4. Recuperar el socio creado para confirmar
    created_partner = await db.find_one({"_id": result.inserted_id})
    return created_partner

# --- ENDPOINT 2: LISTAR SOCIOS ---
# GET /admin/partners
@router.get("/partners", response_model=List[PartnerDB])
async def list_partners(request: Request, authorized: str = Depends(verify_admin_key)):
    """Devuelve la lista de todos los socios registrados"""
    db = request.app.mongodb["partners"]
    partners = await db.find().to_list(1000)
    return partners
