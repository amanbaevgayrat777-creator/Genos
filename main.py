import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = "8416729210:AAFQxUsJunPSGN49Zco5Py8mirZ5mwtJVo8"  # Bu joyga o'zingizning @BotFather dan olgan tokeningizni yozasiz

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Foydalanuvchi ma'lumotlari
user_data = {}
user_warnings = {}

# /start komandasi
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {"coins": 0, "level": 1}

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("👤 Shaxsiy ma'lumot", "💰 Coinlar", "📞 Admin bilan bog'lanish")

    await message.answer("Salom! Minecraft redactorga hush kelibsiz 👋🏻", reply_markup=keyboard)

# Tugmalar ishlashi
@dp.message_handler(lambda message: message.text == "💰 Coinlar")
async def show_coins(message: types.Message):
    user_id = message.from_user.id
    coins = user_data[user_id]["coins"]
    await message.answer(f"Sizda {coins} ta coin bor.")

@dp.message_handler(lambda message: message.text == "👤 Shaxsiy ma'lumot")
async def show_profile(message: types.Message):
    user_id = message.from_user.id
    coins = user_data[user_id]["coins"]
    level = user_data[user_id]["level"]

    level_names = {
        1: "Boshlovchi",
        2: "O‘yinchi",
        3: "Pro",
        4: "Zam",
        5: "Admin"
    }

    await message.answer(
        f"📌 Sizning darajangiz: {level_names[level]}\n"
        f"💰 Coinlar: {coins}"
    )

@dp.message_handler(lambda message: message.text == "📞 Admin bilan bog'lanish")
async def contact_admin(message: types.Message):
    await message.answer("Admin bilan bog‘lanish uchun: @YourAdminUsername")

# Ogohlantirish va ban tizimi (faqat Zam va Adminlar)
@dp.message_handler(commands=['warn'])
async def warn_user(message: types.Message):
    admin_id = message.from_user.id
    if user_data.get(admin_id, {}).get("level", 1) < 4:
        await message.reply("❌ Sizda huquq yo‘q.")
        return

    if not message.reply_to_message:
        await message.reply("⚠️ Kimga ogohlantirish berishni xabar ustida yozing.")
        return

    target_id = message.reply_to_message.from_user.id
    user_warnings[target_id] = user_warnings.get(target_id, 0) + 1

    if user_warnings[target_id] >= 3:
        await message.answer(f"🚫 {message.reply_to_message.from_user.full_name} guruhdan chiqarildi.")
        await bot.kick_chat_member(message.chat.id, target_id)
    else:
        await message.answer(
            f"⚠️ {message.reply_to_message.from_user.full_name} ogohlantirildi "
            f"({user_warnings[target_id]}/3)"
        )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
