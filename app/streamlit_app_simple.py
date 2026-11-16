"""
Streamlit App SIMPLIFICADO - Voice of Customer Intelligence
Versão sem imports complexos para testar
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Voice of Customer Intelligence",
    page_icon="🎯",
    layout="wide"
)

# Header
st.title("🎯 Voice of Customer Intelligence")
st.subheader("Análise Inteligente de Avaliações com RAG")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    
    llm_provider = st.selectbox(
        "Provedor LLM",
        options=["groq", "openai", "google", "ollama"]
    )
    
    if st.button("🚀 Inicializar Sistema", use_container_width=True):
        try:
            with st.spinner("Inicializando..."):
                # Tentar importar o pipeline
                import sys
                from pathlib import Path
                sys.path.append(str(Path(__file__).parent.parent))
                
                from src.rag_pipeline import RAGPipeline
                
                pipeline = RAGPipeline(llm_provider=llm_provider)
                pipeline.setup()
                pipeline.build_knowledge_base()
                
                st.session_state.pipeline = pipeline
                st.session_state.ready = True
                st.success("✅ Sistema pronto!")
                
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")
            st.error("Verifique se executou o notebook EDA e se a API key está configurada.")
    
    st.divider()
    st.info("""
    **Sobre:**
    Sistema RAG para análise de reviews do e-commerce Olist.
    """)

# Main content
if 'ready' not in st.session_state:
    st.session_state.ready = False

if not st.session_state.ready:
    st.warning("⚠️ Inicialize o sistema usando o botão na barra lateral.")
    st.info("**Passos necessários antes:**\n1. Execute o notebook EDA\n2. Configure API key no .env\n3. Clique em 'Inicializar Sistema'")
else:
    st.success("✅ Sistema pronto para uso!")
    
    # Query input
    query = st.text_input(
        "Digite sua pergunta:",
        placeholder="Ex: Quais são os principais problemas relatados pelos clientes?"
    )
    
    if st.button("🔍 Buscar"):
        if query:
            with st.spinner("Processando..."):
                try:
                    pipeline = st.session_state.pipeline
                    result = pipeline.query(query)
                    
                    st.markdown("### 📝 Resposta")
                    st.write(result['answer'])
                    
                    if result.get('sources'):
                        st.markdown("### 📚 Evidências")
                        for i, source in enumerate(result['sources'], 1):
                            with st.expander(f"Review {i} - Nota {source['metadata']['review_score']}/5"):
                                st.write(source['content'])
                                
                except Exception as e:
                    st.error(f"Erro ao processar: {str(e)}")
        else:
            st.warning("Digite uma pergunta primeiro!")
