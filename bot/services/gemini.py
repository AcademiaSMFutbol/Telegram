import logging
import google.generativeai as genai
from bot.config import GEMINI_API_KEY
from bot.data.knowledge_base import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

_model = None
_chats: dict[int, genai.ChatSession] = {}


def _get_model() -> genai.GenerativeModel:
    global _model
    if _model is None:
        genai.configure(api_key=GEMINI_API_KEY)
        _model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_PROMPT,
        )
    return _model


def _get_chat(chat_id: int) -> genai.ChatSession:
    if chat_id not in _chats:
        _chats[chat_id] = _get_model().start_chat(history=[])
    return _chats[chat_id]


async def ask(chat_id: int, message: str) -> str:
    if not GEMINI_API_KEY:
        return (
            "Lo siento, el asistente IA no está disponible en este momento. "
            "Contacta directamente al <b>+34 625 468 296</b>."
        )
    try:
        chat = _get_chat(chat_id)
        response = await chat.send_message_async(message)
        return response.text
    except Exception as exc:
        logger.error("Gemini error for chat_id=%s: %s", chat_id, exc)
        return (
            "No he podido procesar tu pregunta ahora mismo. "
            "Llámanos al <b>+34 625 468 296</b> y te atendemos encantados."
        )
