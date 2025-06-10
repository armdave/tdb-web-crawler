import base64
import asyncio
from crawler.crawler import run_crawl_job_from_payload
from common.firestore_repository import FirestoreRepository
from crawler.extractor import extract_and_save_content
from indexing.indexing import enqueue_all_indexing_jobs, run_indexing_job
from indexing.keybert_keyword_model import KeyBERTKeywordModel
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
    

def run_all_indexing_job(event, context):
    print('all indexing job entered')
    enqueue_all_indexing_jobs(FirestoreRepository())


def run_indexing_job(event, context):
    print('indexing job entered')
    message_json = load_message(event)
    article_id = message_json.get('article_id')

    if article_id:
        run_indexing_job(article_id, KeyBERTKeywordModel(), FirestoreRepository())
    else:
        raise Exception("No article_id provided in the message.")


def load_message(event):
    try:
        message_data = base64.b64decode(event['data']).decode('utf-8') if 'data' in event else '{}'
        return json.loads(message_data)

    except Exception as e:
        print(f"Error processing extract job: {e}")
