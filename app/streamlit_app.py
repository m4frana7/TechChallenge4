"""
Voice of Customer Intelligence - Central de Ajuda com IA
Interface FIAP - Design Dark Theme
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import streamlit as st
from src.rag_pipeline import RAGPipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Voice of Customer Intelligence - FIAP",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Local styling keeps the interface available without external font requests.
st.markdown(
    "<style>" + Path(__file__).with_name("styles.css").read_text(encoding="utf-8") + "</style>",
    unsafe_allow_html=True,
)

# Initialize session state
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = None
if 'ready' not in st.session_state:
    st.session_state.ready = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


def initialize_pipeline(llm_provider: str):
    """Initialize RAG pipeline"""
    try:
        with st.spinner("🔧 Inicializando sistema inteligente..."):
            pipeline = RAGPipeline(llm_provider=llm_provider)
            pipeline.setup()
            
            with st.spinner("📚 Carregando base de conhecimento..."):
                pipeline.build_knowledge_base()
            
            st.session_state.pipeline = pipeline
            st.session_state.ready = True
            st.success("✅ Sistema pronto para uso!")
            st.balloons()
            
    except Exception as e:
        st.error(f"❌ Erro ao inicializar: {str(e)}")
        logger.error(f"Pipeline error: {e}", exc_info=True)


def get_score_badge(score: int) -> str:
    """Generate HTML badge for review score"""
    emojis = {5: "😊", 4: "🙂", 3: "😐", 2: "😕", 1: "😞"}
    classes = {5: "positive", 4: "positive", 3: "neutral", 2: "negative", 1: "negative"}
    
    emoji = emojis.get(score, "⭐")
    css_class = classes.get(score, "neutral")
    
    return f'<span class="score-badge score-{css_class}">{emoji} {score}/5</span>'


def display_review(review: dict, index: int):
    """Display a modern review card with FIAP dark theme"""
    metadata = review['metadata']
    score = metadata.get('review_score', 'N/A')
    category = metadata.get('product_category', 'N/A')
    delivery = metadata.get('delivery_status', 'N/A')
    content = review['content']
    
    # Extract comment
    if "Comentário:" in content:
        comment = content.split("Comentário:")[1].split("|")[0].strip()
    else:
        comment = content
    
    st.markdown(f"""
    <div class="review-card">
        <div class="review-header">
            <span class="review-number">📝 Review #{index}</span>
            {get_score_badge(score)}
        </div>
        <div class="review-content">
            {comment}
        </div>
        <div class="review-metadata">
            <span class="metadata-item">📦 <strong>Categoria:</strong> {category}</span>
            <span class="metadata-item">🚚 <strong>Entrega:</strong> {delivery}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# Main app
