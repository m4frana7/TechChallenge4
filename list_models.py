"""
Lista modelos disponíveis no Groq
"""
import os
from dotenv import load_dotenv

# Carregar .env
load_dotenv()

try:
    from groq import Groq
    
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("❌ GROQ_API_KEY não encontrada no .env")
        exit(1)
    
    print("🔍 Conectando ao Groq...\n")
    client = Groq(api_key=api_key)
    
    print("=" * 80)
    print("📋 MODELOS DISPONÍVEIS NO GROQ")
    print("=" * 80)
    
    # Listar modelos
    models = client.models.list()
    
    print(f"\n✅ Total de {len(models.data)} modelos encontrados:\n")
    
    # Separar por tipo
    text_models = []  # Modelos para geração de texto
    audio_models = []
    safety_models = []
    
    for model in models.data:
        model_id = model.id
        
        # Classificar modelos
        if 'whisper' in model_id.lower():
            audio_models.append(model_id)
        elif 'guard' in model_id.lower() or 'safeguard' in model_id.lower():
            safety_models.append(model_id)
        else:
            text_models.append(model_id)
    
    # Mostrar modelos de texto (adequados para RAG)
    if text_models:
        print("\n💬 MODELOS DE GERAÇÃO DE TEXTO (Adequados para RAG):")
        print("-" * 80)
        for i, model in enumerate(sorted(text_models), 1):
            # Destacar os modelos GPT-OSS
            star = " ⭐" if "gpt-oss" in model and "120b" in model else ""
            star = " 🔸" if "gpt-oss" in model and "20b" in model else star
            print(f"  {i}. {model}{star}")
    
    # Mostrar modelos de áudio
    if audio_models:
        print("\n🎤 MODELOS DE ÁUDIO (Transcrição):")
        print("-" * 80)
        for i, model in enumerate(sorted(audio_models), 1):
            print(f"  {i}. {model}")
    
    # Mostrar modelos de segurança
    if safety_models:
        print("\n�️ MODELOS DE SEGURANÇA:")
        print("-" * 80)
        for i, model in enumerate(sorted(safety_models), 1):
            print(f"  {i}. {model}")
    
    print("\n" + "=" * 80)
    print("💡 RECOMENDAÇÕES:")
    print("=" * 80)
    print("\n🎯 Para o Tech Challenge (Português + RAG):")
    
    # Recomendar apenas modelos que existem na lista
    recommended = []
    for model in text_models:
        if "gpt-oss-120b" in model:
            recommended.append((model, "⭐ MELHOR (mais poderoso)"))
        elif "gpt-oss-20b" in model and "safeguard" not in model:
            recommended.append((model, "🔸 ALTERNATIVA (mais rápido)"))
    
    if recommended:
        for model, desc in recommended:
            print(f"   • {model.ljust(40)} {desc}")
    else:
        print("   • Nenhum modelo específico recomendado encontrado")
        print("   • Use qualquer modelo de texto disponível acima")
    
    print("\n📝 Para alterar o modelo, edite o arquivo .env:")
    print(f'   GROQ_MODEL=openai/gpt-oss-120b')
    
    print("\n✅ Modelo atual configurado:")
    current_model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    if current_model in [m.id for m in models.data]:
        print(f"   ✓ {current_model} (disponível)")
    else:
        print(f"   ✗ {current_model} (NÃO ENCONTRADO - atualize o .env!)")
    
    print("\n✅ Conexão com Groq funcionando perfeitamente!")
    print("=" * 80 + "\n")
    
except ImportError:
    print("❌ Biblioteca 'groq' não instalada")
    print("Execute: pip install groq")
except Exception as e:
    print(f"❌ Erro ao conectar com Groq: {e}")
    print("\nVerifique:")
    print("  1. Se a GROQ_API_KEY está correta no .env")
    print("  2. Se tem internet conectada")
    print("  3. Se a API key não foi revogada")
