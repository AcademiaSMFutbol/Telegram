from telegram import Update
from telegram.ext import ContextTypes
from bot.data.knowledge_base import WELCOME_MESSAGE
from bot.services.subscribers import subscribe


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat_id = update.effective_chat.id

    is_new = subscribe(
        chat_id=chat_id,
        username=user.username,
        first_name=user.first_name,
    )

    if is_new:
        await update.message.reply_html(
            WELCOME_MESSAGE + "\n\n✅ <b>Te has suscrito a los avisos de SM Academia.</b>"
        )
    else:
        await update.message.reply_html(WELCOME_MESSAGE)


async def handle_avisos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat_id = update.effective_chat.id

    is_new = subscribe(
        chat_id=chat_id,
        username=user.username,
        first_name=user.first_name,
    )

    if is_new:
        await update.message.reply_html(
            "✅ <b>¡Suscripción activada!</b>\n\n"
            "A partir de ahora recibirás avisos sobre entrenamientos, "
            "cambios de horario y novedades de SM Academia.\n\n"
            "Puedes cancelarla en cualquier momento con /baja"
        )
    else:
        await update.message.reply_html(
            "Ya estás suscrito a los avisos. 👍\n"
            "Para darte de baja usa /baja"
        )


async def handle_baja(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from bot.services.subscribers import unsubscribe

    was_active = unsubscribe(update.effective_chat.id)
    if was_active:
        await update.message.reply_text(
            "Baja registrada. Ya no recibirás avisos de SM Academia.\n"
            "Si cambias de opinión, usa /avisos para suscribirte de nuevo."
        )
    else:
        await update.message.reply_text(
            "No estabas suscrito a los avisos.\n"
            "Usa /avisos para suscribirte."
        )
