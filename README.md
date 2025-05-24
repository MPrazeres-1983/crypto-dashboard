# 🚀 CryptoDash - Real-Time Analytics

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://crypto-dashboard-jvjxcxcfzrz5bvk5zigjju.streamlit.app/)

🔗 **[🌐 Ver Demo Online](https://crypto-dashboard-jvjxcxcfzrz5bvk5zigjju.streamlit.app/)**

Dashboard profissional para análise de criptomoedas em tempo real demonstrando competências em:

- 📊 Visualização de dados com Plotly
- 🔄 APIs e integração em tempo real
- 🐳 DevOps com Docker e CI/CD
- 🧪 Testes automatizados
- ⚡ Deploy em produção

## 🛠️ Tecnologias

- Python, Streamlit, Plotly, Pandas
- GitHub Actions (CI/CD)
- Docker
- CoinGecko API

## ✨ Funcionalidades

- 📊 **Dados em Tempo Real**: Preços e métricas atualizadas via CoinGecko API
- 📈 **Visualizações Interativas**: Gráficos de preços, volume e distribuição
- 🔄 **Auto-refresh**: Atualização automática dos dados
- 📱 **Responsivo**: Interface adaptável para diferentes dispositivos
- 🐳 **Docker Ready**: Containerização completa
- 🧪 **Testes Automatizados**: Cobertura de testes com pytest
- 🚀 **CI/CD**: Pipeline automatizado com GitHub Actions

## 🛠️ Tecnologias

- **Backend**: Python 3.11, Streamlit
- **APIs**: CoinGecko API (dados de crypto)
- **Visualização**: Plotly, Pandas
- **Async**: aiohttp para requisições assíncronas
- **Containerização**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Testes**: pytest, pytest-asyncio

## 🚀 Quick Start

### Método 1: Execução Local

```bash
# Clone o repositório
git clone https://github.com/seu-utilizador/crypto-dashboard.git
cd crypto-dashboard

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
streamlit run app/main.py
```

### Método 2: Docker

```bash
# Build e execute com Docker Compose
docker-compose -f docker/docker-compose.yml up --build

# Ou execute diretamente
docker build -f docker/Dockerfile -t crypto-dashboard .
docker run -p 8501:8501 crypto-dashboard
```

Acesse: `http://localhost:8501`

## 📊 Funcionalidades Detalhadas

### Dashboard Principal

- **Métricas em Tempo Real**: Preço atual, variação 24h, market cap
- **Seleção Dinâmica**: Escolha múltiplas criptomoedas
- **Alertas Visuais**: Indicadores de alta/baixa com cores

### Análise Técnica

- **Gráficos de Preços**: Histórico com volume de negociação
- **Distribuição**: Visualização por market cap
- **Comparação**: Análise lado a lado de múltiplas moedas

### Insights Automáticos

- **Maiores Altas**: Top performers do período
- **Maiores Baixas**: Moedas em declínio
- **Tendências**: Análise de padrões

## 🧪 Testes

```bash
# Execute todos os testes
pytest tests/ -v

# Teste com cobertura
pytest tests/ --cov=app --cov-report=html
```

## 🔧 Configuração

Edite `app/config.py` para personalizar:

- APIs utilizadas
- Criptomoedas disponíveis
- Cores e temas
- Configurações de cache

## 📈 Roadmap

- [ ] Integração com mais exchanges
- [ ] Sistema de alertas por email/SMS
- [ ] Análise técnica avançada (RSI, MACD)
- [ ] Portfolio tracking
- [ ] Modo escuro/claro
- [ ] Export de dados (CSV, PDF)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [CoinGecko](https://coingecko.com) pela API gratuita
- [Streamlit](https://streamlit.io) pelo framework incrível
- [Plotly](https://plotly.com) pelas visualizações interativas

---

**Desenvolvido com ❤️ para a comunidade crypto**

⭐ Se este projeto foi útil, considere dar uma estrela!
