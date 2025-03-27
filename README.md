# TeraBox Link Processor Bot

A Telegram bot that processes TeraBox links and provides instant streaming access.

## Features

- 🔗 Process TeraBox links instantly
- 🎬 Stream content directly in Telegram
- 👥 Force subscription to channels
- 📢 Broadcast messages to all users
- 🔧 Admin controls and maintenance mode
- 📊 User tracking and statistics

## Deployment

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/yourusername/tereb)
[![Deploy on Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&repository=yourusername/tereb&branch=main&name=terabox-bot)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tereb.git
cd tereb
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
BOT_TOKEN=your_bot_token
API_ID=your_api_id
API_HASH=your_api_hash
MONGODB_URI=your_mongodb_uri
ADMIN_IDS=[your_admin_ids]
DEFAULT_CHANNEL_ID=your_channel_id
LOGS_CHANNEL_ID=your_logs_channel_id
```

4. Run the bot:
```bash
python bot.py
```

## Docker Deployment

1. Build the image:
```bash
docker build -t terabox-bot .
```

2. Run the container:
```bash
docker run -d -p 8000:8000 terabox-bot
```

## Admin Commands

- `/users` - Get total user count
- `/broadcast` - Send message to all users
- `/add` - Add force subscription channel
- `/revert` - Revert to default channel
- `/stop` - Set bot to maintenance mode
- `/activate` - Resume bot service
- `/help` - Show admin help menu

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, join our [Telegram Channel](https://t.me/your_channel) or create an issue in the repository.

## Credits

- [Pyrogram](https://github.com/pyrogram/pyrogram) - Telegram MTProto API client library
- [MongoDB](https://www.mongodb.com/) - Database
- [TeraBox](https://www.terabox.com/) - File hosting service 
