from indexing.keyword_model import KeywordModel
from common.job_dispatcher import enqueue_indexing_job
from common.models import IndexingJob
from common.repository import Repository

def enqueue_all_indexing_jobs(repository: Repository):
    for doc in repository.stream_articles():
        enqueue_indexing_job(IndexingJob(article_id=doc.id))

def run_indexing_job(article_id: str, keyword_model: KeywordModel, repository: Repository):
    data = repository.retrieve_article(article_id)
    body = data.get("body", "")
    if not body.strip():
        print(f"Skipping {data.get('url', '')}: empty body")
        return

    keywords = keyword_model.extract_keywords(body)
    print(f"Updating {data.get('url', '')} with keywords: {keywords}")
    repository.update_article_keywords(article_id, keywords)
