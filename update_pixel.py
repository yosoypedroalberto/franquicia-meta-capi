import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def update():
    # Conexión Local Explícita
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.get_database("franquicia_db")
    
    pixel_id = "3342222025931480"
    slug = "pionero-01"
    
    await db.partners.update_one(
        {"slug": slug},
        {"$set": {"pixel_id": pixel_id, "name": "Socio Pionero Real"}},
        upsert=True
    )
    print(f"✅ LISTO: El socio '{slug}' ahora usa el Pixel {pixel_id}")
    client.close()

if __name__ == "__main__":
    asyncio.run(update())
