import os
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

GROUP_IDS = list(map(int, os.getenv("GROUP_ID", "").split(",")))

FRIENDS = list(map(int, os.getenv("FRIENDS", "").split(",")))
BLACKWORDS = os.getenv("BLACKWORDS", "").split(",")

app = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

@app.on_message(filters.chat(GROUP_IDS))
async def check_message(client: Client, message: Message):
    if not message.from_user:
        print("Mensaje de admin anónimo, no se borra.")
        return

    user_id = message.from_user.id

    content = (message.text or "") + " " + (message.caption or "")

    if any(word in content.lower() for word in BLACKWORDS):
        if user_id not in FRIENDS:
            try:
                await message.delete()
                print(f"Mensaje eliminado de {user_id}")
            except Exception as e:
                print(f"No se pudo eliminar el mensaje: {e}")
        else:
            print(f"Mensaje permitido de amigo {user_id}")
    else:
        print("Mensaje limpio.")
        
async def main():
    await app.start()
    await asyncio.Event().wait()
    
import asyncio
asyncio.run(main())
