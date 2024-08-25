import os
import asyncio
from dotenv import load_dotenv
from .discord_collector import DiscordCollector
from .dashboard import run_dashboard
from .sentiment_analyzer import analyze_sentiment
from .topic_categorizer import categorize_topic
from .user_segmentation import segment_users
from .email_notifier import check_sentiment_and_notify
from .database import Session, Message
from concurrent.futures import ThreadPoolExecutor
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

sleep_time = 60*60  # Change how long it takes for script to update (in seconds)

async def update_messages():
    while True:
        session = Session()
        try:
            unprocessed_messages = session.query(Message).filter(
                (Message.sentiment_score == None) | (Message.topic_category == None)
            ).all()

            logging.info(f"Processing {len(unprocessed_messages)} messages")

            for message in unprocessed_messages:
                message.sentiment_score = analyze_sentiment(message.content)
                message.topic_category = categorize_topic(message.content)
                logging.info(f"Processed message: sentiment={message.sentiment_score}, topic={message.topic_category}")

            session.commit()
        except Exception as e:
            logging.error(f"Error in update_messages: {e}")
            session.rollback()
        finally:
            session.close()
        await asyncio.sleep(sleep_time)

async def check_sentiment():
    while True:
        session = Session()
        try:
            check_sentiment_and_notify(session, -0.5, os.getenv('MANAGER_EMAIL'))
        except Exception as e:
            logging.error(f"Error in check_sentiment: {e}")
        finally:
            session.close()
        await asyncio.sleep(sleep_time)

async def run_bot(bot, token):
    await bot.start(token)

async def main():
    bot = DiscordCollector()

    try:
        with ThreadPoolExecutor() as executor:
            # Pass the PORT and HOST information to the dashboard
            dashboard_future = executor.submit(run_dashboard, host="0.0.0.0", port=int(os.getenv('PORT', 5000)))

            await asyncio.gather(
                run_bot(bot, os.getenv('DISCORD_TOKEN')),
                update_messages(),
                check_sentiment()
            )
    except Exception as e:
        logging.error(f"An error occurred in main: {e}")
    finally:
        await bot.close()
        if 'dashboard_future' in locals():
            dashboard_future.cancel()

if __name__ == "__main__":
    asyncio.run(main())
