import asyncio
import logging
from aiohttp import web
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from bot.config import TELEGRAM_BOT_TOKEN, PORT
from bot.services.subscribers import init_db
from bot.handlers import start, info, faq, admin

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def _run_health_server() -> None:
    async def health(_: web.Request) -> web.Response:
        return web.Response(text="OK")

    app = web.Application()
    app.router.add_get("/", health)
    app.router.add_get("/health", health)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", PORT).start()
    logger.info("Health server listening on port %s", PORT)


async def main() -> None:
    init_db()

    await _run_health_server()

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # ── Comandos públicos ────────────────────────────────────────
    application.add_handler(CommandHandler("start", start.handle))
    application.add_handler(CommandHandler("avisos", start.handle_avisos))
    application.add_handler(CommandHandler("baja", start.handle_baja))
    application.add_handler(CommandHandler("info", info.handle_info))
    application.add_handler(CommandHandler("horarios", info.handle_horarios))
    application.add_handler(CommandHandler("precios", info.handle_precios))
    application.add_handler(CommandHandler("contacto", info.handle_contacto))

    # ── Comandos de administrador ────────────────────────────────
    application.add_handler(CommandHandler("avisar", admin.handle_avisar))
    application.add_handler(CommandHandler("publicar", admin.handle_publicar))
    application.add_handler(CommandHandler("suscriptores", admin.handle_suscriptores))

    # ── FAQ con IA (mensajes de texto libres) ────────────────────
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, faq.handle)
    )

    logger.info("Bot iniciado — polling activo")
    await application.initialize()
    await application.start()
    await application.updater.start_polling(allowed_updates=["message"])

    await asyncio.Event().wait()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
