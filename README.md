<h1 align="center">🎵 Swati Music Bot 🎵</h1>

<p align="center">
  <b>A fast, powerful, and lightweight Telegram Music Bot built with Python, Pyrogram, PyTgCalls, and shnwazdev-ytmusicapi.</b>
</p>

<p align="center">
  <a href="https://github.com/shnwazdeveloper/swati-music"><img src="https://img.shields.io/github/stars/shnwazdeveloper/swati-music?style=for-the-badge&color=blue" alt="GitHub stars"></a>
  <a href="https://github.com/shnwazdeveloper/swati-music"><img src="https://img.shields.io/github/forks/shnwazdeveloper/swati-music?style=for-the-badge&color=blue" alt="GitHub forks"></a>
  <a href="https://github.com/shnwazdeveloper/swati-music/blob/main/LICENSE"><img src="https://img.shields.io/github/license/shnwazdeveloper/swati-music?style=for-the-badge&color=green" alt="License"></a>
</p>

---

## ✨ Features

- 🚀 **Ultra Fast Response**: Powered by `shnwazdev-ytmusicapi` for instant track retrieval and streaming.
- 💎 **Premium Custom Emojis**: Beautiful custom Telegram emojis integrated into responses and welcome messages.
- 🎶 **Audio & Video Streaming**: Play music or high-definition music videos (`/play`, `/vplay`) directly in voice chats.
- ⚡ **Optimized Assistant VC Join**: Instant assistant account channel/group join with reduced latency.
- 🌐 **Built-in Web Health Check**: Exposes `/health` and `/apikey` endpoints on port `$PORT` (default 8080) for 24/7 web hosting support.

## 📖 About

**Swati Music** is a high-performance Telegram Voice Chat bot that allows users to play music and video streams directly in their Telegram groups. Designed with a custom integration of `shnwazdev-ytmusicapi`, it provides instant search and playback speeds without the common lag found in traditional bots. Built completely on modern Python asynchronously, it supports custom premium emojis, playlist queuing, and 24/7 web hosting.

---

## 🚀 One-Click Deploy to Render

You can easily host this bot for free 24/7 on Render. Click the button below, fill in your environment variables, and deploy!

<p align="center">
  <a href="https://render.com/deploy?repo=https://github.com/shnwazdeveloper/swati-music">
    <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
  </a>
</p>

---

## 🛠️ Required Environment Variables

| Variable | Description |
|---|---|
| `API_ID` | Telegram API ID from [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | Telegram API Hash from [my.telegram.org](https://my.telegram.org) |
| `BOT_TOKEN` | Bot Token from [@BotFather](https://t.me/BotFather) |
| `MONGO_URL` | MongoDB connection URL |
| `OWNER_ID` | Telegram User ID of the Bot Owner |
| `SESSION` | Pyrogram String Session for the Assistant Account |
| `LOGGER_ID` | Log Group Telegram Chat ID |

---

## 🚀 Manual VPS Deployment

### 1. Prerequisites
- Python 3.10+
- FFmpeg installed

### 2. Installation Steps
```bash
# Update System
sudo apt-get update && sudo apt-get upgrade -y

# Install Python & FFmpeg
sudo apt-get install python3-pip ffmpeg -y

# Clone Repository
git clone https://github.com/shnwazdeveloper/swati-music
cd swati-music

# Install Python Dependencies
pip3 install -U -r requirements.txt

# Run Bot
bash start
```

---

## 📌 Commands

| Command | Description |
|---|---|
| `/play <song/URL>` | Play music in the voice chat |
| `/vplay <song/URL>` | Play video in the voice chat |
| `/pause` | Pause ongoing stream |
| `/resume` | Resume paused stream |
| `/skip` | Skip current stream |
| `/stop` | Stop playback & clear queue |
| `/queue` | View active queue |
| `/sudolist` | View bot sudo users |
| `/help` | Show interactive help menu |

---

## 📄 License & Credits

Distributed under the MIT License. See `LICENSE` for details.

- Developed & Maintained by [shnwazdeveloper](https://github.com/shnwazdeveloper)
- Base Architecture: Swati Music
