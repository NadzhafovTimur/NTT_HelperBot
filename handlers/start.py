from telebot import types


def register_start_handlers(bot):
  @bot.message_handler(commands=["start"])
  def start_message(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="ДР", callback_data="btn1")
    markup.add(btn1)
    bot.send_message(message.chat.id, "Привет! Я твой персональный помощник.\nЯ помогу чем смогу. Что хочешь сделать?", reply_markup=markup,)

  @bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
  def back_to_main_menu(call):
    bot.answer_callback_query(call.id)
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="ДР", callback_data="btn1")
    markup.add(btn1)
    bot.edit_message_text(text=("Привет! Я твой персональный помощник.\nЯ помогу чем смогу. Что хочешь сделать?"), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup,)