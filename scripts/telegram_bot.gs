/**
 * SM Academia — Bot Telegram via Google Apps Script
 *
 * INSTRUCCIONES DE DESPLIEGUE:
 * 1. Abre script.google.com → Nuevo proyecto → pega este código
 * 2. Menú: Proyecto → Propiedades del proyecto → Propiedades de script
 *    Añade dos propiedades:
 *      TELEGRAM_TOKEN  →  tu token del bot
 *      GEMINI_KEY      →  tu API key de Google AI Studio
 * 3. Menú: Implementar → Nueva implementación
 *    Tipo: Aplicación web
 *    Ejecutar como: Yo
 *    Quién tiene acceso: Cualquiera
 *    → Copia la URL de implementación
 * 4. En el editor, pega la URL en setWebhook() y ejecútala una vez
 */

const PROPS = PropertiesService.getScriptProperties();
const TOKEN = PROPS.getProperty('TELEGRAM_TOKEN');
const GEMINI_KEY = PROPS.getProperty('GEMINI_KEY');
const TG = `https://api.telegram.org/bot${TOKEN}`;

const SYSTEM_PROMPT = `Eres el asistente virtual de SM Academia, una academia de formación deportiva en Las Palmas de Gran Canaria.

SM Academia tiene dos ramas:
- Academia SM Fútbol: tecnificación individual de fútbol para jugadores de 6 a 13 años, metodología MEC.
- SM Extraescolares: actividad deportiva extraescolar en colegios (actualmente CEIP Escaleritas).

METODOLOGÍA MEC:
M - Motivación: cada sesión debe ser el mejor momento del día del alumno.
E - Esfuerzo: valoramos el trabajo diario por encima del talento.
C - Constancia: creamos hábitos, disciplina y autonomía más allá del deporte.
Filosofía: "Formamos personas, luego lo que sean."

TARIFAS Academia SM Fútbol:
- 1 sesión/semana: 55 €/mes
- 2 sesiones/semana: 110 €/mes
- 3 sesiones/semana: 160 €/mes
- Sesión suelta: 15 €
Extraescolares: tarifas según centro o AMPA.

INSCRIPCIÓN: formulario en https://academiasmfutbol.com/inscripcion-academia-sm-futbol/
Para cualquier gestión necesitamos: nombre del alumno, nombre del tutor legal, aceptación RGPD.

HORARIOS: sesiones de entrenamiento de lunes a viernes. Para horario exacto del grupo, contactar directamente.

CONTACTO:
Teléfono: +34 625 468 296
Web: academiasmfutbol.com
Canal Telegram: @academiasmfutbol2

Responde siempre en español, de forma directa y cercana. Máximo 3-4 párrafos.
Si no sabes algo con certeza, di que contacten al +34 625 468 296.
No inventes información que no esté aquí.`;


// ─── Punto de entrada del webhook ───────────────────────────────────────────

function doPost(e) {
  try {
    const update = JSON.parse(e.postData.contents);
    handleUpdate(update);
  } catch (err) {
    Logger.log('doPost error: ' + err.toString());
  }
  return ContentService.createTextOutput('OK');
}


// ─── Router principal ────────────────────────────────────────────────────────

function handleUpdate(update) {
  if (update.callback_query) {
    const cb = update.callback_query;
    answerCallback(cb.id);
    handleCallback(cb.message.chat.id, cb.data);
    return;
  }

  if (update.message && update.message.text) {
    const chatId = update.message.chat.id;
    const text = update.message.text.trim();

    if (text === '/start' || text === '/menu' || text.startsWith('/start ')) {
      handleStart(chatId);
    } else if (!text.startsWith('/')) {
      handleFreeText(chatId, text);
    }
  }
}


// ─── Handlers ────────────────────────────────────────────────────────────────

function handleStart(chatId) {
  const text =
    'Hola! Bienvenido al bot oficial de SM Academia.\n\n' +
    'Somos una academia de formación deportiva en Las Palmas de Gran Canaria:\n\n' +
    'Academia SM Fútbol — Tecnificación individual, jugadores de 6 a 13 años\n' +
    'SM Extraescolares — Actividad deportiva en colegios\n\n' +
    '¿En qué podemos ayudarte? Escoge una opción o escríbenos directamente.';

  sendMessage(chatId, text, {
    inline_keyboard: [
      [{ text: 'Metodología MEC', callback_data: 'metodologia' }],
      [{ text: 'Inscripción',     callback_data: 'inscripcion' }],
      [{ text: 'Tarifas',         callback_data: 'pagos'       }],
      [{ text: 'Contacto',        callback_data: 'contacto'    }]
    ]
  });
}

