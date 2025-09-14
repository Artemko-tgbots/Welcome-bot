import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties

API_TOKEN = "ТВОЙ_ТОКЕН_БОТА"

# Список каналів для пропозицій (посилання)
CHANNELS = [
    {"name": "Канал 1", "link": "https://t.me/example1"},
    {"name": "Канал 2", "link": "https://t.me/example2"},
]

# Ініціалізація бота під aiogram 3.10+
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# --- Функція перевірки підписок ---
async def check_subscriptions(user_id):
    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(ch["link"], user_id)
            if member.status == "left":
                return False
        except Exception:
            return False
    return True

# --- Обробка заявки на вступ ---
@dp.chat_join_request()
async def join_request_handler(event: types.ChatJoinRequest):
    user_id = event.from_user.id
    chat_title = event.chat.title

    try:
        # Формуємо текст з усіма каналами
        text = f"👋 Привіт!\nДякуємо за заявку у канал <b>{chat_title}</b>!\n\n"
        text += "Перш ніж отримати доступ, підпишись на наші канали:\n"
        for ch in CHANNELS:
            text += f"👉 <a href='{ch['link']}'>{ch['name']}</a>\n"

        text += "\nПісля підписки повідом нас знову, і ми дамо доступ."

        await bot.send_message(chat_id=user_id, text=text)

    except Exception as e:
        print(f"Не вдалося написати користувачу {user_id}: {e}")

    # ❌ НЕ схвалюємо заявку автоматично
    # Якщо хочеш схвалювати після перевірки підписок, можна:
    # if await check_subscriptions(user_id):
    #     await event.approve()
    # else:
    #     await event.decline()


# --- Старт бота ---
async def main():
    print("Бот запущений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
