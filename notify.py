import requests
from datetime import datetime
import os
import polars as pl
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

district = os.getenv("DISTRICT")
locality = os.getenv("LOCALITY")
bot_token = os.getenv("BOT_TOKEN")
bot_chatID = os.getenv("CHAT_ID")


data_path = "./fetched_files/power-outages.json"


def get_outage_data(district, locality, file_path):

    data = pl.scan_ndjson(data_path)
    district_data = (
        data.select(
            district
        )
        .collect()
        .item()
        .to_list()
    )
    df = pl.from_dicts(district_data).lazy()
    df = (
        df.filter(
            pl.col("locality")
            .str.to_lowercase()
            .str.contains(locality.lower())
        )
    )
    df = (
        df.with_columns(
            pl.col("from").cast(pl.Datetime),
            pl.col("to").cast(pl.Datetime),
        )
        .sort("from", descending=True)
        .head(1)
    )
    return df


def outage_message(latest_date: str):
    date = latest_date["date"]
    locality = latest_date["locality"]
    streets = latest_date["streets"]
    from_time = latest_date["from"]
    to_time = latest_date["to"]

    if from_time <= to_time:
        duration = int((to_time - from_time).seconds / 60 / 60)
    else:
        duration = int((from_time - to_time).seconds / 60 / 60)

    message = f"""
    *Power Outage Alert*:
    {date}

    Locality: {locality}
    Streets: {streets}
    Outage Duration: {duration} hours
    """

    return message


def send_telegram_message(bot_message: str, bot_token: str, bot_chatID: str):

    send_text: str = (
        f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={bot_message}"
    )
    logging.info("Bot: Message Sent to Telegram")

    response = requests.get(send_text)

    return response


def notify(latest_date):

    from_time = latest_date["from"]
    to_time = latest_date["to"]

    if (from_time >= datetime.now()) or (to_time >= datetime.now()):
        return True
    else:
        logging.info("Outage data is outdated")
        return False


def main():
    latest_date = get_outage_data(district, locality, data_path)
    latest_date = latest_date.collect().to_dicts()[0]

    if latest_date is None:
        logging.info("No Outage Data Found")
        return

    notify_result = notify(latest_date)

    if notify_result:
        logging.info("Notifying Outage")
        message = outage_message(latest_date)

        response = send_telegram_message(message, bot_token, bot_chatID)

        logging.info(response.json())


if __name__ == "__main__":
    main()
