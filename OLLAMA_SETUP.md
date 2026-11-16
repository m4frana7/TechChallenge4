# 🦙 Guia Completo: Usar Llama Localmente com Ollama

## 🎯 Vantagens do Ollama

✅ **100% Gratuito** - Sem custos de API  
✅ **Privado** - Dados não saem do seu computador  
✅ **Offline** - Funciona sem internet  
✅ **Rápido** - Resposta local (sem latência de rede)  
✅ **Múltiplos Modelos** - Llama, Mistral, Phi, etc.

---

## 📋 Requisitos de Sistema

### **Mínimo:**
- **RAM:** 8GB (para Llama 3.2 3B)
- **Espaço:** 5GB livre
- **GPU:** Opcional (NVIDIA recomendado)

### **Recomendado:**
- **RAM:** 16GB+ (para Llama 3.1 8B)
- **Espaço:** 10GB+ livre
- **GPU:** NVIDIA com 8GB+ VRAM

---

## 🚀 Passo 1: Instalar Ollama

### **Windows:**

1. **Download:**
   ```
   https://ollama.com/download/windows
   ```

2. **Executar instalador**
   - `OllamaSetup.exe`
   - Next → Next → Install
   - Ollama inicia automaticamente em background

3. **Verificar instalação:**
   ```powershell
   ollama --version
   ```
   Deve mostrar algo como: `ollama version 0.1.x`

---

## 🦙 Passo 2: Baixar Modelo Llama

### **Opções de Modelos:**

```powershell
# OPÇÃO 1: Llama 3.2 3B (MAIS LEVE - ~2GB) ⭐ Para máquinas modestas
ollama pull llama3.2:3b

# OPÇÃO 2: Llama 3.1 8B (BALANCEADO - ~4.7GB) ⭐ RECOMENDADO
ollama pull llama3.1:8b

# OPÇÃO 3: Llama 3.1 70B (MELHOR QUALIDADE - ~40GB) - Apenas se tiver RAM suficiente
ollama pull llama3.1:70b

# OPÇÃO 4: Llama 3 8B (PORTUGUÊS OTIMIZADO - ~4.7GB)
ollama pull llama3:8b
```

**Tempo de download:** 5-20 minutos (dependendo da internet)

### **Verificar modelos instalados:**
```powershell
ollama list
```

---

## 🧪 Passo 3: Testar Ollama

### **Teste 1: Chat Simples**
```powershell
ollama run llama3.1:8b "Olá, como você está?"
```

### **Teste 2: Pergunta em Português**
```powershell
ollama run llama3.1:8b "Explique o que é RAG em 50 palavras"
```

### **Teste 3: Chat Interativo**
```powershell
ollama run llama3.1:8b
# Digite suas perguntas
# /bye para sair
```

---

## 🔧 Passo 4: Integrar com o Projeto

### **1. Atualizar Dependências**
```powershell
pip install ollama
```

### **2. Atualizar `.env`** (opcional)
```bash
# Modelo padrão do Ollama (opcional - padrão é llama3.1:8b)
OLLAMA_MODEL=llama3.1:8b

# Host do Ollama (opcional - padrão é http://localhost:11434)
OLLAMA_HOST=http://localhost:11434
```

### **3. Iniciar Ollama** (se não estiver rodando)
```powershell
# Verificar se está rodando:
ollama list

# Se não estiver, iniciar:
ollama serve
```

### **4. Usar no Pipeline RAG**

#### **Opção A: Via Python**
```python
from src.rag_pipeline import RAGPipeline

# Usar Ollama (local)
pipeline = RAGPipeline(llm_provider="ollama")
pipeline.setup()
pipeline.build_knowledge_base()

# Fazer pergunta
result = pipeline.query("Quais os principais problemas de entrega?")
print(result['answer'])
```

#### **Opção B: Via Streamlit**
```powershell
streamlit run app/streamlit_app.py
```
1. Selecione **"ollama"** no dropdown de provedor
2. Clique em "Inicializar Sistema"
3. Faça suas perguntas!

---

## ⚙️ Configuração Avançada

### **Mudar Modelo Llama**

Edite `src/rag_pipeline.py` linha ~50:

```python
elif self.llm_provider == "ollama":
    import ollama
    self.llm_client = ollama
    self.llm_model = "llama3.2:3b"  # ← Mude aqui
```

**Opções:**
- `llama3.2:3b` (mais leve)
- `llama3.1:8b` (balanceado) ⭐
- `llama3.1:70b` (melhor qualidade)
- `mistral:7b` (alternativa ao Llama)

### **Ajustar Parâmetros**

```python
response = self.llm_client.chat(
    model=self.llm_model,
    messages=[{"role": "user", "content": prompt}],
    options={
        'temperature': 0.3,      # Criatividade (0-1)
        'num_predict': 1024,     # Máximo de tokens
        'top_p': 0.9,            # Nucleus sampling
        'repeat_penalty': 1.1    # Penalidade por repetição
    }
)
```

