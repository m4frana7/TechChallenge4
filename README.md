# 🎯 Tech Challenge - Fase 4: Voice of Customer Intelligence com RAG

Sistema de **Voice of Customer Intelligence** baseado em **RAG (Retrieval-Augmented Generation)** para análise inteligente de avaliações de clientes do e-commerce brasileiro Olist.

---

## 📋 Sobre o Projeto

Este projeto implementa uma solução de IA Generativa que permite explorar e analisar milhares de avaliações de clientes através de perguntas em linguagem natural, utilizando técnicas de RAG para garantir respostas fundamentadas em evidências reais.

### 🎓 Contexto Acadêmico

Projeto desenvolvido como parte do **Tech Challenge - Fase 4** da Pós-Tech em IA para Devs (FIAP/Alura).

**Objetivos:**
- Implementar pipeline RAG completo
- Construir base de conhecimento a partir de reviews
- Gerar respostas fundamentadas em evidências
- Criar interface para exploração inteligente dos dados

---

## 🗂️ Estrutura do Projeto

```
Tech-Challenge-Fase4/
├── dados/                          # Datasets originais
│   ├── olist_order_reviews_dataset.csv
│   ├── olist_orders_dataset.csv
│   ├── olist_products_dataset.csv
│   └── reviews_for_rag.csv        # Dataset preparado (gerado pelo EDA)
│
├── notebooks/                      # Jupyter notebooks
│   └── eda_olist_reviews.ipynb    # Análise exploratória
│
├── src/                            # Código fonte
│   ├── __init__.py
│   ├── config.py                  # Configurações
│   ├── utils.py                   # Funções auxiliares
│   ├── data_preparation.py        # Preparação dos dados
│   ├── embeddings.py              # Geração de embeddings
│   ├── vector_store.py            # Vector database (FAISS)
│   └── rag_pipeline.py            # Pipeline RAG completo
│
├── app/                            # Interface do usuário
│   └── streamlit_app.py           # App Streamlit
│
├── tests/                          # Testes
│   └── test_rag.py
│
├── requirements.txt                # Dependências Python
├── .env.example                    # Template de variáveis de ambiente
├── .gitignore
└── README.md                       # Este arquivo
```

---

## 🚀 Quick Start

### 1. Clone o Repositório

```bash
git clone https://github.com/m4frana7/TechChallenge4.git
cd TechChallenge4
```

### 2. Configurar Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

```bash
# Copiar template
cp .env.example .env

# Editar .env e adicionar suas API keys
# Pelo menos uma chave é necessária: OpenAI, Groq, ou Google
```

### 5. Executar EDA (Análise Exploratória)

```bash
jupyter notebook notebooks/eda_olist_reviews.ipynb
```

Este notebook vai:
- Analisar os dados de reviews
- Gerar visualizações
- Criar o arquivo `dados/reviews_for_rag.csv`

### 6. Testar Preparação dos Dados

```bash
python -m src.data_preparation
```

### 7. Executar Interface

```bash
streamlit run app/streamlit_app.py
```

---

## 📊 Dataset

