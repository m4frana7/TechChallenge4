# ============================================================================
# Setup Script - Tech Challenge Fase 4
# Script de configuração automática do ambiente
# ============================================================================

Write-Host "`n============================================================================" -ForegroundColor Cyan
Write-Host "  Tech Challenge - Fase 4: Voice of Customer Intelligence" -ForegroundColor Cyan
Write-Host "  Setup Automático" -ForegroundColor Cyan
Write-Host "============================================================================`n" -ForegroundColor Cyan

# Verificar Python
Write-Host "[1/6] Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python não encontrado! Instale Python 3.9+ e tente novamente." -ForegroundColor Red
    exit 1
}

# Criar ambiente virtual
Write-Host "`n[2/6] Criando ambiente virtual..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  ! Ambiente virtual já existe, pulando..." -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "  ✓ Ambiente virtual criado" -ForegroundColor Green
}

# Ativar ambiente virtual
Write-Host "`n[3/6] Ativando ambiente virtual..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
Write-Host "  ✓ Ambiente virtual ativado" -ForegroundColor Green

# Atualizar pip
Write-Host "`n[4/6] Atualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "  ✓ pip atualizado" -ForegroundColor Green

# Instalar dependências
Write-Host "`n[5/6] Instalando dependências..." -ForegroundColor Yellow
Write-Host "  (Isso pode levar alguns minutos...)" -ForegroundColor Gray
pip install -r requirements.txt --quiet
Write-Host "  ✓ Dependências instaladas" -ForegroundColor Green

# Configurar .env
Write-Host "`n[6/6] Configurando variáveis de ambiente..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  ! Arquivo .env já existe, pulando..." -ForegroundColor Yellow
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "  ✓ Arquivo .env criado" -ForegroundColor Green
}

# Resumo
Write-Host "`n============================================================================" -ForegroundColor Cyan
Write-Host "  ✓ Setup Concluído com Sucesso!" -ForegroundColor Green
Write-Host "============================================================================`n" -ForegroundColor Cyan

Write-Host "📋 Próximos passos:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  1. Configure suas API keys no arquivo .env" -ForegroundColor White
Write-Host "     Edite o arquivo e adicione pelo menos uma chave:" -ForegroundColor Gray
Write-Host "     - GROQ_API_KEY (recomendado, grátis)" -ForegroundColor Gray
Write-Host "     - OPENAI_API_KEY (pago)" -ForegroundColor Gray
Write-Host "     - GOOGLE_API_KEY (free tier)" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Execute o notebook EDA:" -ForegroundColor White
Write-Host "     jupyter notebook" -ForegroundColor Cyan
Write-Host "     > Abra: notebooks/eda_olist_reviews.ipynb" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. Teste o pipeline RAG:" -ForegroundColor White
Write-Host "     python -m src.rag_pipeline" -ForegroundColor Cyan
Write-Host ""
Write-Host "  4. Execute a interface:" -ForegroundColor White
Write-Host "     streamlit run app/streamlit_app.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "📖 Documentação completa: NEXT_STEPS.md" -ForegroundColor Yellow
Write-Host ""
Write-Host "🚀 Boa sorte no Tech Challenge!" -ForegroundColor Green
Write-Host ""
