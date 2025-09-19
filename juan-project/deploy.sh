#!/bin/bash

echo "🚀 Deployando Pomodoro Timer na AWS..."

# Verificar se AWS CLI está configurado
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "❌ AWS CLI não configurado. Execute: aws configure"
    exit 1
fi

# Instalar dependências do CDK
echo "📦 Instalando dependências..."
cd infrastructure
pip install -r requirements.txt

# Bootstrap CDK (apenas primeira vez)
echo "🔧 Configurando CDK..."
cdk bootstrap

# Deploy da infraestrutura
echo "☁️ Deployando na AWS..."
cdk deploy --require-approval never

echo "✅ Deploy concluído!"
echo "🌐 Acesse o CloudFormation no console AWS para ver os recursos criados"