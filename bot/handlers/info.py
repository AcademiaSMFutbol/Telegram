from telegram import Update
from telegram.ext import ContextTypes
from bot.data.knowledge_base import (
    INFO_MESSAGE,
    CONTACTO_MESSAGE,
    HORARIOS_MESSAGE,
    PRECIOS_MESSAGE,
)


async def handle_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(INFO_MESSAGE)


async def handle_contacto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(CONTACTO_MESSAGE)


async def handle_horarios(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(HORARIOS_MESSAGE)


async def handle_precios(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(PRECIOS_MESSAGE)
