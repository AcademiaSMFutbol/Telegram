import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from bot.config import ADMIN_CHAT_IDS, CHANNEL_ID
from bot.services.subscribers import get_active_subscribers, count_active

logger = logging.getLogger(__name__)


def _is_admin(chat_id: int) -> bool:
    return chat_id in ADMIN_CHAT_IDS


async def handle_avisar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Broadcast a message to all subscribed users."""
    if not _is_admin(update.effective_chat.id):
        await update.message.reply_text("⛔ Solo disponible para administradores.")
        return

    if not context.args:
        await update.message.reply_html(
            "Uso: <code>/avisar Tu mensaje aquí</code>\n\n"
            "El mensaje se enviará a todas las familias suscritas."
        )
        return

    text = " ".join(context.args)
    broadcast_text = (
        f"📢 <b>Aviso de SM Academia</b>\n\n"
        f"{text}\n\n"
        f"📞 +34 625 468 296"
    )

    subscribers = get_active_subscribers()
    if not subscribers:
        await update.message.reply_text("No hay suscriptores activos aún.")
        return

    sent = 0
    failed = 0
    for chat_id in subscribers:
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=broadcast_text,
                parse_mode=ParseMode.HTML,
            )
            sent += 1
        except Exception as exc:
            logger.warning("Failed to send to %s: %s", chat_id, exc)
            failed += 1

    await update.message.reply_html(
        f"✅ <b>Aviso enviado</b>\n"
        f"• Enviados: {sent}\n"
        f"• Fallidos: {failed}"
    )


async def handle_publicar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Post a message to the configured channel."""
    if not _is_admin(update.effective_chat.id):
        await update.message.reply_text("⛔ Solo disponible para administradores.")
        return

    if not CHANNEL_ID:
        await update.message.reply_text(
            "⚠️ No hay canal configurado. Añade CHANNEL_ID en los secretos."
        )
        return

    if not context.args:
        await update.message.reply_html(
            "Uso: <code>/publicar Tu mensaje para el canal</code>"
        )
        return

    text = " ".join(context.args)
    try:
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=text,
            parse_mode=ParseMode.HTML,
        )
        await update.message.reply_text("✅ Publicado en el canal.")
    except Exception as exc:
        logger.error("Failed to post to channel: %s", exc)
        await update.message.reply_text(
            f"❌ No se pudo publicar: {exc}\n\n"
            "Asegúrate de que el bot es administrador del canal."
        )


async def handle_suscriptores(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show subscriber count (admin only)."""
    if not _is_admin(update.effective_chat.id):
        await update.message.reply_text("⛔ Solo disponible para administradores.")
        return

    total = count_active()
    await update.message.reply_html(
        f"👥 <b>Suscriptores activos:</b> {total}"
    )
