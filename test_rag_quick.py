"""
Teste rápido do pipeline RAG sem reconstruir a base de conhecimento
"""
import logging
import sys
sys.path.append('.')

from src.rag_pipeline import RAGPipeline

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

print("\n" + "="*80)
print("🚀 TESTE RÁPIDO DO PIPELINE RAG")
print("="*80 + "\n")

# Inicializar pipeline
print("1️⃣ Inicializando pipeline com Groq...")
pipeline = RAGPipeline(llm_provider="groq")
pipeline.setup()

# Tentar carregar base existente
print("\n2️⃣ Carregando base de conhecimento existente...")
try:
    pipeline.build_knowledge_base(force_rebuild=False)
    print("✅ Base de conhecimento carregada")
except Exception as e:
    print(f"⚠️ Erro ao carregar base: {e}")
    print("ℹ️ Execute 'python -m src.rag_pipeline' para criar a base primeiro")
    sys.exit(1)

# Teste de query simples
print("\n3️⃣ Testando query...\n")
query = "Quais são os principais problemas relatados pelos clientes?"

print(f"❓ Pergunta: {query}")
print("-" * 80)

result = pipeline.query(query, return_sources=True)

print(f"\n📝 Resposta:\n{result['answer']}")

if result.get('sources'):
    print(f"\n📚 Fontes recuperadas: {len(result['sources'])} reviews")
    for i, source in enumerate(result['sources'][:2], 1):
        print(f"\n  Review {i}:")
        print(f"    Nota: {source['metadata']['review_score']}/5")
        print(f"    Trecho: {source['content'][:80]}...")

print("\n" + "="*80)
print("✅ Teste concluído com sucesso!")
print("="*80 + "\n")