def main():
    # Project identity and title hierarchy.
    st.markdown("""
    <div class="main-header">
        <div class="hero-topline">
            <span class="challenge-label">TECH CHALLENGE</span>
            <span class="project-label">FIAP / INTELIGÊNCIA ARTIFICIAL</span>
        </div>
        <p class="hero-subtitle">Análise de Avaliações de Clientes com Inteligência Artificial - FIAP Tech Challenge</p>
        <h1>Voice of Customer Intelligence</h1>
        <div class="hero-tags"><span>AVALIAÇÕES REAIS</span><span>BUSCA SEMÂNTICA</span><span>RESPOSTAS COM EVIDÊNCIAS</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-brand">FIAP</div><div class="sidebar-caption">PÓS TECH · TECH CHALLENGE</div>', unsafe_allow_html=True)
        st.markdown("### Configurações")
        
        # LLM Provider
        llm_provider = st.selectbox(
            "🤖 Provedor de IA",
            options=["groq", "openai", "google", "ollama"],
            help="Selecione o provedor de Inteligência Artificial"
        )
        
        st.markdown("---")
        
        # Initialize/Reset
        if not st.session_state.ready:
            if st.button("Iniciar Sistema", use_container_width=True, type="primary"):
                initialize_pipeline(llm_provider)
        else:
            st.success("✅ Sistema Ativo")
            if st.button("🔄 Reiniciar", use_container_width=True):
                st.session_state.pipeline = None
                st.session_state.ready = False
                st.rerun()
        
        st.markdown("---")
        st.markdown("### Filtros Avançados")
        
        score_filter = st.select_slider(
            "⭐ Filtrar por Nota",
            options=["Todas", 1, 2, 3, 4, 5],
            value="Todas"
        )
        
        sentiment_map = {
            "Todos": None,
            "😊 Positivo": "Positivo",
            "😐 Neutro": "Neutro",
            "😞 Negativo": "Negativo"
        }
        
        sentiment_filter = st.selectbox(
            "😊 Filtrar por Sentimento",
            options=list(sentiment_map.keys())
        )
        
        st.markdown("---")
        st.markdown("### Sobre o Sistema")
        st.info("""
        **Tecnologia RAG**  
        Sistema de IA que analisa ~41 mil avaliações reais de clientes para responder suas perguntas com base em evidências.
        
        **Recursos:**
        - ✅ Busca semântica inteligente
        - ✅ Respostas fundamentadas
        - ✅ Filtros personalizados
        - ✅ Análise de sentimentos
        """)
    
    # Main content
    if not st.session_state.ready:
        st.markdown("""
        <div class="info-box">
            <h3>Transforme a voz do cliente em inteligência.</h3>
            <p>Para começar, clique em <strong>"Iniciar Sistema"</strong> na barra lateral. O sistema irá carregar a base de conhecimento com milhares de avaliações reais de clientes.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="suggestion-box">
            <div class="suggestion-title">EXPLORE AS POSSIBILIDADES</div>
            <div class="suggestion-grid">
                <div class="suggestion-item"><span>01</span>Quais são os principais problemas relatados pelos clientes?</div>
                <div class="suggestion-item"><span>02</span>O que os clientes reclamam sobre entregas?</div>
                <div class="suggestion-item"><span>03</span>Quais aspectos da experiência são mais elogiados?</div>
                <div class="suggestion-item"><span>04</span>Quais problemas aparecem nas avaliações negativas?</div>
                <div class="suggestion-item"><span>05</span>Quais padrões aparecem sobre a qualidade dos produtos?</div>
                <div class="suggestion-item"><span>06</span>Como está o desempenho das entregas?</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Query interface
    st.markdown("### 💭 Como posso ajudar você hoje?")
    
    query = st.text_input(
        "Sua pergunta sobre as avaliações",
        placeholder="Digite sua pergunta aqui... Ex: Quais os principais problemas de entrega?",
        key="query_input",
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        search_button = st.button("Buscar Resposta", use_container_width=True, type="primary")
    with col2:
        clear_button = st.button("🗑️ Limpar Histórico", use_container_width=True)
    
    if clear_button:
        st.session_state.chat_history = []
        st.success("🗑️ Histórico limpo!")
        st.rerun()
    
    # Process query
    if search_button and query:
        with st.spinner("🤔 Analisando sua pergunta e buscando evidências..."):
            try:
                # Build filters
                filters = {}
                if score_filter != "Todas":
                    filters['review_score'] = score_filter
                if sentiment_filter != "Todos":
                    filters['sentiment'] = sentiment_map[sentiment_filter]
                
                # Query pipeline
                result = st.session_state.pipeline.query(
                    query,
                    filters=filters if filters else None,
                    return_sources=True
                )
                
                # Add to history
                st.session_state.chat_history.append({
                    'query': query,
                    'result': result,
                    'filters': filters
                })
                
                # Display result
                st.markdown("""
                <div class="response-box">
                    <div class="response-title">🤖 Resposta da IA</div>
                """, unsafe_allow_html=True)
                
                st.markdown(result['answer'])
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Sources
                if result.get('sources'):
                    # Stats counter
                    st.markdown(f"""
                    <div class="stats-counter">
                        <h2>{len(result['sources'])}</h2>
                        <p>Avaliações Analisadas</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("### 📚 Evidências Encontradas")
                    
                    for i, source in enumerate(result['sources'], 1):
                        display_review(source, i)
                
            except Exception as e:
                st.error(f"❌ Erro ao processar consulta: {str(e)}")
                logger.error(f"Query error: {e}", exc_info=True)
    
    # History
    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("### 📜 Histórico de Consultas")
        
        for i, item in enumerate(reversed(st.session_state.chat_history[-5:]), 1):
            with st.expander(f"🔍 {item['query']}", expanded=(i == 1)):
                st.markdown("**💬 Resposta:**")
                st.write(item['result']['answer'])
                
                if item['filters']:
                    st.markdown("**🔧 Filtros aplicados:**")
                    st.json(item['filters'])


if __name__ == "__main__":
    main()
