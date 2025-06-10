import pytest
from unittest.mock import MagicMock, patch
from indexing.indexing import enqueue_all_indexing_jobs, run_indexing_job
from common.models import IndexingJob

def test_enqueue_all_indexing_jobs():
    mock_repo = MagicMock()
    doc1 = MagicMock()
    doc1.id = "article_1"
    doc2 = MagicMock()
    doc2.id = "article_2"
    mock_repo.stream_articles.return_value = [doc1, doc2]

    with patch("indexing.indexing.enqueue_indexing_job") as mock_enqueue:
        enqueue_all_indexing_jobs(mock_repo)

    mock_enqueue.assert_any_call(IndexingJob(article_id="article_1"))
    mock_enqueue.assert_any_call(IndexingJob(article_id="article_2"))
    assert mock_enqueue.call_count == 2

def test_run_indexing_job_updates_keywords():
    article_id = "abc123"
    article_data = {
        "body": "This is an example about apples and bananas.",
        "url": "https://example.com/article"
    }

    mock_repo = MagicMock()
    mock_repo.retrieve_article.return_value = article_data

    mock_model = MagicMock()
    mock_model.extract_keywords.return_value = [("apple", 0.9), ("banana", 0.8)]

    run_indexing_job(article_id, mock_model, mock_repo)

    mock_model.extract_keywords.assert_called_once_with(article_data["body"])
    mock_repo.update_article_keywords.assert_called_once_with(article_id, [("apple", 0.9), ("banana", 0.8)])

def test_run_indexing_job_skips_empty_body():
    article_id = "abc456"
    article_data = {
        "body": "    ",  # whitespace only
        "url": "https://example.com/empty"
    }

    mock_repo = MagicMock()
    mock_repo.retrieve_article.return_value = article_data

    mock_model = MagicMock()

    run_indexing_job(article_id, mock_model, mock_repo)

    mock_model.extract_keywords.assert_not_called()
    mock_repo.update_article_keywords.assert_not_called()