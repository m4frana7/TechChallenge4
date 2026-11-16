"""
Teste rápido do RAG com Groq (Llama 3.1 70B - GRÁTIS)
"""

import sys
sys.path.append('.')

from src.rag_pipeline import RAGPipeline

print("="*80)
print("🦙 TESTE RAG COM LLAMA 3.1 70B (GROQ - GRÁTIS)")
print("="*80)

print("\n1️⃣ Inicializando pipeline com Groq (Llama)...")
pipeline = RAGPipeline(llm_provider="groq")
pipeline.setup()

print("\n2️⃣ Construindo base de conhecimento...")
pipeline.build_knowledge_base()

print("\n3️⃣ Testando pergunta...")
print("\n" + "="*80)

pergunta = "Quais são os principais problemas relatados pelos clientes?"
print(f"❓ PERGUNTA: {pergunta}")
print("="*80)

result = pipeline.query(pergunta)

print("\n📝 RESPOSTA:")
print("-"*80)
print(result['answer'])
print("-"*80)

print(f"\n📚 EVIDÊNCIAS UTILIZADAS ({len(result['sources'])} reviews):")
for i, source in enumerate(result['sources'][:3], 1):
    print(f"\n{i}. Nota: {source['metadata']['review_score']}/5 | Categoria: {source['metadata'].get('product_category', 'N/A')}")
    comentario = source['content'].split('|')[0] if '|' in source['content'] else source['content']
    print(f"   {comentario[:200]}...")

print("\n" + "="*80)
print("✅ TESTE CONCLUÍDO!")
print("🎉 Você está usando Llama 3.1 70B GRATUITAMENTE via Groq!")
print("="*80)
