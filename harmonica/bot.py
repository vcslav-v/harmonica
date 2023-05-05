import os

from loguru import logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes, filters)

from harmonica import harmonica

BOT_TOKEN = os.environ.get('BOT_TOKEN', '')


@logger.catch
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, new_msg=False) -> None:
    keyboard = []
    query = update.callback_query
    for note_1, note_2, note_3 in zip(harmonica.NOTES[::3], harmonica.NOTES[1::3], harmonica.NOTES[2::3]):
        keyboard.append([
            InlineKeyboardButton(note_1, callback_data=note_1),
            InlineKeyboardButton(note_2, callback_data=note_2),
            InlineKeyboardButton(note_3, callback_data=note_3)
        ])

    reply_markup = InlineKeyboardMarkup(keyboard)
    text = 'Какая у вас гармошка?'
    if query and not new_msg:
        await query.edit_message_text(text=text, reply_markup=reply_markup)
    elif new_msg:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text, reply_markup=reply_markup)


@logger.catch
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data in harmonica.NOTES:
        context.user_data['harmonica'] = query.data
        keyboard = []
        for scale in harmonica.SCALES:
            keyboard.append([
                InlineKeyboardButton(scale[1], callback_data=scale[0])
            ])
        keyboard.append([
            InlineKeyboardButton('Cancel', callback_data='cancel')
        ])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text='Какую гамму вы хотите играть?', reply_markup=reply_markup)
    elif query.data in [scale[0] for scale in harmonica.SCALES]:
        context.user_data['scale'] = query.data
        keyboard = []
        for tonic in harmonica.NOTES:
            position = harmonica.get_position(context.user_data['harmonica'], tonic)
            keyboard.append([
                InlineKeyboardButton(f'{tonic} ({position} position)', callback_data=f'tonic_{tonic}')
            ])
        keyboard.append([
            InlineKeyboardButton('Cancel', callback_data='cancel')
        ])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text='Выберите тонику?', reply_markup=reply_markup)

    elif query.data.startswith('tonic_'):
        tonic = query.data.split('_')[1]
        context.user_data['tonic'] = tonic
        scale = context.user_data['scale']
        harmonica_img = harmonica.get_harmonica(context.user_data['harmonica'], scale=harmonica.get_scale(scale, tonic))
        await query.edit_message_text(
            text=f'{context.user_data["harmonica"]} гармошка\n{context.user_data["tonic"]} {context.user_data["scale"]}',
            reply_markup=None
        )
        keyboard = [InlineKeyboardButton('Again', callback_data='again')]
        await query.message.reply_photo(harmonica_img, reply_markup=InlineKeyboardMarkup([keyboard]))

    elif query.data == 'cancel':
        await start(update, context)
    elif query.data == 'again':
        await start(update, context, new_msg=True)


@logger.catch
def main() -> None:

    '''Start the bot.'''
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start, filters.ChatType.PRIVATE))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()


if __name__ == '__main__':
    main()
