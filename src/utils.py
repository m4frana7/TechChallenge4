"""
Utility functions for the RAG pipeline
"""

import re
import logging
from unicodedata import normalize
from typing import List, Dict, Any
import pandas as pd


def setup_logging(level: str = "INFO"):
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)


logger = setup_logging()


def clean_text(text: str) -> str:
    """
    Clean and normalize text
    
    Args:
        text: Raw text to clean
        
    Returns:
        Cleaned text
    """
    if not isinstance(text, str) or not text.strip():
        return ""
    
    # Remove extra whitespace
    text = " ".join(text.split())
    
    # Normalize unicode characters
    text = normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    
    return text.strip()


def remove_stopwords(text: str, stopwords: set) -> str:
    """
    Remove stopwords from text
    
    Args:
        text: Input text
        stopwords: Set of stopwords to remove
        
    Returns:
        Text without stopwords
    """
    words = text.lower().split()
    filtered_words = [w for w in words if w not in stopwords]
    return " ".join(filtered_words)


def classify_sentiment(score: int) -> str:
    """
    Classify sentiment based on review score
    
    Args:
        score: Review score (1-5)
        
    Returns:
        Sentiment label: Negativo, Neutro, or Positivo
    """
    if score <= 2:
        return "Negativo"
    elif score == 3:
        return "Neutro"
    else:
        return "Positivo"


def prepare_document_text(row: pd.Series) -> str:
    """
    Prepare document text from review data
    Combines review text with relevant metadata
    
    Args:
        row: Pandas Series with review data
        
    Returns:
        Formatted document text
    """
    parts = []
    
    # Add review title if available
    if pd.notna(row.get('review_comment_title')) and row['review_comment_title'].strip():
        parts.append(f"Título: {row['review_comment_title']}")
    
    # Add review comment (main content)
    if pd.notna(row.get('review_comment_message')) and row['review_comment_message'].strip():
        parts.append(f"Comentário: {row['review_comment_message']}")
    
    # Add metadata
    if pd.notna(row.get('review_score')):
        parts.append(f"Nota: {row['review_score']}/5")
    
    if pd.notna(row.get('product_category_name_english')):
        parts.append(f"Categoria: {row['product_category_name_english']}")
    
    if pd.notna(row.get('delivery_status')):
        parts.append(f"Status de Entrega: {row['delivery_status']}")
    
    return " | ".join(parts)


def format_retrieved_documents(documents: List[Dict[str, Any]]) -> str:
    """
    Format retrieved documents for display
    
    Args:
        documents: List of retrieved documents
        
    Returns:
        Formatted string
    """
    formatted = []
    
    for i, doc in enumerate(documents, 1):
        formatted.append(f"\n{'='*60}")
        formatted.append(f"Review {i}")
        formatted.append(f"{'='*60}")
        
        # Extract metadata
        metadata = doc.get('metadata', {})
        
        formatted.append(f"📝 Comentário: {doc.get('content', 'N/A')}")
        formatted.append(f"⭐ Nota: {metadata.get('review_score', 'N/A')}/5")
        
        if metadata.get('product_category_name_english'):
            formatted.append(f"📦 Categoria: {metadata['product_category_name_english']}")
        
        if metadata.get('delivery_status'):
            formatted.append(f"🚚 Entrega: {metadata['delivery_status']}")
        
        if metadata.get('review_id'):
            formatted.append(f"🔑 Review ID: {metadata['review_id']}")
    
    return "\n".join(formatted)


def create_rag_prompt(query: str, context: str) -> str:
    """
    Create prompt for RAG pipeline
    
    Args:
        query: User query
        context: Retrieved context from vector store
        
    Returns:
        Formatted prompt
    """
    prompt = f"""Você é um assistente especializado em análise de avaliações de clientes de e-commerce.
Sua função é responder perguntas baseadas EXCLUSIVAMENTE nas avaliações de clientes fornecidas como contexto.

REGRAS IMPORTANTES:
1. Baseie suas respostas APENAS nas avaliações fornecidas abaixo
2. Cite exemplos específicos das avaliações quando relevante
3. Se não houver informação suficiente no contexto, diga claramente: "Não encontrei evidências suficientes nas avaliações para responder essa pergunta"
4. Não invente ou adicione informações que não estejam nas avaliações
5. Quando identificar padrões, mencione quantas avaliações apoiam essa conclusão

CONTEXTO (Avaliações de Clientes):
{context}

PERGUNTA DO USUÁRIO:
{query}

RESPOSTA:"""
    
    return prompt


def extract_keywords(text: str, top_n: int = 10) -> List[str]:
    """
    Extract keywords from text (simple frequency-based)
    
    Args:
        text: Input text
        top_n: Number of top keywords to return
        
    Returns:
        List of keywords
    """
    # Simple implementation - can be improved with TF-IDF
    words = re.findall(r'\b\w{4,}\b', text.lower())
    from collections import Counter
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(top_n)]


def truncate_text(text: str, max_length: int = 200) -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Input text
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


if __name__ == "__main__":
    # Test utilities
    test_text = "Este é um   texto    com    espaços   extras!"
    print(f"Original: {test_text}")
    print(f"Cleaned: {clean_text(test_text)}")
    
    print(f"\nSentiment 1: {classify_sentiment(1)}")
    print(f"Sentiment 3: {classify_sentiment(3)}")
    print(f"Sentiment 5: {classify_sentiment(5)}")
