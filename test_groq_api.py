"""
Teste simples da API Groq com o modelo configurado
"""
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

print(f"🔧 Testando modelo: {model}")
print("🔑 API key configurada:", bool(api_key))

client = Groq(api_key=api_key)

try:
    print("\n📤 Enviando mensagem simples...")
    response = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user", 
            "content": "Responda em português: O que é RAG em IA?"
        }],
        temperature=0.3,
        max_tokens=200
    )
    
    answer = response.choices[0].message.content
    print("\n✅ Resposta recebida:\n")
    print(answer)
    print("\n✅ Teste concluído com sucesso!")
    
except Exception as e:
    print(f"\n❌ Erro: {e}")
