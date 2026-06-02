import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType, ParseMode
from bot.services.gemini import ask

logger = logging.getLogger(__name__)

_BOT_USERNAME: str | None = None


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global _BOT_USERNAME

    message = update.message
    if not message or not message.text:
        return

    chat_type = update.effective_chat.type

    # In groups: only respond when mentioned or replying to the bot
    if chat_type in (ChatType.GROUP, ChatType.SUPERGROUP):
        if _BOT_USERNAME is None:
            me = await context.bot.get_me()
            _BOT_USERNAME = f"@{me.username}"

        mentioned = _BOT_USERNAME and _BOT_USERNAME.lower() in message.text.lower()
        reply_to_bot = (
            message.reply_to_message
            and message.reply_to_message.from_user
            and message.reply_to_message.from_user.id == context.bot.id
        )
        if not mentioned and not reply_to_bot:
            return

        # Strip the mention from the text before sending to Gemini
        text = message.text.replace(_BOT_USERNAME, "").strip()
    else:
        text = message.text

    if not text:
        return

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    response = await ask(chat_id=update.effective_chat.id, message=text)
    await message.reply_html(response)
