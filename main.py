import base64
import asyncio
from crawler.crawler import run_crawl_job_from_payload
from common.firestore_repository import FirestoreRepository
from crawler.extractor import extract_and_save_content
import json

def run_crawl_job(event, context):
    print('crawl job entered')
    message_json = load_message(event)
    asyncio.run(run_crawl_job_from_payload(json.dumps(message_json)))


def run_extract_job(event, context):
    print('extract job entered')
    message_json = load_message(event)
    url = message_json.get('url')

    if url:
        extract_and_save_content(url, FirestoreRepository())
    else:
        raise Exception("No URL provided in the message.")


def load_message(event):
    try:
        message_data = base64.b64decode(event['data']).decode('utf-8') if 'data' in event else '{}'
        return json.loads(message_data)

    except Exception as e:
        print(f"Error processing extract job: {e}")
