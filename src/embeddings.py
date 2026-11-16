"""
Embeddings generation module
Handles creation of vector embeddings for documents
"""

import logging
from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from .config import EMBEDDING_MODEL, MODELS_PATH

logger = logging.getLogger(__name__)


class EmbeddingsGenerator:
    """Class to generate embeddings for documents"""
    
    def __init__(self, model_name: str = None):
        """
        Initialize embeddings generator
        
        Args:
            model_name: Name of the sentence transformer model
        """
        self.model_name = model_name or EMBEDDING_MODEL
        self.model = None
        self.embedding_dimension = None
        
    def load_model(self):
        """Load the sentence transformer model"""
        logger.info(f"Loading embedding model: {self.model_name}")
        
        try:
            self.model = SentenceTransformer(
                self.model_name,
                cache_folder=str(MODELS_PATH)
            )
            self.embedding_dimension = self.model.get_sentence_embedding_dimension()
            
            logger.info(
                f"Model loaded successfully. "
                f"Embedding dimension: {self.embedding_dimension}"
            )
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def generate_embeddings(
        self, 
        documents: List[Dict[str, Any]],
        batch_size: int = 32,
        show_progress: bool = True
    ) -> np.ndarray:
        """
        Generate embeddings for a list of documents
        
        Args:
            documents: List of documents with 'text' field
            batch_size: Batch size for encoding
            show_progress: Whether to show progress bar
            
        Returns:
            Array of embeddings
        """
        if self.model is None:
            self.load_model()
        
        logger.info(f"Generating embeddings for {len(documents)} documents")
        
        # Extract texts
        texts = [doc['text'] for doc in documents]
        
        # Generate embeddings
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )
        
        logger.info(f"Generated embeddings with shape: {embeddings.shape}")
        
        return embeddings
    
    def generate_query_embedding(self, query: str) -> np.ndarray:
        """
        Generate embedding for a single query
        
        Args:
            query: Query text
            
        Returns:
            Query embedding
        """
        if self.model is None:
            self.load_model()
        
        embedding = self.model.encode(
            query,
            convert_to_numpy=True
        )
        
        return embedding


def main():
    """Test embeddings generation"""
    logging.basicConfig(level=logging.INFO)
    
    print("🧠 Embeddings Generation Test\n")
    print("="*60)
    
    # Initialize generator
    generator = EmbeddingsGenerator()
    
    # Test documents
    test_docs = [
        {'text': 'Produto excelente, entrega rápida!'},
        {'text': 'Muito insatisfeito com a qualidade.'},
        {'text': 'Atendimento nota 10, recomendo!'}
    ]
    
    print(f"\n📝 Test documents: {len(test_docs)}")
    
    # Generate embeddings
    embeddings = generator.generate_embeddings(test_docs)
    
    print(f"\n📊 Results:")
    print(f"  Shape: {embeddings.shape}")
    print(f"  Dimension: {embeddings.shape[1]}")
    print(f"  Sample embedding (first 5 dims): {embeddings[0][:5]}")
    
    # Test query
    query = "Problemas com entrega"
    query_emb = generator.generate_query_embedding(query)
    
    print(f"\n🔍 Query embedding:")
    print(f"  Query: '{query}'")
    print(f"  Shape: {query_emb.shape}")
    
    print("\n✅ Embeddings generation test completed!")


if __name__ == "__main__":
    main()
