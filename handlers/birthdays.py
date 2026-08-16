import re
from datetime import datetime
from database import load_data, save_data
from telebot import types


def register_birthday_handlers(bot):

  @bot.callback_query_handler(func=lambda call: call.data == "btn1")
  def birthday_bd_menu(call):
    bot.answer_callback_query(call.id)
    all_data = load_data()
    user_id = str(call.message.chat.id)
    user_info = all_data.get("users", {}).get(user_id, {})
    user_birthdays = user_info.get("birthdays", [])
    markup = types.InlineKeyboardMarkup()
    btn_add = types.InlineKeyboardButton(
        text="Добавить ДР", callback_data="add_birthdays"
    )
    btn_del = types.InlineKeyboardButton(
        text="Удалить ДР", callback_data="del_birthdays"
    )
    btn_back = types.InlineKeyboardButton(
        text="Назад", callback_data="back_to_main"
    )
    markup.add(btn_add)
    markup.add(btn_del)
    markup.add(btn_back)
    if not user_birthdays:
      text = "У вас еще нету ДР в списке. Хотите добавить?"
    else:
      text = "Ваш список ДР:\n" + "\n".join(
          [f"{item['name']} {item['date']}" for item in user_birthdays]
      )
      today = datetime.now().strftime("%d.%m")
      today_alt = datetime.now().strftime("%d:%m")
      for item in user_birthdays:
        if (
            isinstance(item, dict)
            and item.get("date") == today
            or item.get("date") == today_alt
        ):
          text += f"\n\nУ человека по имени {item['name']} сегодня ДР!"
    bot.edit_message_text(
        text=text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
    )

  @bot.callback_query_handler(func=lambda call: call.data == "add_birthdays")
  def add_birthday_start(call):
    bot.answer_callback_query(call.id)
    markup = types.InlineKeyboardMarkup()
    btn_cancel = types.InlineKeyboardButton(
        text="Отмена", callback_data="cancel_action"
    )
    markup.add(btn_cancel)
    msg = bot.send_message(
        call.message.chat.id,
        "Введите имя и дату рождения в формате ДД.ММ или ДД:ММ (например: Иван"
        " 20.10 или Иван 20:10):",
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, process_birthday_name)

  def process_birthday_name(message):
    user_id = str(message.chat.id)
    text = message.text.strip()
    match = re.match(r"^(.+)\s+(\d{2}[\.:]\d{2})$", text)
    if not match:
      bot.send_message(message.chat.id, "Неверный формат! Повторите попытку.")
      return
    name, date_str = match.groups()
    all_data = load_data()
    if user_id not in all_data["users"]:
      all_data["users"][user_id] = {"birthdays": []}
    user_birthdays = all_data["users"][user_id]["birthdays"]
    for item in user_birthdays:
      if (
          isinstance(item, dict)
          and item.get("name") == name
          and item.get("date") == date_str
      ):
        bot.send_message(
            message.chat.id, f"Запись {name} {date_str} уже есть в списке!"
        )
        return
    all_data["users"][user_id]["birthdays"].append(
        {"name": name, "date": date_str}
    )
    save_data(all_data)
    today = datetime.now().strftime("%d.%m")
    today_alt = datetime.now().strftime("%d:%m")
    bot.send_message(
        message.chat.id, f"Отлично! Успешно добавлено: {name} {date_str}"
    )
    if date_str == today or date_str == today_alt:
      bot.send_message(
          message.chat.id, f"У человека по имени {name} сегодня ДР!"
      )
    show_bd_menu_after_action(message, user_id, all_data)

  @bot.callback_query_handler(func=lambda call: call.data == "del_birthdays")
  def del_birthday_start(call):
    bot.answer_callback_query(call.id)
    all_data = load_data()
    user_id = str(call.message.chat.id)
    user_bithdays = (
        all_data.get("users", {}).get(user_id, {}).get("birthdays", [])
    )
    if not user_bithdays:
      bot.send_message(call.message.chat.id, "Ваш список пуст.")
      return
    markup = types.InlineKeyboardMarkup()
    btn_cancel = types.InlineKeyboardButton(
        text="Отмена", callback_data="cancel_action"
    )
    markup.add(btn_cancel)
    msg = bot.send_message(
        call.message.chat.id,
        "Введите имя и дату в формате ДД.ММ или ДД:ММ, чтобы удалить (например"
        " Иван 20.10)",
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, process_birthday_delete)

  def process_birthday_delete(message):
    user_id = str(message.chat.id)
    text = message.text.strip()
    match = re.match(r"^(.+)\s+(\d{2}[\.:]\d{2})$", text)
    if not match:
      bot.send_message(
          message.chat.id,
          "Неверный формат! Введите имя и дату в формате ДД.ММ или ДД:ММ.",
      )
      return
    name, date_str = match.groups()
    all_data = load_data()
    user_bithdays = (
        all_data.get("users", {}).get(user_id, {}).get("birthdays", [])
    )
    target_item = None
    for item in user_bithdays:
      if (
          isinstance(item, dict)
          and item.get("name") == name
          and item.get("date") == date_str
      ):
        target_item = item
        break
    if target_item:
      user_bithdays.remove(target_item)
      all_data["users"][user_id]["birthdays"] = user_bithdays
      save_data(all_data)
      bot.send_message(message.chat.id, f"Запись {name} {date_str} удалена!")
    else:
      bot.send_message(
          message.chat.id, f"Запись {name} {date_str} не найдена."
      )
    show_bd_menu_after_action(message, user_id, all_data)

  @bot.callback_query_handler(func=lambda call: call.data == "cancel_action")
  def cancel_action(call):
    bot.answer_callback_query(call.id)
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    bot.delete_message(
        chat_id=call.message.chat.id, message_id=call.message.message_id
    )

  def show_bd_menu_after_action(message, user_id, all_data):
    user_birthdays = (
        all_data.get("users", {}).get(user_id, {}).get("birthdays", [])
    )
    markup = types.InlineKeyboardMarkup()
    btn_add = types.InlineKeyboardButton(
        text="Добавить ДР", callback_data="add_birthdays"
    )
    btn_del = types.InlineKeyboardButton(
        text="Удалить ДР", callback_data="del_birthdays"
    )
    btn_back = types.InlineKeyboardButton(
        text="Назад", callback_data="back_to_main"
    )
    markup.add(btn_add)
    markup.add(btn_del)
    markup.add(btn_back)
    if not user_birthdays:
      text = "У вас еще нету ДР в списке. Хотите добавить?"
    else:
      text = "Ваш список ДР:\n" + "\n".join(
          [f"{item['name']} {item['date']}" for item in user_birthdays]
      )
      today = datetime.now().strftime("%d.%m")
      today_alt = datetime.now().strftime("%d:%m")
      for item in user_birthdays:
        if (
            isinstance(item, dict)
            and item.get("date") == today
            or item.get("date") == today_alt
        ):
          text += f"\n\nУ человека по имени {item['name']} сегодня ДР!"
    bot.send_message(message.chat.id, text, reply_markup=markup)