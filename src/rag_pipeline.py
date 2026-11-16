"""
RAG Pipeline implementation
Complete Retrieval-Augmented Generation pipeline
"""

import logging
from typing import List, Dict, Any, Optional
import numpy as np
from .data_preparation import DataPreparation
from .embeddings import EmbeddingsGenerator
from .vector_store import VectorStore
from .config import (
    TOP_K_RESULTS, 
    TEMPERATURE, 
    GROQ_API_KEY, 
    GROQ_MODEL,
    OPENAI_API_KEY, 
    GOOGLE_API_KEY
)
from .utils import create_rag_prompt, format_retrieved_documents

logger = logging.getLogger(__name__)


class RAGPipeline:
    """Complete RAG pipeline for Voice of Customer Intelligence"""
    
    def __init__(
        self,
        embedding_model: Optional[str] = None,
        llm_provider: str = "groq",
        top_k: int = TOP_K_RESULTS
    ):
        """
        Initialize RAG pipeline
        
        Args:
            embedding_model: Name of embedding model (default from config)
            llm_provider: LLM provider ('groq', 'openai', or 'google')
            top_k: Number of documents to retrieve
        """
        self.data_prep = DataPreparation()
        self.embeddings_gen = EmbeddingsGenerator(model_name=embedding_model)
        self.vector_store = None
        self.llm_provider = llm_provider
        self.top_k = top_k
        self.llm_client = None
        
    def setup(self):
        """Setup the pipeline by loading models and initializing components"""
        logger.info("Setting up RAG pipeline...")
        
        # Load embedding model
        self.embeddings_gen.load_model()
        
        # Initialize LLM
        self._initialize_llm()
        
        logger.info("RAG pipeline setup completed")
    
    def _initialize_llm(self):
        """Initialize LLM client based on provider"""
        logger.info(f"Initializing LLM: {self.llm_provider}")
        
        if self.llm_provider == "groq":
            if not GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY not found in environment variables")
            
            from groq import Groq
            self.llm_client = Groq(api_key=GROQ_API_KEY)
            # Usar modelo GPT-OSS disponível na conta
            self.llm_model = GROQ_MODEL
            logger.info(f"Using Groq model: {self.llm_model}")
            
        elif self.llm_provider == "openai":
            if not OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            
            from openai import OpenAI
            self.llm_client = OpenAI(api_key=OPENAI_API_KEY)
            self.llm_model = "gpt-4-turbo-preview"
            
        elif self.llm_provider == "google":
            if not GOOGLE_API_KEY:
                raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
            import google.generativeai as genai
            genai.configure(api_key=GOOGLE_API_KEY)
            self.llm_client = genai.GenerativeModel('gemini-pro')
            self.llm_model = "gemini-pro"
        
        elif self.llm_provider == "ollama":
            # Local Ollama - sem necessidade de API key
            try:
                import ollama
                self.llm_client = ollama
                self.llm_model = "llama3.1:8b"  # Modelo padrão
                # Testar conexão
                ollama.list()
                logger.info("Connected to local Ollama instance")
            except Exception as e:
                raise ValueError(
                    f"Failed to connect to Ollama. Make sure Ollama is running: {e}\n"
                    "Install: https://ollama.com/download\n"
                    "Start: ollama serve"
                )
            
        else:
            raise ValueError(f"Unknown LLM provider: {self.llm_provider}")
        
        logger.info(f"LLM initialized: {self.llm_model}")
    
    def build_knowledge_base(self, force_rebuild: bool = False):
        """
        Build the knowledge base from reviews
        
        Args:
            force_rebuild: Force rebuild even if exists
        """
        logger.info("Building knowledge base...")
        
        # Try to load existing vector store
        try:
            if not force_rebuild:
                dimension = self.embeddings_gen.embedding_dimension
                if dimension is None:
                    self.embeddings_gen.load_model()
                    dimension = self.embeddings_gen.embedding_dimension
                
                self.vector_store = VectorStore(dimension=dimension)
                self.vector_store.load()
                logger.info("Loaded existing vector store")
                return
        except (FileNotFoundError, Exception) as e:
            logger.info(f"Creating new vector store: {e}")
        
        # Prepare data
        logger.info("Step 1/3: Preparing data...")
        self.data_prep.load_data()
        self.data_prep.clean_data()
        documents = self.data_prep.prepare_documents()
        
        logger.info(f"Prepared {len(documents)} documents")
        
        # Generate embeddings
        logger.info("Step 2/3: Generating embeddings...")
        embeddings = self.embeddings_gen.generate_embeddings(
            documents,
            show_progress=True
        )
        
        # Create vector store
        logger.info("Step 3/3: Building vector store...")
        self.vector_store = VectorStore(
            dimension=self.embeddings_gen.embedding_dimension
        )
        self.vector_store.add_documents(documents, embeddings)
        
        # Save vector store
        self.vector_store.save()
        
        logger.info("Knowledge base built successfully!")
    
    def retrieve(
        self, 
        query: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: User query
            filters: Optional metadata filters
            
        Returns:
            List of retrieved documents with scores
        """
        logger.info(f"Retrieving documents for query: '{query}'")
        
        # Generate query embedding
        query_embedding = self.embeddings_gen.generate_query_embedding(query)
        
        # Search vector store
        results = self.vector_store.search(
            query_embedding,
            top_k=self.top_k,
            filters=filters
        )
        
        # Format results
        retrieved_docs = []
        for doc, score in results:
            retrieved_docs.append({
                'content': doc['text'],
                'metadata': doc['metadata'],
                'score': score
            })
        
        logger.info(f"Retrieved {len(retrieved_docs)} documents")
        return retrieved_docs
    
    def generate_response(
        self, 
        query: str, 
        context_docs: List[Dict[str, Any]]
    ) -> str:
        """
        Generate response using LLM
        
        Args:
            query: User query
            context_docs: Retrieved context documents
            
        Returns:
            Generated response
        """
        logger.info("Generating response with LLM...")
        
        # Prepare context
        context_parts = []
        for i, doc in enumerate(context_docs, 1):
            metadata = doc['metadata']
            context_parts.append(
                f"Review {i}:\n"
                f"Comentário: {doc['content']}\n"
                f"Nota: {metadata.get('review_score', 'N/A')}/5\n"
                f"Categoria: {metadata.get('product_category', 'N/A')}\n"
                f"Entrega: {metadata.get('delivery_status', 'N/A')}\n"
            )
        
        context = "\n".join(context_parts)
        
        # Create prompt
        prompt = create_rag_prompt(query, context)
        
        # Generate response based on provider
        try:
            if self.llm_provider == "groq":
                response = self.llm_client.chat.completions.create(
                    model=self.llm_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=TEMPERATURE,
                    max_tokens=1024
                )
                answer = response.choices[0].message.content
                
            elif self.llm_provider == "openai":
                response = self.llm_client.chat.completions.create(
                    model=self.llm_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=TEMPERATURE,
                    max_tokens=1024
                )
                answer = response.choices[0].message.content
                
            elif self.llm_provider == "google":
                response = self.llm_client.generate_content(
                    prompt,
                    generation_config={
                        'temperature': TEMPERATURE,
                        'max_output_tokens': 1024
                    }
                )
                answer = response.text
            
            elif self.llm_provider == "ollama":
                response = self.llm_client.chat(
                    model=self.llm_model,
                    messages=[{"role": "user", "content": prompt}],
                    options={
                        'temperature': TEMPERATURE,
                        'num_predict': 1024
                    }
                )
                answer = response['message']['content']
            
            logger.info("Response generated successfully")
            return answer
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error generating response: {error_msg}")
            
            # Tratamento específico de erros
            if "model_not_found" in error_msg or "does not exist" in error_msg:
                return (
                    f"❌ Erro: Modelo '{self.llm_model}' não encontrado.\n\n"
                    f"Configure um modelo disponível na variável GROQ_MODEL no arquivo .env\n"
                    f"Execute 'python list_models.py' para ver modelos disponíveis."
                )
            elif "invalid_api_key" in error_msg or "Unauthorized" in error_msg:
                return "❌ Erro: Chave de API inválida. Verifique GROQ_API_KEY no .env"
            elif "rate_limit" in error_msg or "429" in error_msg:
                return "❌ Erro: Limite de requisições excedido. Aguarde alguns segundos e tente novamente."
            elif "timeout" in error_msg.lower():
                return "❌ Erro: Timeout na comunicação com a API. Tente novamente."
            else:
                return f"❌ Erro ao gerar resposta: {error_msg}"
    
    def query(
        self, 
        question: str,
        filters: Optional[Dict[str, Any]] = None,
        return_sources: bool = True
    ) -> Dict[str, Any]:
        """
        Complete RAG query pipeline
        
        Args:
            question: User question
            filters: Optional metadata filters
            return_sources: Whether to include source documents
            
        Returns:
            Dictionary with answer and optionally sources
        """
        logger.info(f"Processing query: '{question}'")
        
        # Retrieve relevant documents
        retrieved_docs = self.retrieve(question, filters=filters)
        
        if not retrieved_docs:
            return {
                'answer': "Não encontrei avaliações relevantes para responder essa pergunta.",
                'sources': [] if return_sources else None
            }
        
        # Generate response
        answer = self.generate_response(question, retrieved_docs)
        
        result = {'answer': answer}
        
        if return_sources:
            result['sources'] = retrieved_docs
        
        return result


def main():
    """Test RAG pipeline"""
    logging.basicConfig(level=logging.INFO)
    
    print("\n" + "="*80)
    print("🚀 RAG PIPELINE TEST")
    print("="*80 + "\n")
    
    # Initialize pipeline
    print("1️⃣ Initializing pipeline...")
    pipeline = RAGPipeline(llm_provider="groq")
    pipeline.setup()
    
    # Build knowledge base
    print("\n2️⃣ Building knowledge base...")
    pipeline.build_knowledge_base()
    
    # Test queries
    test_queries = [
        "Quais são os principais problemas relatados pelos clientes?",
        "O que os clientes reclamam sobre atrasos na entrega?",
        "Quais aspectos da experiência de compra são mais elogiados?"
    ]
    
    print("\n3️⃣ Testing queries...\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*80}")
        print(f"Query {i}: {query}")
        print("="*80)
        
        result = pipeline.query(query)
        
        print(f"\n📝 Resposta:\n{result['answer']}")
        
        if result.get('sources'):
            print(f"\n📚 Fontes ({len(result['sources'])} reviews):")
            for j, source in enumerate(result['sources'][:3], 1):
                print(f"\n  Review {j}:")
                print(f"    Nota: {source['metadata']['review_score']}/5")
                print(f"    Comentário: {source['content'][:100]}...")
    
    print("\n" + "="*80)
    print("✅ RAG Pipeline test completed!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
