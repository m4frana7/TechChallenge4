"""
Vector store module using FAISS
Handles storage and retrieval of document embeddings
"""

import logging
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import faiss
from .config import VECTOR_STORE_PATH, PROJECT_ROOT, EMBEDDING_MODEL
from .bundled_store import load_bundled_store

logger = logging.getLogger(__name__)


class VectorStore:
    """FAISS-based vector store for document retrieval"""
    
    def __init__(self, dimension: int, store_path: Optional[Path] = None):
        """
        Initialize vector store
        
        Args:
            dimension: Dimension of embeddings
            store_path: Path to save/load the index
        """
        self.dimension = dimension
        self.store_path = store_path or VECTOR_STORE_PATH
        self.index = None
        self.documents = []
        self.embeddings = None
        
    def create_index(self, use_gpu: bool = False):
        """
        Create a new FAISS index
        
        Args:
            use_gpu: Whether to use GPU acceleration (if available)
        """
        logger.info(f"Creating FAISS index with dimension {self.dimension}")
        
        # Create a flat (exact search) index
        # For production, consider using IVF or HNSW for better performance
        self.index = faiss.IndexFlatL2(self.dimension)
        
        if use_gpu and faiss.get_num_gpus() > 0:
            logger.info("Using GPU acceleration")
            res = faiss.StandardGpuResources()
            self.index = faiss.index_cpu_to_gpu(res, 0, self.index)
        
        logger.info("FAISS index created")
    
    def add_documents(
        self, 
        documents: List[Dict[str, Any]], 
        embeddings: np.ndarray
    ):
        """
        Add documents and their embeddings to the store
        
        Args:
            documents: List of documents with metadata
            embeddings: Array of embeddings
        """
        if self.index is None:
            self.create_index()
        
        logger.info(f"Adding {len(documents)} documents to vector store")
        
        # Ensure embeddings are float32
        embeddings = embeddings.astype('float32')
        
        # Add to index
        self.index.add(embeddings)
        
        # Store documents and embeddings
        self.documents.extend(documents)
        if self.embeddings is None:
            self.embeddings = embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, embeddings])
        
        logger.info(f"Total documents in store: {len(self.documents)}")
    
    def search(
        self, 
        query_embedding: np.ndarray, 
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        Search for similar documents
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            filters: Optional metadata filters
            
        Returns:
            List of (document, score) tuples
        """
        if self.index is None or len(self.documents) == 0:
            logger.warning("Vector store is empty")
            return []
        
        # Ensure query is float32 and 2D
        query_embedding = query_embedding.astype('float32').reshape(1, -1)
        
        # Search
        distances, indices = self.index.search(query_embedding, top_k)
        
        # Prepare results
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.documents):
                doc = self.documents[idx]
                
                # Apply filters if provided
                if filters:
                    match = all(
                        doc['metadata'].get(key) == value 
                        for key, value in filters.items()
                    )
                    if not match:
                        continue
                
                results.append((doc, float(dist)))
        
        logger.info(f"Found {len(results)} results for query")
        return results
    
    def save(self):
        """Save the vector store to disk"""
        logger.info(f"Saving vector store to {self.store_path}")
        
        # Create directory if it doesn't exist
        self.store_path.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        index_path = self.store_path / "index.faiss"
        faiss.write_index(self.index, str(index_path))
        
        # Save documents and embeddings
        data_path = self.store_path / "documents.pkl"
        with open(data_path, 'wb') as f:
            pickle.dump({
                'documents': self.documents,
                'embeddings': self.embeddings,
                'dimension': self.dimension
            }, f)
        
        logger.info("Vector store saved successfully")
    
    def load(self):
        """Load the vector store from disk"""
        logger.info(f"Loading vector store from {self.store_path}")

        # The deployed app uses a precomputed index instead of encoding all reviews.
        bundle_path = PROJECT_ROOT / "assets" / "search_index"
        if self.store_path == VECTOR_STORE_PATH and (bundle_path / "manifest.json").exists():
            self.index, self.documents = load_bundled_store(
                bundle_path, EMBEDDING_MODEL, self.dimension
            )
            # FAISS already holds the vectors; retaining another copy wastes memory.
            self.embeddings = None
            logger.info("Loaded precomputed index: %s documents", len(self.documents))
            return
        
        # Load FAISS index
        index_path = self.store_path / "index.faiss"
        if not index_path.exists():
            raise FileNotFoundError(f"Index not found at {index_path}")
        
        self.index = faiss.read_index(str(index_path))
        
        # Load documents and embeddings
        data_path = self.store_path / "documents.pkl"
        with open(data_path, 'rb') as f:
            data = pickle.load(f)
            self.documents = data['documents']
            self.embeddings = data['embeddings']
            self.dimension = data['dimension']
        
        logger.info(f"Loaded {len(self.documents)} documents")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the vector store"""
        return {
            'total_documents': len(self.documents),
            'embedding_dimension': self.dimension,
            'index_type': type(self.index).__name__,
            'total_vectors': self.index.ntotal if self.index else 0
        }


def main():
    """Test vector store"""
    logging.basicConfig(level=logging.INFO)
    
    print("🗄️ Vector Store Test\n")
    print("="*60)
    
    # Create test data
    dimension = 384
    num_docs = 100
    
    print(f"Creating test data: {num_docs} documents with {dimension} dimensions")
    
    # Random embeddings for testing
    embeddings = np.random.rand(num_docs, dimension).astype('float32')
    
    # Test documents
    documents = [
        {
            'id': f'doc_{i}',
            'text': f'Test document {i}',
            'metadata': {
                'review_score': (i % 5) + 1,
                'category': f'category_{i % 10}'
            }
        }
        for i in range(num_docs)
    ]
    
    # Initialize vector store
    store = VectorStore(dimension=dimension)
    
    # Add documents
    store.add_documents(documents, embeddings)
    
    # Test search
    query_embedding = np.random.rand(dimension).astype('float32')
    results = store.search(query_embedding, top_k=5)
    
    print(f"\n🔍 Search results (top 5):")
    for i, (doc, score) in enumerate(results, 1):
        print(f"  {i}. {doc['id']} (score: {score:.4f})")
    
    # Test with filters
    filtered_results = store.search(
        query_embedding, 
        top_k=5,
        filters={'review_score': 5}
    )
    
    print(f"\n🎯 Filtered search (score=5):")
    for i, (doc, score) in enumerate(filtered_results, 1):
        print(f"  {i}. {doc['id']} (score: {score:.4f})")
    
    # Statistics
    stats = store.get_statistics()
    print(f"\n📊 Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test save/load
    print(f"\n💾 Testing save/load...")
    store.save()
    
    new_store = VectorStore(dimension=dimension)
    new_store.load()
    
    print(f"  Loaded {len(new_store.documents)} documents")
    
    print("\n✅ Vector store test completed!")


if __name__ == "__main__":
    main()
