import os
import requests
from dotenv import load_dotenv
import time

load_dotenv()
token = os.getenv("FB_ACCESS_TOKEN")
pixel_id = "3342222025931480"

print(f"🔑 Probando con Pixel ID: {pixel_id}")
print("📡 Conectando con Meta Graph API...")

url = f"https://graph.facebook.com/v18.0/{pixel_id}/events"
payload = {
    "data": [
        {
            "event_name": "Lead",
            "event_time": int(time.time()),
            "user_data": {
                # Solo enviamos el email encriptado (test@test.com)
                "em": "7b17fb0bd173f625b58636fb796407c22b3d16fc78302d79f0fd30c2fc2fc068"
            },
            "custom_data": {
                "currency": "USD",
                "value": 10.0,
                "status": "PRUEBA_EXITOSA_FINAL"
            }
        }
    ],
    "access_token": token
}

try:
    response = requests.post(url, json=payload)
    data = response.json()
    
    if response.status_code == 200:
        print("\n✅ ¡ÉXITO TOTAL! (200 OK)")
        print(f"🎉 Eventos recibidos: {data.get('events_received')}")
    else:
        print(f"\n❌ ERROR ({response.status_code}):")
        print(data)

except Exception as e:
    print(f"\n❌ Error de conexión: {e}")
