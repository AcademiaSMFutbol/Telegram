from datetime import datetime


WEEKLY_MESSAGES = {
    0: (
        "⚽ <b>¡Semana de entrenos en marcha!</b>\n\n"
        "Recordad que los entrenamientos comienzan hoy. "
        "Llegad 5 minutos antes, con botines, espinilleras y agua. ¡A por ella!\n\n"
        "🟢 <b>SM Academia</b> · <i>Formamos personas, luego lo que sean</i>"
    ),
    2: (
        "💪 <b>Miércoles de tecnificación</b>\n\n"
        "Hoy toca trabajo técnico. Cada repetición cuenta — ¡darlo todo en el entrenamiento!\n\n"
        "🟢 <b>SM Academia</b>"
    ),
    4: (
        "🏆 <b>¡Último entreno de la semana!</b>\n\n"
        "Viernes de fútbol. Termina la semana con energía y esfuerzo máximo. "
        "¡Nos vemos en el campo!\n\n"
        "🟢 <b>SM Academia</b>"
    ),
    6: (
        "☀️ <b>¡Buenas tardes, familias!</b>\n\n"
        "Mañana arrancamos nueva semana de entrenamientos. "
        "¿Están los chavales preparados?\n\n"
        "🟢 <b>SM Academia</b> · academiasmfutbol.com"
    ),
}


def get_message_for_today() -> str | None:
    day = datetime.now().weekday()  # 0=Lunes … 6=Domingo
    return WEEKLY_MESSAGES.get(day)