function handleCallback(chatId, data) {
  switch (data) {
    case 'metodologia':
      sendMessage(chatId,
        'Metodología MEC — SM Academia\n\n' +
        'Trabajamos el desarrollo individual de cada niño, priorizando el aprendizaje real sobre el resultado inmediato.\n\n' +
        'M — Motivación\nCada sesión tiene que ser el mejor momento del día del alumno.\n\n' +
        'E — Esfuerzo\nValoramos el trabajo diario por encima del talento.\n\n' +
        'C — Constancia\nCreamos hábitos, disciplina y autonomía más allá del deporte.\n\n' +
        'Formamos personas, luego lo que sean.\n\n' +
        'Escribe /menu para volver al inicio.'
      );
      break;

    case 'inscripcion':
      sendMessage(chatId,
        'Inscripción en SM Academia\n\n' +
        'Para apuntar a tu hijo/a:\n\n' +
        '1. Rellena el formulario online\n' +
        '2. Datos del alumno y tutor legal\n' +
        '3. Aceptación uso de imagen (RGPD)\n' +
        '4. La dirección confirma la plaza\n\n' +
        '¿Dudas? Llámanos al +34 625 468 296.',
        { inline_keyboard: [[{ text: 'Ir al formulario', url: 'https://academiasmfutbol.com/inscripcion-academia-sm-futbol/' }]] }
      );
      break;

    case 'pagos':
      sendMessage(chatId,
        'Tarifas — Academia SM Fútbol\n\n' +
        '1 sesión/semana: 55 €/mes\n' +
        '2 sesiones/semana: 110 €/mes\n' +
        '3 sesiones/semana: 160 €/mes\n' +
        'Sesión suelta: 15 €\n\n' +
        'Extraescolares: tarifas según centro o AMPA.\n\n' +
        'Tel: +34 625 468 296\n\n' +
        'Escribe /menu para volver al inicio.'
      );
      break;

    case 'contacto':
      sendMessage(chatId,
        'Contacto — SM Academia\n\n' +
        'Escríbenos aquí mismo con:\n\n' +
        '• Tu nombre y el del alumno\n' +
        '• Si es Fútbol o Extraescolares\n' +
        '• Tu consulta\n\n' +
        'Te respondemos lo antes posible.\n\n' +
        'Tel: +34 625 468 296\n\n' +
        '¡Gracias por confiar en SM Academia!'
      );
      break;
  }
}

function handleFreeText(chatId, text) {
  const response = askGemini(text);
  sendMessage(chatId, response);
}


// ─── Gemini API ──────────────────────────────────────────────────────────────

function askGemini(userText) {
  const url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=' + GEMINI_KEY;

  const payload = {
    contents: [{
      role: 'user',
      parts: [{ text: SYSTEM_PROMPT + '\n\nPregunta: ' + userText }]
    }],
    generationConfig: {
      temperature: 0.6,
      maxOutputTokens: 400
    }
  };

  try {
    const res = UrlFetchApp.fetch(url, {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    });
    const json = JSON.parse(res.getContentText());
    return json.candidates[0].content.parts[0].text.trim();
  } catch (err) {
    Logger.log('Gemini error: ' + err.toString());
    return 'No he podido procesar tu consulta ahora mismo. Llámanos al +34 625 468 296 o escríbenos y te atendemos enseguida.';
  }
}


// ─── Telegram API helpers ────────────────────────────────────────────────────

function sendMessage(chatId, text, replyMarkup) {
  const payload = { chat_id: chatId, text: text };
  if (replyMarkup) payload.reply_markup = replyMarkup;

  UrlFetchApp.fetch(TG + '/sendMessage', {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  });
}

function answerCallback(callbackQueryId) {
  UrlFetchApp.fetch(TG + '/answerCallbackQuery', {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify({ callback_query_id: callbackQueryId }),
    muteHttpExceptions: true
  });
}


// ─── Configuración del webhook (ejecutar UNA vez tras desplegar) ─────────────

function setWebhook() {
  const WEB_APP_URL = 'PEGA_AQUI_TU_URL_DE_IMPLEMENTACION';
  const res = UrlFetchApp.fetch(TG + '/setWebhook?url=' + WEB_APP_URL);
  Logger.log(res.getContentText());
}

function deleteWebhook() {
  const res = UrlFetchApp.fetch(TG + '/deleteWebhook');
  Logger.log(res.getContentText());
}
