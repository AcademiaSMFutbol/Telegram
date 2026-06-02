"""
Script autónomo para publicaciones programadas en el canal.
Se ejecuta desde GitHub Actions — no necesita el bot en marcha.
"""
import asyncio
import os
import sys

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHANNEL = os.environ.get("CHANNEL_ID", "")


async def main() -> None:
    if not TOKEN or not CHANNEL:
        print("ERROR: TELEGRAM_BOT_TOKEN y CHANNEL_ID son obligatorios")
        sys.exit(1)

    from telegram import Bot
    from bot.data.scheduled_messages import get_message_for_today

    message = get_message_for_today()
    if not message:
        print("Hoy no hay mensaje programado para este día de la semana.")
        return

    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHANNEL, text=message, parse_mode="HTML")
    print(f"Publicado en {CHANNEL}: {message[:60]}...")


if __name__ == "__main__":
    asyncio.run(main())
