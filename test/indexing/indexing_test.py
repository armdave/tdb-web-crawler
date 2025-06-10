import pytest
from unittest.mock import MagicMock
from indexing.indexing import run

@pytest.fixture
def fake_doc():
    doc = MagicMock()
    doc.id = "doc123"
    doc.to_dict.return_value = {"body": "Apple and banana are fruits."}
    return doc

@pytest.fixture
def empty_doc():
    doc = MagicMock()
    doc.id = "doc_empty"
    doc.to_dict.return_value = {"body": " "}
    return doc

def test_run_updates_keywords_for_valid_docs(fake_doc):
    mock_model = MagicMock()
    mock_model.extract_keywords.return_value = [("apple", 0.9), ("banana", 0.8)]

    mock_repo = MagicMock()
    mock_repo.stream_articles.return_value = [fake_doc]

    run(mock_model, mock_repo)

    mock_model.extract_keywords.assert_called_once_with("Apple and banana are fruits.")
    mock_repo.update_article_keywords.assert_called_once_with(
        fake_doc,
        [("apple", 0.9), ("banana", 0.8)]
    )

def test_run_skips_empty_documents(empty_doc):
    mock_model = MagicMock()
    mock_repo = MagicMock()
    mock_repo.stream_articles.return_value = [empty_doc]

    run(mock_model, mock_repo)

    mock_model.extract_keywords.assert_not_called()
    mock_repo.update_article_keywords.assert_not_called()
