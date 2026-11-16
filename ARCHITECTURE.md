# 🏗️ Arquitetura do Sistema RAG

## 📐 Visão Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                      USUÁRIO                                     │
│                 (Interface Streamlit)                            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   RAG PIPELINE                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  1. Query Processing                                     │  │
│  │     └─> Embedding Generation                             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                      │
│                           ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  2. Semantic Search                                      │  │
│  │     └─> FAISS Vector Store                               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                      │
│                           ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  3. Context Building                                     │  │
│  │     └─> Top-K Reviews + Metadata                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                      │
│                           ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  4. Response Generation                                  │  │
│  │     └─> LLM (Groq/OpenAI/Google)                         │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Fluxo de Dados Detalhado

### **1. Preparação dos Dados (Offline)**

```
CSV Files (Olist Dataset)
    │
    ├─> data_preparation.py
    │   ├─> Load data
    │   ├─> Clean text
    │   ├─> Filter reviews with comments
    │   ├─> Add sentiment classification
    │   └─> Prepare documents
    │
    ▼
Reviews + Metadata (41k documents)
    │
    ├─> embeddings.py
    │   └─> Sentence Transformer
    │       └─> paraphrase-multilingual-MiniLM-L12-v2
    │
    ▼
Vector Embeddings (41k × 384 dimensions)
    │
    ├─> vector_store.py
    │   └─> FAISS IndexFlatL2
    │
    ▼
Indexed Vector Store (saved to disk)
```

### **2. Query Processing (Online)**

```
User Question
    │
    ├─> embeddings.py
    │   └─> Generate query embedding (1 × 384)
    │
    ▼
Query Vector
    │
    ├─> vector_store.py
    │   └─> Similarity Search (L2 distance)
    │       └─> Apply filters (score, category, sentiment)
    │
    ▼
Top-K Similar Documents (default: 5)
    │
    ├─> rag_pipeline.py
    │   ├─> Format context
    │   ├─> Build prompt
    │   └─> Call LLM API
    │
    ▼
Generated Response + Evidence
```

---

## 📦 Módulos e Responsabilidades

### **src/config.py**
```python
📋 Configurações centralizadas
- Paths do projeto
- API keys
- Parâmetros do RAG
- Constantes
```

### **src/utils.py**
```python
🛠️ Funções auxiliares
- Limpeza de texto
- Classificação de sentimento
- Formatação de documentos
- Criação de prompts
```

### **src/data_preparation.py**
```python
🔧 Preparação de dados
- Carregamento de CSVs
- Limpeza e normalização
- Filtragem de reviews
- Geração de documentos estruturados
```

### **src/embeddings.py**
```python
🧠 Geração de embeddings
- Carregamento do modelo Sentence Transformer
- Encoding batch de documentos
- Embedding de queries individuais
- Cache de modelo
```

### **src/vector_store.py**
```python
🗄️ Banco de vetores
- Criação de índice FAISS
- Adição de documentos
- Busca por similaridade
- Aplicação de filtros
- Persistência (save/load)
```

### **src/rag_pipeline.py**
```python
🎯 Pipeline RAG completo
- Orquestração de componentes
- Build knowledge base
- Retrieve documents
- Generate responses
- Integração com LLMs
```

### **app/streamlit_app.py**
```python
🎨 Interface do usuário
- Chat interativo
- Visualização de evidências
- Filtros (nota, sentimento)
- Histórico de perguntas
```

---

## 🔧 Stack Tecnológica

### **Embeddings**
```
Model: paraphrase-multilingual-MiniLM-L12-v2
Provider: Sentence Transformers
Dimension: 384
Language: Multilingual (PT, EN, ES, etc)
Size: ~420MB
```

### **Vector Database**
```
Engine: FAISS (Facebook AI Similarity Search)
Index Type: IndexFlatL2 (exact search)
Distance Metric: L2 (Euclidean)
Storage: Local disk (pickle + faiss)
```

### **LLM Options**
```
Option 1: Groq (Recommended)
  - Model: llama-3.1-70b-versatile
  - Cost: FREE
  - Speed: Very fast (~1s)
  
Option 2: OpenAI
  - Model: gpt-4-turbo-preview
  - Cost: Paid
  - Quality: Highest
  
Option 3: Google Gemini
  - Model: gemini-pro
  - Cost: Free tier available
  - Speed: Fast
```

### **Framework**
```
Python: 3.9+
RAG: Custom (no LangChain dependency for core)
Interface: Streamlit
Testing: Pytest
```

