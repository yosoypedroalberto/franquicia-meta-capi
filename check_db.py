import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

async def check():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client.get_database("franquicia_db")
    count = await db.partners.count_documents({})
    print(f"\n📊 ESTADO DE LA NUBE")
    print(f"-------------------")
    print(f"Socios registrados: {count}")
    async for partner in db.partners.find():
        print(f"👤 Socio: {partner['slug']} | Pixel: {partner['pixel_id']}")
    client.close()

if __name__ == "__main__":
    asyncio.run(check())
