"""
Streamlit App Simplificado - Voice of Customer Intelligence RAG
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

import streamlit as st
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Voice of Customer Intelligence",
    page_icon="🎯",
    layout="wide"
)

# Title
st.title("🎯 Voice of Customer Intelligence")
st.markdown("### Análise Inteligente de Avaliações com RAG")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # LLM Provider (fixo em Groq por enquanto)
    st.info("🚀 Usando: **Groq (Llama 3.1 70B)**")
    
    # Initialize button
    if 'pipeline' not in st.session_state:
        st.session_state.pipeline = None
        st.session_state.ready = False
    
    if not st.session_state.ready:
        if st.button("🚀 Inicializar Sistema", use_container_width=True):
            try:
                with st.spinner("🔧 Inicializando pipeline RAG..."):
                    from src.rag_pipeline import RAGPipeline
                    
                    pipeline = RAGPipeline(llm_provider="groq")
                    pipeline.setup()
                    
                    with st.spinner("📚 Carregando base de conhecimento..."):
                        pipeline.build_knowledge_base()
                    
                    st.session_state.pipeline = pipeline
                    st.session_state.ready = True
                    st.success("✅ Sistema pronto!")
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")
                logger.error(f"Erro na inicialização: {e}", exc_info=True)
    else:
        st.success("✅ Sistema Pronto")
        if st.button("🔄 Reinicializar", use_container_width=True):
            st.session_state.pipeline = None
            st.session_state.ready = False
            st.rerun()
    
    st.divider()
    
    # Info
    st.header("ℹ️ Sobre")
    st.info("""
    Sistema RAG para análise de ~41k reviews do e-commerce Olist.
    
    **Funcionalidades:**
    - Busca semântica
    - Respostas com evidências
    - Powered by Groq + Llama 3.1
    """)
    
    # Examples
    st.header("💡 Exemplos")
    st.markdown("""
    - Quais os principais problemas?
    - O que reclamam sobre entrega?
    - Quais aspectos são elogiados?
    """)

# Main content
if not st.session_state.ready:
    st.warning("⚠️ Por favor, inicialize o sistema usando o botão na barra lateral.")
    st.stop()

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Query input
st.markdown("### 💬 Faça sua Pergunta")
query = st.text_input(
    "Digite sua pergunta:",
    placeholder="Ex: Quais são os principais problemas relatados pelos clientes?",
    key="query_input"
)

col1, col2 = st.columns([1, 5])
with col1:
    search_button = st.button("🔍 Buscar", use_container_width=True)
with col2:
    if st.button("🗑️ Limpar", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# Process query
if search_button and query:
    with st.spinner("🔄 Processando pergunta..."):
        try:
            # Query pipeline
            result = st.session_state.pipeline.query(
                query,
                return_sources=True
            )
            
            # Add to history
            st.session_state.chat_history.append({
                'query': query,
                'result': result
            })
            
            # Display result
            st.success("✅ Resposta gerada!")
            
            # Answer
            st.markdown("### 📝 Resposta")
            st.markdown(result['answer'])
            
            # Sources
            if result.get('sources'):
                st.markdown("### 📚 Evidências Utilizadas")
                st.info(f"*{len(result['sources'])} avaliações recuperadas*")
                
                for i, source in enumerate(result['sources'], 1):
                    metadata = source['metadata']
                    content = source['content']
                    
                    # Extract comment
                    if "Comentário:" in content:
                        comment = content.split("Comentário:")[1].split("|")[0].strip()
                    else:
                        comment = content[:200]
                    
                    with st.expander(f"Review {i} - Nota {metadata.get('review_score', 'N/A')}/5"):
                        st.markdown(f"**Comentário:** {comment}")
                        st.markdown(f"**Categoria:** {metadata.get('product_category', 'N/A')}")
                        st.markdown(f"**Entrega:** {metadata.get('delivery_status', 'N/A')}")
            
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")
            logger.error(f"Erro na query: {e}", exc_info=True)

# History
if st.session_state.chat_history:
    st.divider()
    st.markdown("### 📜 Histórico")
    
    for i, item in enumerate(reversed(st.session_state.chat_history), 1):
        with st.expander(f"Pergunta {len(st.session_state.chat_history) - i + 1}: {item['query']}", expanded=(i == 1)):
            st.markdown("**Resposta:**")
            st.markdown(item['result']['answer'])
            
            if item['result'].get('sources'):
                st.caption(f"Baseado em {len(item['result']['sources'])} avaliações")
