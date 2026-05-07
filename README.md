# Telegram Channel Gatekeeper Bot 🚀

A high-performance Telegram bot built to automate subscriber management for private Telegram channels. It automatically approves join requests, greets new users with a welcome message (lead magnet) in their DMs, and provides a powerful admin panel for statistics and broadcasting.

<img width="593" height="697" alt="image" src="https://github.com/user-attachments/assets/3b4f8466-75ab-4467-b649-d718240d44ad" />


## ✨ Features

- **Auto-Approve System:** Instantly intercepts and approves `chat_join_request` events.
- **Lead Magnet Delivery:** Sends a customized greeting and bonus link to users directly in private messages upon joining.
- **Robust Database:** Securely stores user data (Telegram ID, Username, First Name, Join Date) using PostgreSQL and SQLAlchemy 2.0.
- **Admin Dashboard:** Exclusive access for administrators to view real-time statistics (total users, new users today).
- **Smart Broadcasting:** Built-in `/mail` command to send mass messages to all subscribers, featuring automatic FloodWait protection to prevent bot bans.


## 🛠 Tech Stack

- **Language:** Python 3.12+
- **Framework:** `aiogram` 3.x
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy (Async)
- **Deployment:** Docker & Docker Compose

## ⚙️ Prerequisites

Before you begin, ensure you have met the following requirements:
* You have installed **Docker** and **Docker Compose**.
* You have created a bot via [@BotFather](https://t.me/botfather) and obtained its `TOKEN`.
* Your bot is added to your private channel as an **Administrator** with the **"Add Subscribers"** permission.
* You have generated an **Invite Link** for your channel with the **"Request Admin Approval"** setting enabled.

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ImpLeax/GateKeeperBot
   cd GateKeeperBot
   ```

2. **Configure Environment Variables:**
   Create a `.env` file in the root directory and configure it as follows:
   ```ini
   # Bot Configuration
   TOKEN=your_bot_token_here
   ADMIN=your_telegram_id_here

   # PostgreSQL Configuration
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=gatekeeper_db
   POSTGRES_HOST=db
   ```

3. **Run with Docker Compose:**
   Build and start the bot and database containers in detached mode:
   ```bash
   docker compose up -d --build
   ```


## 📱 Admin Commands

These commands are restricted and will only respond to the `ADMIN` ID specified in the `.env` file.

* `/start` - Displays the Bot Control Panel with basic status information.
* `/stats` - Shows detailed statistics (Total subscribers in the DB and new joins today).
* `/mail <your message>` - Initiates a mass broadcast to all saved users. Includes built-in sleep delays to comply with Telegram API rate limits.

<img width="594" height="213" alt="image" src="https://github.com/user-attachments/assets/58d1fb3e-b3a9-48ba-8a1f-983d1149bac9" />
<img width="589" height="232" alt="image" src="https://github.com/user-attachments/assets/ddd0e119-28b0-4d81-9965-f2bce06ccf0b" />


