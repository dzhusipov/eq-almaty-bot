from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
from datetime import datetime, timedelta
import sqlite3 
import asyncio
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Use environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hi! Use /latest to get the latest earthquake info.')


async def latest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&eventtype=earthquake&latitude=43.222015&longitude=76.851250&maxradiuskm=1000&orderby=time&minmagnitude=4.0"
    response = requests.get(url).json()
    
    if response["features"]:
        latest_eq = response["features"][0]
        mag = latest_eq["properties"]["mag"]
        place = latest_eq["properties"]["place"]
        
        time_epoch = latest_eq["properties"]["time"]
        timestamp_s = time_epoch / 1000
        date_time = datetime.utcfromtimestamp(timestamp_s)
        date_time_plus_5_hours = date_time + timedelta(hours=5)
        time = date_time_plus_5_hours.strftime("%d-%m-%Y %H:%M:%S")
        
        message = f"Latest Earthquake:\nMagnitude: {mag}\nLocation: {place}\nTime: {time}"
        await update.message.reply_text(message)

         # Save to database
        conn = sqlite3.connect('earthquake_data.db')
        c = conn.cursor()
        c.execute("INSERT INTO earthquakes (magnitude, place, time) VALUES (?, ?, ?)",
                  (mag, place, time))
        conn.commit()
        conn.close()

    else:
        update.message.reply_text("No recent earthquakes found.")


async def check_earthquake_updates(context: ContextTypes.DEFAULT_TYPE):
    chat_id = '151137540'  # Replace with your actual chat ID
    while True:
        url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&eventtype=earthquake&latitude=43.222015&longitude=76.851250&maxradiuskm=1000&orderby=time&minmagnitude=4.0"
        response = requests.get(url).json()

        if response["features"]:
            latest_eq = response["features"][0]
            mag = latest_eq["properties"]["mag"]
            place = latest_eq["properties"]["place"]
            time_epoch = latest_eq["properties"]["time"]
            
            # Check against the last entry in the database
            conn = sqlite3.connect('earthquake_data.db')
            c = conn.cursor()
            c.execute("SELECT * FROM earthquakes ORDER BY id DESC LIMIT 1")
            last_record = c.fetchone()
            conn.close()

            # If there's no record or the time is different, it's a new earthquake
            if not last_record or last_record[3] != str(time_epoch):
                # Update the database with the new earthquake
                conn = sqlite3.connect('earthquake_data.db')
                c = conn.cursor()
                c.execute("INSERT INTO earthquakes (magnitude, place, time) VALUES (?, ?, ?)",
                          (mag, place, str(time_epoch)))
                conn.commit()
                conn.close()

                # Convert time to human-readable format
                timestamp_s = time_epoch / 1000
                date_time = datetime.utcfromtimestamp(timestamp_s) + timedelta(hours=5)
                human_time = date_time.strftime("%d-%m-%Y %H:%M:%S")

                message = f"New Earthquake Detected:\nMagnitude: {mag}\nLocation: {place}\nTime: {human_time}"
                # Use context.bot.send_message to send a message from a background task
                await context.bot.send_message(chat_id=chat_id, text=message)
                
        await asyncio.sleep(10)  # Wait for 10 seconds before checking again


def setup_database():
    conn = sqlite3.connect('earthquake_data.db')
    c = conn.cursor()
    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS earthquakes
                 (id INTEGER PRIMARY KEY, magnitude REAL, place TEXT, time TEXT)''')
    conn.commit()
    conn.close()


def main() -> None:
    setup_database()  # Ensure the database and table are ready.
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("latest", latest))

    application.run_polling()
    asyncio.create_task(check_earthquake_updates(application.get_default_context()))


if __name__ == "__main__":
    main()
