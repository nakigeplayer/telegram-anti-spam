import os
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")
GROUP_ID = int(os.getenv("GROUP_ID"))
FRIENDS = list(map(int, os.getenv("FRIENDS", "").split(",")))

blackwords = os.getenv("BLACKWORDS", "").split(",")

app = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

@app.on_message(filters.chat(GROUP_ID))
async def check_message(client: Client, message: Message):
    if not message.from_user:
        print("Mensaje de admin anónimo, no se borra.")
        return

    user_id = message.from_user.id
    text = message.text or ""

    if any(word in text.lower() for word in blackwords):
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

app.run()
  
