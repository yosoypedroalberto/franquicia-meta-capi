import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

async def update():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client.get_database("franquicia_db")
    
    # Sincronizamos el Pixel real detectado previamente
    pixel_real = "3342222025931480"
    slug = "pionero-01"
    
    await db.partners.update_one(
        {"slug": slug},
        {"$set": {"pixel_id": pixel_real, "name": "Socio Pionero Real"}},
        upsert=True
    )
    print(f"\n✅ DATOS SINCRONIZADOS EN ATLAS")
    print(f"Socio: {slug} ahora tiene el Pixel real: {pixel_real}")
    client.close()

if __name__ == "__main__":
    asyncio.run(update())
