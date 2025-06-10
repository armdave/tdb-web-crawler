import pytest
from unittest.mock import MagicMock, patch
from indexing.keybert_keyword_model import KeyBERTKeywordModel

@pytest.fixture
def long_text():
    return "word " * 600  # long enough to produce multiple chunks

@patch("indexing.keybert_keyword_model.KeyBERT")
@patch("indexing.keybert_keyword_model.SentenceTransformer")
def test_keyword_extraction_deduplication_and_truncation(mock_st, mock_kb, long_text):
    mock_model = MagicMock()
    mock_model.extract_keywords.side_effect = [
    [("apple", 0.9), ("banana", 0.8)],
    [("carrot", 0.7), ("banana", 0.85)],
    [("durian", 0.6)],
    [("eggplant", 0.5)],
    ]
    mock_kb.return_value = mock_model

    model = KeyBERTKeywordModel()
    keywords = model.extract_keywords(long_text, top_n=4)

    assert len(keywords) == 4
    assert keywords[0] == "apple"
    assert keywords[1] == "banana"
    assert "carrot" in keywords
    assert any(kw in keywords for kw in ["durian", "eggplant"])

def test_chunking_behavior():
    model = KeyBERTKeywordModel()
    chunks = model._chunk_text("a" * 2500, chunk_size=1000, overlap=100)
    assert len(chunks) == 3
    assert len(chunks[0]) == 1000
    assert len(chunks[1]) == 1000
    assert len(chunks[2]) == 700

def test_empty_text_returns_empty_list():
    model = KeyBERTKeywordModel()
    keywords = model.extract_keywords("", top_n=5)
    assert keywords == []
