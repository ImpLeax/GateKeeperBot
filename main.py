import os, logging, sys, asyncio
from logging.handlers import TimedRotatingFileHandler

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ChatJoinRequest
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter

from db.database import BotDatabase

load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN = int(os.getenv("ADMIN"))
dp = Dispatcher()
bot = Bot(TOKEN)
db = BotDatabase()

@dp.message(CommandStart())
async def start(message: Message):
    if message.from_user.id != ADMIN:
        return

    await bot.send_message(
        message.chat.id,
        (
            f"⚙️ Bot Control Panel\nHello, {message.from_user.first_name if message.from_user.first_name else "Admin"}!"
            "\nThe bot is operating normally and is ready to accept requests."
            "\n\nAvailable commands:"
            "\n/stats - view the bot's statistics"
            "\n/mail <message> - send a message to all users "
        )
    )

@dp.chat_join_request()
async def approve_request(update: ChatJoinRequest, bot: Bot):
    user_id = update.from_user.id
    username = update.from_user.username
    first_name = update.from_user.first_name
    channel_id = update.chat.id

    try:
        await update.approve()
        logging.info(f"Request approved to user: {username} with id: {user_id}.")

        await db.add_user(user_id, channel_id, username, first_name)

        await bot.send_message(
            chat_id=user_id,
            text=(
                f"Hi, {update.from_user.first_name}! 👋\n\n"
                f"Your application to the channel has been approved. Here's the bonus we promised: 🎁"
            )
        )

    except TelegramForbiddenError:
        logging.warning(f"We were unable to send a greeting to {user_id}. The bot has been blocked by the user.")

    except Exception as e:
        logging.error(f"An error occurred while processing user {user_id}: {e}")

@dp.message(Command("mail"))
async def mail(message: Message):
    if message.from_user.id != ADMIN:
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("❌ Enter the text for the email after the command.\nExample: `/mail Hello everyone!`")
        return

    mail_text = parts[1]

    user_ids = await db.get_users()

    success_count = 0
    fail_count = 0

    await message.answer(f"🚀 Starting a newsletter for {len(user_ids)} users...")

    for user in user_ids:
        if user < 0:
            continue
        try:
            await bot.send_message(
                chat_id=user,
                text=mail_text
            )
            success_count += 1

            await  asyncio.sleep(0.05)

        except TelegramRetryAfter as e:
            logging.warning(f"You've exceeded the limits. Please wait {e.retry_after} seconds...")
            await asyncio.sleep(e.retry_after)

        except TelegramForbiddenError:
            fail_count += 1
            await db.delete_user(user)
        except Exception as e:
            logging.error(f"An error occurred while sending a message to user {user}: {e}")

    await message.answer(
        f"✅ The mailing is complete!\n"
        f"Successfully delivered: {success_count}\n"
        f"Bot blocked / Errors: {fail_count}"
    )

@dp.message(Command("stats"))
async def stats(message: Message):
    if message.from_user.id != ADMIN:
        return

    res = await db.get_stats()

    try:
        await message.reply(
            (
                "📊 *Statistics:*\n\n"
                f"👥 Total subscribers in the database: *{res.get("user_count", 0)}*\n"
                f"📈 New subscribers today: *{res.get("users_today", 0)}*"
            ),
            parse_mode="MarkdownV2"
        )
    except Exception as e:
        logging.error(f"An error occurred while sending a message to user {message.from_user.id}: {e}")

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    os.makedirs("logs", exist_ok=True)
    file_handler = TimedRotatingFileHandler(
        "logs/gatekeeper.log",
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

async def main():
    await db.init_models()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        setup_logger()
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Error: {e}")
