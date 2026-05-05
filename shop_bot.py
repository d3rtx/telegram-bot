from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8256171705:AAH01z6TohMmVnBkk2qVx7KG81g1DA5_OM8"


# ===============================
# ГОРОДА РОССИИ (пример)
# ===============================
cities = [
    "Москва", "Санкт-Петербург", "Казань", "Новосибирск",
    "Екатеринбург", "Краснодар", "Сочи", "Ростов-на-Дону",
    "Самара", "Омск", "Челябинск", "Уфа",
    "Пермь", "Воронеж", "Волгоград", "Красноярск",
    "Тюмень", "Иркутск", "Хабаровск", "Владивосток"
]

# ===============================
# РАЙОНЫ ГОРОДОВ
# ===============================
districts = {
    "Москва": ["ЦАО", "САО", "ЮАО", "ЗАО", "ВАО"],
    "Санкт-Петербург": ["Центральный", "Приморский", "Московский"],
    "Казань": ["Советский", "Приволжский", "Авиастроительный"]
}


# ===============================
# ГЛАВНОЕ МЕНЮ
# ===============================
async def main_menu(update, context):

    keyboard = [
        [InlineKeyboardButton("🛒 Купить", callback_data="buy")],
        [InlineKeyboardButton("⭐ Отзывы", callback_data="reviews")],
        [InlineKeyboardButton("👥 Группа", url="https://t.me/your_group")]
    ]

    markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            "Добро пожаловать в магазин",
            reply_markup=markup
        )
    else:
        await update.callback_query.edit_message_text(
            "Добро пожаловать в магазин",
            reply_markup=markup
        )


# ===============================
# СПИСОК ГОРОДОВ С ПАГИНАЦИЕЙ
# ===============================
async def cities_menu(query, page=0):

    per_page = 5
    start = page * per_page
    end = start + per_page

    keyboard = []

    for city in cities[start:end]:
        keyboard.append(
            [InlineKeyboardButton(city, callback_data=f"city_{city}")]
        )

    navigation = []

    if start > 0:
        navigation.append(
            InlineKeyboardButton("⬅️", callback_data=f"cities_{page-1}")
        )

    if end < len(cities):
        navigation.append(
            InlineKeyboardButton("➡️", callback_data=f"cities_{page+1}")
        )

    if navigation:
        keyboard.append(navigation)

    keyboard.append(
        [InlineKeyboardButton("⬅️ Назад", callback_data="menu")]
    )

    await query.edit_message_text(
        "Выберите город:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ===============================
# МЕНЮ РАЙОНОВ
# ===============================
async def districts_menu(query, city):

    city_districts = districts.get(city, ["Район 1", "Район 2"])

    keyboard = []

    for d in city_districts:
        keyboard.append(
            [InlineKeyboardButton(d, callback_data="district")]
        )

    keyboard.append(
        [InlineKeyboardButton("⬅️ Города", callback_data="buy")]
    )

    await query.edit_message_text(
        f"Город: {city}\nВыберите район:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ===============================
# START
# ===============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await main_menu(update, context)


# ===============================
# ОБРАБОТКА КНОПОК
# ===============================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "buy":
        await cities_menu(query, 0)

    elif data.startswith("cities_"):
        page = int(data.split("_")[1])
        await cities_menu(query, page)

    elif data.startswith("city_"):
        city = data.replace("city_", "")
        await districts_menu(query, city)

    elif data == "menu":
        await main_menu(update, context)

    elif data == "reviews":
        keyboard = [
            [InlineKeyboardButton("⬅️ Назад", callback_data="menu")]
        ]

        await query.edit_message_text(
            "Отзывы клиентов:\n⭐️⭐️⭐️⭐️⭐️",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# ===============================
# ЗАПУСК
# ===============================
def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    print("Бот запущен")
    app.run_polling()


if __name__ == "__main__":
    main()
    