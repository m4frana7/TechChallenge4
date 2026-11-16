"""
Tests for RAG pipeline
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.utils import clean_text, classify_sentiment
from src.data_preparation import DataPreparation


def test_clean_text():
    """Test text cleaning"""
    text = "  Este   é   um   texto    com   espaços  "
    cleaned = clean_text(text)
    assert cleaned == "Este e um texto com espacos"
    assert len(cleaned) > 0


def test_classify_sentiment():
    """Test sentiment classification"""
    assert classify_sentiment(1) == "Negativo"
    assert classify_sentiment(2) == "Negativo"
    assert classify_sentiment(3) == "Neutro"
    assert classify_sentiment(4) == "Positivo"
    assert classify_sentiment(5) == "Positivo"


def test_data_preparation_load():
    """Test data loading"""
    prep = DataPreparation()
    
    try:
        df = prep.load_data()
        assert df is not None
        assert len(df) > 0
        assert 'review_comment_message' in df.columns
    except FileNotFoundError:
        pytest.skip("Reviews CSV not found - run EDA first")


def test_data_preparation_clean():
    """Test data cleaning"""
    prep = DataPreparation()
    
    try:
        prep.load_data()
        df_clean = prep.clean_data()
        
        assert df_clean is not None
        assert len(df_clean) > 0
        assert 'clean_comment' in df_clean.columns
        assert 'sentiment' in df_clean.columns
        
    except FileNotFoundError:
        pytest.skip("Reviews CSV not found - run EDA first")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