**Fonte:** [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

**Período:** 2016-2018  
**Total de pedidos:** ~100.000  
**Reviews com comentários:** ~41.000

### Principais campos utilizados:
- `review_comment_message`: Comentário textual do cliente
- `review_score`: Nota de 1 a 5
- `product_category_name`: Categoria do produto
- `delivery_status`: Status da entrega (antecipado/no prazo/atrasado)

---

## 🧠 Arquitetura do RAG

### Pipeline:

```
1. Pergunta do Usuário
   ↓
2. Geração de Embedding da Pergunta
   ↓
3. Busca Semântica no Vector Store
   ↓
4. Recuperação dos Top-K Reviews Relevantes
   ↓
5. Construção do Contexto
   ↓
6. Geração da Resposta pelo LLM
   ↓
7. Resposta Fundamentada + Evidências
```

### Tecnologias:

- **Embeddings:** Sentence Transformers (paraphrase-multilingual-MiniLM-L12-v2)
- **Vector Store:** FAISS (local)
- **LLM:** Groq / OpenAI / Google Gemini
- **Framework:** LangChain
- **Interface:** Streamlit

---

## 🎯 Exemplos de Uso

### Perguntas que o sistema pode responder:

```
✅ "Quais são os principais problemas relatados pelos clientes?"
✅ "O que os clientes reclamam sobre atrasos na entrega?"
✅ "Quais aspectos da experiência de compra são mais elogiados?"
✅ "Quais problemas são relatados por clientes insatisfeitos?"
✅ "Existem padrões nas avaliações relacionadas à qualidade dos produtos?"
✅ "O que os clientes dizem sobre a categoria eletrônicos?"
```

---

## 📈 Análise Exploratória (EDA)

O notebook de EDA (`notebooks/eda_olist_reviews.ipynb`) fornece:

### Análises Principais:
1. **Overview dos Reviews** - Estatísticas gerais e distribuição de notas
2. **Análise Textual** - Tamanho, qualidade e exemplos de comentários
3. **Sentimento por Nota** - Classificação positivo/neutro/negativo
4. **Palavras Frequentes** - Termos e temas mais recorrentes
5. **Metadados** - Correlação entre entrega, categoria e satisfação
6. **Insights para RAG** - Recomendações técnicas

### Principais Descobertas:
- 📊 57% das avaliações têm nota 5 (máxima)
- 📝 41% dos reviews contêm comentários textuais
- 🚚 Atraso na entrega está correlacionado com notas baixas
- 💬 Clientes insatisfeitos deixam comentários mais detalhados

---

## 🔧 Configuração Avançada

### Variáveis de Ambiente (.env):

```bash
# LLM API (escolha uma)
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...
GOOGLE_API_KEY=AIza...

# Embeddings
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2

# RAG Configuration
TOP_K_RESULTS=5
TEMPERATURE=0.3
CHUNK_SIZE=500
```

### Customização:

Para ajustar o comportamento do RAG, edite `src/config.py`:
- `TOP_K_RESULTS`: Número de reviews recuperados
- `TEMPERATURE`: Criatividade do LLM (0-1)
- `EMBEDDING_MODEL`: Modelo de embeddings

---

## 🧪 Testes

```bash
# Executar todos os testes
pytest tests/

# Executar com cobertura
pytest --cov=src tests/
```

---

## 📦 Dependências Principais

```
pandas >= 2.1.4          # Manipulação de dados
sentence-transformers    # Embeddings
faiss-cpu               # Vector store
langchain               # RAG framework
streamlit               # Interface
groq                    # LLM API (grátis)
```

---

## 🎬 Demonstração

[Link para vídeo de demonstração - 7 minutos]

### Conteúdo do vídeo:
1. Problema de negócio
2. Arquitetura da solução
3. Demonstração prática
4. Exemplos de perguntas e respostas
5. Evidências recuperadas
6. Desafios técnicos

---

## 👥 Equipe

- **Seu Nome** - [LinkedIn](https://linkedin.com/in/seuperfil) | [GitHub](https://github.com/seuperfil)

---

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais como parte do Tech Challenge da FIAP.

---

## 🙏 Agradecimentos

- **Olist** por disponibilizar o dataset
- **FIAP/Alura** pela estrutura do desafio
- **Comunidade Open Source** pelas ferramentas utilizadas

---

## 📚 Referências

- [Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- [LangChain Documentation](https://python.langchain.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [FAISS](https://github.com/facebookresearch/faiss)

---

## 🔄 Status do Projeto

- [x] EDA completo
- [x] Estrutura do projeto
- [ ] Preparação dos dados
- [ ] Geração de embeddings
- [ ] Implementação do RAG
- [ ] Interface Streamlit
- [ ] Testes
- [ ] Vídeo de apresentação
- [ ] Documentação final

---

**Última atualização:** Dezembro 2024


## Interface atualizada

O front usa tema escuro com detalhes em rosa e o cabeçalho:

- **TECH CHALLENGE**
- Análise de Avaliações de Clientes com Inteligência Artificial - FIAP Tech Challenge
- **Voice of Customer Intelligence**

O estilo está em `app/styles.css` e o tema nativo em `.streamlit/config.toml`.

### Dados e configuração local

Este repositório contém o código e o notebook. Datasets, modelos, índice vetorial,
ambiente virtual e chaves de API são mantidos fora do Git.
Baixe os datasets Olist pelo link da seção Dataset, coloque os CSVs em `dados/`
e execute o notebook para gerar `dados/reviews_for_rag.csv`.
O modelo será baixado e o índice será criado na primeira inicialização.
Copie `.env.example` para `.env` e configure sua chave localmente.

### Validação realizada

- Os quatro testes de `tests/test_rag.py` passaram usando os dados locais.
- Modelo e índice de 37.488 avaliações carregados; busca semântica verificada.
- Interface e inicialização conferidas com Streamlit AppTest.
- Layout verificado em desktop e tela estreita.
- Respostas reais via API externa ainda não foram validadas nesta sessão.

No Mac Apple Silicon, caso ocorra conflito de OpenMP entre PyTorch e FAISS,
use o runtime do PyTorch e uma thread ao iniciar o app:

```bash
export DYLD_LIBRARY_PATH="$(python -c 'import pathlib, torch; print(pathlib.Path(torch.__file__).parent / "lib")')"
export OMP_NUM_THREADS=1
streamlit run app/streamlit_app.py
```

Limitações identificadas na busca atual: `top_k` maior que o índice pode repetir
fontes, e filtros aplicados após o `top_k` podem omitir documentos compatíveis.
