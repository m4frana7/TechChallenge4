# ⚡ Quick Start - Tech Challenge Fase 4

## 🚀 Começar em 5 Minutos

### **1. Setup Automático** (recomendado)

```powershell
# Execute este comando na raiz do projeto:
.\setup.ps1
```

Este script vai:
- ✅ Criar ambiente virtual
- ✅ Instalar todas as dependências
- ✅ Configurar arquivo .env

---

### **2. Setup Manual**

```powershell
# Criar ambiente virtual
python -m venv venv

# Ativar
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar .env
copy .env.example .env
# Edite .env e adicione suas API keys
```

---

## 🔑 Configurar LLM

### **OPÇÃO A: Groq API (Recomendado - Grátis e Rápido)** ⭐

1. Acesse: https://console.groq.com/
2. Crie conta (grátis)
3. Vá em "API Keys"
4. Crie nova key
5. Cole no `.env`:
   ```
   GROQ_API_KEY=gsk_...
   ```

### **OPÇÃO B: Ollama Local (100% Privado e Offline)** 🦙

1. Baixe: https://ollama.com/download/windows
2. Instale e execute
3. Baixe modelo Llama:
   ```powershell
   ollama pull llama3.1:8b
   ```
4. Teste:
   ```powershell
   ollama run llama3.1:8b "Olá!"
   ```
5. No código, use:
   ```python
   pipeline = RAGPipeline(llm_provider="ollama")
   ```

📖 **Guia completo do Ollama:** Veja `OLLAMA_SETUP.md`

---

## 🎯 Executar Pipeline RAG

### **Opção 1: Script Completo** (recomendado para primeira vez)

```powershell
# Executar pipeline completo (prepara dados + cria índice + testa queries)
python -m src.rag_pipeline
```

**Tempo estimado:** 10-15 minutos na primeira execução  
**Próximas execuções:** Instantâneo (usa cache)

---

### **Opção 2: Passo a Passo**

```powershell
# 1. Preparar dados
python -m src.data_preparation

# 2. Testar embeddings
python -m src.embeddings

# 3. Testar vector store
python -m src.vector_store

# 4. Executar pipeline RAG
python -m src.rag_pipeline
```

---

## 🎨 Interface Streamlit

```powershell
streamlit run app/streamlit_app.py
```

Abre no navegador automaticamente em `http://localhost:8501`

---

## 📊 Análise Exploratória (EDA)

```powershell
jupyter notebook
```

Abra: `notebooks/eda_olist_reviews.ipynb`

---

## 🧪 Testes

```powershell
# Todos os testes
pytest tests/ -v

# Com cobertura
pytest --cov=src tests/
```

---

## 📝 Comandos Úteis

### **Validar Configuração**
```powershell
python -m src.config
```

### **Verificar Imports**
```powershell
python -c "from src.rag_pipeline import RAGPipeline; print('OK')"
```

### **Limpar Cache**
```powershell
Remove-Item -Recurse -Force data\, models\, __pycache__\
```

---

## 🎯 Testar com Perguntas

### **Via Python**
```python
from src.rag_pipeline import RAGPipeline

# Inicializar
pipeline = RAGPipeline(llm_provider="groq")
pipeline.setup()
pipeline.build_knowledge_base()

# Fazer pergunta
result = pipeline.query("Quais os principais problemas de entrega?")
print(result['answer'])
```

### **Via Streamlit**
1. Execute: `streamlit run app/streamlit_app.py`
2. Clique em "Inicializar Sistema"
3. Digite sua pergunta
4. Clique em "Buscar"

---

## 📦 Estrutura de Arquivos

```
Tech-Challenge-Fase4/
├── dados/                    # 10 CSVs do dataset Olist
├── notebooks/                # 1 notebook EDA
├── src/                      # 7 módulos Python
├── app/                      # 1 interface Streamlit
├── tests/                    # 1 arquivo de testes
├── README.md                 # Documentação completa
├── NEXT_STEPS.md            # Guia detalhado
├── ARCHITECTURE.md          # Arquitetura técnica
├── QUICK_START.md           # Este arquivo
└── requirements.txt         # Dependências
```

---

## ❓ Troubleshooting Rápido

### "Reviews CSV not found"
```powershell
# Execute o notebook EDA primeiro:
jupyter notebook
# Abra e execute: notebooks/eda_olist_reviews.ipynb
```

### "API key not found"
```powershell
# Verifique se o arquivo .env existe e tem a chave:
Get-Content .env | Select-String "GROQ_API_KEY"
```

### "Import error"
```powershell
# Reative o ambiente virtual:
venv\Scripts\activate
# Reinstale dependências:
pip install -r requirements.txt
```

---

## 🎬 Para o Vídeo (7 min)

### **Preparação:**
```powershell
# 1. Executar EDA e gerar visualizações
jupyter notebook notebooks/eda_olist_reviews.ipynb

# 2. Executar interface
streamlit run app/streamlit_app.py

# 3. Preparar 3-4 perguntas exemplo
```

### **Perguntas Sugeridas:**
1. "Quais os principais problemas relatados?"
2. "O que os clientes reclamam sobre entrega?"
3. "Quais aspectos são mais elogiados?"

---

## 📚 Documentação Completa

- **README.md** - Visão geral e setup
- **NEXT_STEPS.md** - Passo a passo detalhado
- **ARCHITECTURE.md** - Arquitetura técnica
- **QUICK_START.md** - Este arquivo

---

## ✅ Checklist de Entrega

- [ ] Setup completo funcionando
- [ ] EDA executado e documentado
- [ ] Pipeline RAG operacional
- [ ] Interface Streamlit rodando
- [ ] Vídeo de 7 minutos gravado
- [ ] Repositório GitHub público
- [ ] README.md completo

---

## 🆘 Precisa de Ajuda?

1. Leia **NEXT_STEPS.md** para guia detalhado
2. Leia **ARCHITECTURE.md** para entender a estrutura
3. Consulte comentários no código
4. Verifique logs de erro

---

**Tempo total estimado: 1-2 horas** ⏱️

**Boa sorte! 🍀**