---

## 📊 Dados e Metadados

### **Document Structure**
```python
{
    'id': 'review_{review_id}',
    'text': 'Comentário: ... | Nota: 5/5 | Categoria: ...',
    'metadata': {
        'review_id': str,
        'review_score': int (1-5),
        'sentiment': str ('Positivo', 'Neutro', 'Negativo'),
        'product_category': str,
        'delivery_status': str,
        'review_date': str,
        'comment_length': int
    }
}
```

### **Metadata Filters**
```python
filters = {
    'review_score': 5,              # Nota específica
    'sentiment': 'Negativo',         # Sentimento
    'product_category': 'electronics' # Categoria
}
```

---

## 🎯 Prompt Engineering

### **Sistema de Prompts**
```python
PROMPT_TEMPLATE = """
Você é um assistente especializado em análise de avaliações.

REGRAS:
1. Base respostas APENAS nas avaliações fornecidas
2. Cite exemplos específicos
3. Se não houver evidências, diga claramente
4. Não invente informações
5. Mencione quantas avaliações apoiam cada conclusão

CONTEXTO:
{retrieved_reviews}

PERGUNTA:
{user_query}

RESPOSTA:
"""
```

### **Estratégias**
- ✅ Few-shot learning com exemplos
- ✅ Chain-of-thought para análises complexas
- ✅ Instruções explícitas sobre citação de evidências
- ✅ Detecção de "sem evidências suficientes"

---

## 🔒 Segurança e Privacidade

### **API Keys**
```
✓ Armazenadas em .env (não versionado)
✓ Validação no startup
✓ Fallback entre providers
```

### **Dados**
```
✓ Dataset público (Olist)
✓ Sem PII (Personally Identifiable Information)
✓ Processamento local (embeddings)
✓ Vector store local (FAISS)
```

---

## ⚡ Performance

### **Indexação (Offline)**
```
41.000 reviews
↓ Embedding (batch 32) → ~5-10 min
↓ FAISS indexing → ~1 min
= Total: ~10-15 min (primeira vez)
= Cache: Instantâneo (carrega do disco)
```

### **Query (Online)**
```
User query
↓ Embedding → <100ms
↓ FAISS search → <50ms
↓ LLM generation → ~1-3s (Groq) / ~2-5s (GPT-4)
= Total: ~1-5s per query
```

### **Otimizações Possíveis**
```
1. FAISS IVF index (approximate search) → 10x faster
2. Quantization → 4x menos memória
3. GPU acceleration → 5-10x faster embedding
4. Response caching → instantâneo para queries repetidas
5. Async LLM calls → parallelização
```

---

## 📈 Escalabilidade

### **Atual (MVP)**
```
Documents: ~41k reviews
Index Size: ~60MB
Memory: ~500MB
Query Time: ~1-5s
```

### **Escala Futura**
```
Documents: 1M reviews
↓ Solution:
- FAISS IVF clustering
- Distributed search
- Batch processing
- Redis cache

Query Time: <1s (com optimizations)
```

---

## 🧪 Testing Strategy

### **Unit Tests**
```python
✓ Data cleaning functions
✓ Embedding generation
✓ Vector store operations
✓ Utilities
```

### **Integration Tests**
```python
✓ End-to-end pipeline
✓ LLM integration
✓ Query processing
```

### **Quality Tests**
```python
✓ Response relevance
✓ Evidence citation
✓ "No data" handling
```

---

## 🚀 Deployment Options

### **Option 1: Local**
```bash
streamlit run app/streamlit_app.py
```

### **Option 2: Streamlit Cloud**
```
- Push to GitHub
- Connect to Streamlit Cloud
- Set secrets (API keys)
- Deploy
```

### **Option 3: Docker**
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app/streamlit_app.py"]
```

---

## 📚 Documentação Adicional

- **README.md** - Guia completo do projeto
- **NEXT_STEPS.md** - Passo a passo de execução
- **requirements.txt** - Dependências Python
- **.env.example** - Template de configuração
- **notebooks/eda_olist_reviews.ipynb** - Análise exploratória

---

**Arquitetura projetada para ser:**
- ✅ **Modular** - Componentes independentes
- ✅ **Escalável** - Suporta crescimento
- ✅ **Testável** - Cobertura de testes
- ✅ **Documentada** - Código comentado
- ✅ **Reproduzível** - Setup automatizado
