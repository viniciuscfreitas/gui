#!/bin/sh
# Script simples para verificar se tudo está OK - Grug-approved

echo "🔍 Verificando sintaxe Python..."
python3 -m py_compile app.py test_integration.py
if [ $? -eq 0 ]; then
    echo "✅ Sintaxe OK"
else
    echo "❌ Erro de sintaxe"
    exit 1
fi

echo ""
echo "🔍 Verificando imports..."
python3 -c "import app; print('✅ Imports OK')" 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Erro nos imports"
    exit 1
fi

echo ""
echo "🔍 Verificando se pytest está disponível..."
python3 -c "import pytest" 2>&1
if [ $? -eq 0 ]; then
    echo "✅ pytest disponível"
    echo ""
    echo "🧪 Rodando testes..."
    python3 -m pytest test_integration.py -v
    if [ $? -eq 0 ]; then
        echo "✅ Todos os testes passaram!"
    else
        echo "❌ Alguns testes falharam"
        exit 1
    fi
else
    echo "⚠️  pytest não instalado (instale com: pip install pytest)"
    echo "   Testes podem ser rodados dentro do Docker"
fi

echo ""
echo "✅ Verificação completa!"

