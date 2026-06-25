import requests
from geopy.distance import geodesic
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

# ВСТАВЬ СЮДА СВОИ ДАННЫЕ
BOT_TOKEN = "8879148508:AAH1L7dKa0fUDMDWXiDOTIBURlNhFYbwhUI"
WEATHER_API_KEY = "3844242028f28a15119688add739110c"

# Координаты Алматы
ALMATY = (43.238949, 76.889709)


def get_weather(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    )

    response = requests.get(url).json()

    if response.get("cod") != 200:
        return None

    temp = response["main"]["temp"]
    country = response["sys"]["country"]
    lat = response["coord"]["lat"]
    lon = response["coord"]["lon"]

    distance = int(geodesic(ALMATY, (lat, lon)).km)

    return {
        "city": city,
        "temp": temp,
        "country": country,
        "distance": distance,
    }


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text.strip()

    weather = get_weather(city)

    if weather is None:
        await update.message.reply_text(
            "❌ Город не найден. Проверь правильность написания."
        )
        return

    text = (
        f"🌤 Город: {weather['city']}\n"
        f"🌡 Температура: {weather['temp']}°C\n"
        f"🌍 Страна: {weather['country']}\n"
        f"📏 Расстояние от Алматы: {weather['distance']} км"
    )

    await update.message.reply_text(text)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен!")

    app.run_polling()


if __name__ == "__main__":
    main()