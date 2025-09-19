# Estimativa de Custos - Pomodoro Timer AWS

## Recursos AWS Utilizados

### 1. AWS Lambda
- **Função**: Backend API do Pomodoro
- **Estimativa**: ~1000 invocações/mês
- **Custo**: ~$0.20/mês (dentro do free tier)

### 2. Amazon API Gateway
- **Uso**: REST API para comunicação frontend/backend
- **Estimativa**: ~1000 requests/mês
- **Custo**: ~$3.50/mês (após free tier)

### 3. Amazon S3
- **Uso**: Hospedagem do frontend estático
- **Estimativa**: <1GB storage, ~100 requests/mês
- **Custo**: ~$0.02/mês

### 4. Amazon CloudFront
- **Uso**: CDN para distribuição global
- **Estimativa**: ~1GB transfer/mês
- **Custo**: ~$0.08/mês

## Custo Total Estimado
- **Primeiro ano**: ~$0.30/mês (com free tier)
- **Após free tier**: ~$3.80/mês

## Otimizações de Custo
- Lambda dentro do free tier (1M requests/mês)
- S3 free tier (5GB storage, 20k requests)
- CloudFront free tier (1TB transfer/mês)
- API Gateway é o maior custo após free tier