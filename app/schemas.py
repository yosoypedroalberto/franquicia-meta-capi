from pydantic import BaseModel, Field, BeforeValidator, EmailStr
from typing import Optional, List, Annotated, Dict, Any
from datetime import datetime

# --- EL TRADUCTOR MAGICO ---
PyObjectId = Annotated[str, BeforeValidator(str)]

# =======================
# 👥 SOCIOS (PARTNERS)
# =======================
class PartnerBase(BaseModel):
    name: str
    slug: str
    pixel_id: Optional[str] = None
    is_active: bool = True

class PartnerCreate(PartnerBase):
    pass

class PartnerDB(PartnerBase):
    id: PyObjectId = Field(..., alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

# =======================
# 🎣 CLIENTES (LEADS)
# =======================
class LeadBase(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    full_name: Optional[str] = None
    # Aquí guardaremos toda la data "cruda" que mande Facebook por si acaso
    raw_data: Dict[str, Any] = {}

class LeadCreate(LeadBase):
    """Lo que recibimos de afuera"""
    partner_slug: Optional[str] = None

class LeadDB(LeadBase):
    """Lo que guardamos en Mongo"""
    id: PyObjectId = Field(..., alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    assigned_to: Optional[str] = None
    status: str = "NEW"

    class Config:
        populate_by_name = True
