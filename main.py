"""Function called by PubSub trigger to execute cron job tasks."""
import os
import json
import random
import requests
import datetime
from google.cloud import pubsub_v1, logging

from dotenv import load_dotenv

load_dotenv()

from config import config_vars
from constants import COINS, URL_API_NOMICS

topic_id = config_vars['topic_id']
project_id = config_vars['project_id']

publisher = pubsub_v1.PublisherClient()
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)

client = logging.Client()
logger = client.logger("monitoring_crypto_prices")

def generate_tokens() -> str:

    iter_number = random.randint(2, 12)

    coins_formated = ",".join( [ COINS[random.randint(0, 19)] for _ in range(0, iter_number) ] )

    return coins_formated

def execute_request_to_api(ids_currencies):
    """Executes request for get data and publish to a new destination topic pub/sub.
    Args:
        ids_currencies: Object representing a reference to a List of currencies ids
    """
    url_nomics = f"{URL_API_NOMICS}?key={os.environ['API_KEY_NOMICS']}&ids={ids_currencies}&interval=1d,30d&convert=USD&per-page=100&page=1"

    data = requests.get(url_nomics)

    #print(data.json())
    for currency in data.json():

        logger_name = f"monitoring_crypto_price_{str(currency['currency'])}"

        logger_currency = client.logger(logger_name)

        
        #metric = client.metric(f"metrica_dist_monitoring_crypto_price_{str(currency['currency'])}", filter_=filter_, description="")
        #if not metric.exists():
        #    metric.create()

        message = {
            'id': str(currency['id']),
            'currency':str(currency['currency']),
            'name':str(currency['name']),
            'price':str(currency['price']),
            'price_timestamp':str(currency['price_timestamp'])
        }

        if 10 == int(random.randint(0, 19)):
            raise Exception("error random API")

        #logger.log_text(f"Error: {num}", severity="ERROR")
        #logger.log_struct({"stock": (50.0 - float(currency['price'])) * 100.0}, labels={"type": "product"})

        logger_currency.log_struct({"stock" : float(currency['price']) }, labels={"type": "product"})

        print(message)

        # Data must be a bytestring
        message = json.dumps(message).encode('utf-8')
        # When you publish a message, the client returns a future.
        future = publisher.publish(topic_path, message)
        print(future.result())

    logger.log_text('Request complete. The data has been published.', severity="INFO")

def main(data, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
        data (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    print("inicio")
    try:
        current_time = datetime.datetime.utcnow()

        logger.log_text(f'Cloud Function was triggered on {current_time}', severity="INFO")

        currencies_final = generate_tokens()

        try:
            execute_request_to_api(currencies_final)

        except Exception as error:
            print(error)
            logger.log_text(f'Request failed due to {error}.', severity="ERROR")

        print("ok")

    except Exception as error:
        print(error)
        logger.log_text(f'{error}.', severity="ERROR")


main('data', 'context')

