import os
import asyncio
import threading
import logging
import nest_asyncio
from pyrogram import Client
from pyrogram.types import Message

nest_asyncio.apply()
logging.basicConfig(level=logging.INFO)

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

GROUP_IDS = list(map(int, os.getenv("GROUP_ID", "").split(",")))
FRIENDS = list(map(int, os.getenv("FRIENDS", "").split(",")))
BLACKWORDS = os.getenv("BLACKWORDS", "").split(",")

app = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

@app.on_message()
async def handle_message(client: Client, message: Message):
    if not message.chat or message.chat.id not in GROUP_IDS:
        return

    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else None
    content = (message.text or "") + " " + (message.caption or "")

    if message.text and message.text.strip().lower().startswith("/where"):
        user_id_str = str(user_id) if user_id else "No disponible"
        chat_id_str = str(chat_id)
        await message.reply(
            f"User: {user_id_str}\nChat: {chat_id_str}",
            quote=True
        )
        return

    if not user_id:
        print("Mensaje de admin anónimo, no se borra.")
        return

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
    print("Bot iniciado y escuchando mensajes...")
    await asyncio.Event().wait()

def run_bot():
    asyncio.run(main())

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    print("Hilo del bot lanzado correctamente.")
    bot_thread.join()
