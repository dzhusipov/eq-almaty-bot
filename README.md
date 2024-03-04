# Telegram Earthquake Bot

This Telegram bot provides the latest earthquake information based on USGS Earthquake data API. Users can get real-time updates on earthquakes within a specified radius around Almaty, Kazakhstan.

## Features

- **Start**: Welcomes the user and provides instructions on how to use the bot.
- **Latest Earthquake**: Fetches and displays the most recent earthquake information including magnitude, location, and time.

## Prerequisites

Before you can run this bot, you'll need:

- Python 3.9 or later
- A Telegram bot token from [BotFather](https://t.me/botfather)

## Installation

1. Clone this repository to your local machine.
   ```bash
   git clone https://your-repository-url.git
   cd your-repository-directory

2. Install the required dependencies.

    ```bash
    pip install -r requirements.txt

3. Create a .env file in the root directory of your project and add your Telegram bot token.

    ```plaintext
    Copy code
    BOT_TOKEN=your_bot_token_here

4. Run the bot.

    ```bash
    python main.py

## Using Docker  
This project can also be run using Docker. Here's how:

1. Build the Docker image.

    ```bash
    docker build -t telegram-bot-app .

2. Run the Docker container, replacing your_bot_token_here with your actual Telegram bot token.

    ```bash
    docker run -d -p 4000:80 -e BOT_TOKEN='your_bot_token_here' telegram-bot-app

## Contributing
Contributions are welcome! Please feel free to submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