---

## 🚀 Performance e Otimização

### **GPU Acceleration (NVIDIA)**

Ollama detecta automaticamente GPU NVIDIA e usa CUDA.

Verificar:
```powershell
ollama ps
# Mostra uso de GPU se disponível
```

### **Ajustar Memória**

Se ficar sem RAM:

```powershell
# Limitar contexto
ollama run llama3.1:8b --num-ctx 2048

# Ou usar modelo menor
ollama pull llama3.2:3b
```

### **Velocidade Esperada**

| Modelo | RAM | GPU | Tokens/seg |
|--------|-----|-----|-----------|
| 3B | 8GB | Não | ~10-20 |
| 8B | 16GB | Não | ~5-15 |
| 8B | 16GB | NVIDIA | ~30-50 |
| 70B | 64GB+ | NVIDIA | ~10-20 |

---

## 🔄 Comparação: Groq vs Ollama

| Aspecto | Groq (API) | Ollama (Local) |
|---------|------------|----------------|
| **Custo** | Grátis | Grátis |
| **Setup** | Fácil (API key) | Médio (instalar) |
| **Internet** | Necessário | Não necessário |
| **Privacidade** | Dados vão para Groq | 100% local |
| **Velocidade** | Muito rápido (~1s) | Depende do PC |
| **Qualidade** | Llama 70B | Depende do modelo |
| **RAM** | 0 (API) | 8-64GB |

---

## 🐛 Troubleshooting

### **Problema: "ollama: command not found"**
**Solução:** Reinicie o terminal após instalar

### **Problema: "connection refused"**
**Solução:** Iniciar servidor:
```powershell
ollama serve
```

### **Problema: "out of memory"**
**Solução:** Usar modelo menor:
```powershell
ollama pull llama3.2:3b
```

### **Problema: Muito lento**
**Soluções:**
1. Usar modelo menor (3B em vez de 8B)
2. Reduzir contexto (`num_ctx`)
3. Verificar se GPU está sendo usada: `ollama ps`
4. Fechar outros programas pesados

### **Problema: "model not found"**
**Solução:** Baixar modelo:
```powershell
ollama pull llama3.1:8b
```

---

## 📊 Testando Qualidade das Respostas

### **Teste Comparativo:**

```powershell
# Teste 1: Groq (API)
python -c "from src.rag_pipeline import RAGPipeline; p = RAGPipeline('groq'); p.setup(); p.build_knowledge_base(); print(p.query('Principais problemas?')['answer'])"

# Teste 2: Ollama (Local)
python -c "from src.rag_pipeline import RAGPipeline; p = RAGPipeline('ollama'); p.setup(); p.build_knowledge_base(); print(p.query('Principais problemas?')['answer'])"
```

Compare:
- ⏱️ Tempo de resposta
- 📝 Qualidade da resposta
- 🎯 Relevância das evidências citadas

---

## 🎯 Quando Usar Cada Opção?

### **Use Groq (API) se:**
✅ Você quer começar RÁPIDO  
✅ Não tem GPU potente  
✅ RAM limitada (<16GB)  
✅ Internet estável disponível  
✅ Quer máxima qualidade (Llama 70B)

### **Use Ollama (Local) se:**
✅ Privacidade é importante  
✅ Trabalha offline frequentemente  
✅ Tem PC potente (16GB+ RAM)  
✅ Prefere controle total  
✅ Quer experimentar diferentes modelos

---

## 🔗 Recursos Adicionais

- **Site Ollama:** https://ollama.com/
- **Documentação:** https://github.com/ollama/ollama
- **Modelos disponíveis:** https://ollama.com/library
- **Python SDK:** https://github.com/ollama/ollama-python

---

## ✅ Checklist de Setup

- [ ] Ollama instalado e rodando
- [ ] Modelo Llama baixado (3B, 8B, ou 70B)
- [ ] Testado com `ollama run`
- [ ] Biblioteca Python `ollama` instalada
- [ ] Pipeline RAG funcionando com `llm_provider="ollama"`
- [ ] Interface Streamlit com opção "ollama" funcionando

---

## 🚀 Comando Rápido Para Começar:

```powershell
# 1. Instalar Ollama
# Download: https://ollama.com/download/windows

# 2. Baixar Llama
ollama pull llama3.1:8b

# 3. Testar
ollama run llama3.1:8b "Olá!"

# 4. Atualizar projeto
pip install ollama

# 5. Executar RAG
python -m src.rag_pipeline
# Quando perguntar o provider, digite: ollama

# 6. Ou usar interface
streamlit run app/streamlit_app.py
# Selecione "ollama" no dropdown
```

---

**Pronto! Agora você pode usar Llama 100% localmente! 🦙🎉**
