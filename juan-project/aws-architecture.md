# Arquitetura AWS - Pomodoro Timer

```mermaid
graph TB
    User[👤 Usuário] --> CF[☁️ CloudFront<br/>CDN Global]
    
    CF --> S3[📦 S3 Bucket<br/>Frontend Static<br/>HTML/CSS/JS]
    CF --> APIGW[🚪 API Gateway<br/>REST API<br/>/api/pomodoro/*]
    
    APIGW --> Lambda[⚡ Lambda Function<br/>Python Runtime<br/>Pomodoro Logic]
    
    Lambda --> CW[📊 CloudWatch<br/>Logs & Metrics]
    
    subgraph "AWS Free Tier Eligible"
        S3
        Lambda
        APIGW
        CF
        CW
    end
    
    subgraph "Deployment"
        CDK[🏗️ AWS CDK<br/>Infrastructure as Code<br/>Python]
        CDK --> S3
        CDK --> Lambda
        CDK --> APIGW
        CDK --> CF
    end
    
    style User fill:#e1f5fe
    style CF fill:#fff3e0
    style S3 fill:#e8f5e8
    style APIGW fill:#fce4ec
    style Lambda fill:#f3e5f5
    style CW fill:#e0f2f1
    style CDK fill:#fff8e1
```

## Componentes da Arquitetura

### Frontend (Static Web Hosting)
- **Amazon S3**: Hospedagem dos arquivos estáticos (HTML, CSS, JS)
- **CloudFront**: CDN para distribuição global e cache

### Backend (Serverless)
- **API Gateway**: Endpoint REST para comunicação com frontend
- **AWS Lambda**: Execução da lógica do Pomodoro Timer em Python

### Observabilidade
- **CloudWatch**: Logs e métricas de performance

### Deployment
- **AWS CDK**: Infraestrutura como código em Python

## Fluxo de Dados

1. **Usuário** acessa a aplicação web
2. **CloudFront** serve o frontend do S3 com cache global
3. **Frontend** faz chamadas AJAX para API Gateway
4. **API Gateway** roteia requests para Lambda
5. **Lambda** executa lógica do Pomodoro e retorna resposta
6. **CloudWatch** coleta logs e métricas automaticamente

## Benefícios da Arquitetura

- ✅ **Serverless**: Sem gerenciamento de servidores
- ✅ **Escalável**: Auto-scaling automático
- ✅ **Global**: CDN para baixa latência mundial
- ✅ **Custo-efetivo**: Pay-per-use, Free Tier elegível
- ✅ **Observável**: Logs e métricas integrados
