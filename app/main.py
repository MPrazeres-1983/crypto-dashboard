import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List

# Configuração da página
st.set_page_config(
    page_title="CryptoDash - Real-Time Analytics",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache para dados
@st.cache_data(ttl=60)  # Cache por 60 segundos
def fetch_crypto_data(symbols: List[str]) -> Dict:
    """Fetch cryptocurrency data from CoinGecko API"""
    try:
        # Converter símbolos para IDs do CoinGecko
        symbol_to_id = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum', 
            'ADA': 'cardano',
            'DOT': 'polkadot',
            'SOL': 'solana'
        }

        ids = [symbol_to_id.get(symbol, symbol.lower()) for symbol in symbols]
        ids_str = ','.join(ids)

        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': ids_str,
            'vs_currencies': 'usd',
            'include_24hr_change': 'true',
            'include_market_cap': 'true',
            'include_24hr_vol': 'true'
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Converter para formato esperado
        result = {}
        for symbol, coin_id in zip(symbols, ids):
            if coin_id in data:
                coin_data = data[coin_id]
                result[symbol] = {
                    'price': coin_data.get('usd', 0),
                    'change_24h': coin_data.get('usd_24h_change', 0),
                    'market_cap': coin_data.get('usd_market_cap', 0),
                    'volume_24h': coin_data.get('usd_24h_vol', 0)
                }

        return result

    except (requests.RequestException, ValueError, KeyError, TypeError) as exc:
        st.error(f"Não foi possível obter dados reais da CoinGecko: {exc}")
        # Nunca apresentar preços fictícios como se fossem dados de mercado.
        return {}

def create_price_chart(data: Dict) -> go.Figure:
    """Criar gráfico de preços"""
    symbols = list(data.keys())
    prices = [data[symbol]['price'] for symbol in symbols]
    changes = [data[symbol]['change_24h'] for symbol in symbols]

    colors = ['green' if change >= 0 else 'red' for change in changes]

    fig = go.Figure(data=[
        go.Bar(
            x=symbols,
            y=prices,
            marker_color=colors,
            text=[f"${price:,.2f}" for price in prices],
            textposition='auto',
        )
    ])

    fig.update_layout(
        title="Preços Atuais das Criptomoedas",
        xaxis_title="Criptomoeda",
        yaxis_title="Preço (USD)",
        template="plotly_dark",
        height=400
    )

    return fig

def create_change_chart(data: Dict) -> go.Figure:
    """Criar gráfico de mudanças 24h"""
    symbols = list(data.keys())
    changes = [data[symbol]['change_24h'] for symbol in symbols]

    colors = ['green' if change >= 0 else 'red' for change in changes]

    fig = go.Figure(data=[
        go.Bar(
            x=symbols,
            y=changes,
            marker_color=colors,
            text=[f"{change:+.2f}%" for change in changes],
            textposition='auto',
        )
    ])

    fig.update_layout(
        title="Mudança de Preço (24h)",
        xaxis_title="Criptomoeda",
        yaxis_title="Mudança (%)",
        template="plotly_dark",
        height=400
    )

    return fig

def display_dashboard(selected_cryptos: List[str]):
    """Exibir dashboard principal"""

    # Buscar dados
    with st.spinner("Carregando dados..."):
        crypto_data = fetch_crypto_data(selected_cryptos)

    if not crypto_data:
        st.warning("Sem dados de mercado válidos. Tente atualizar mais tarde.")
        return

    # Métricas principais
    st.subheader("📊 Métricas Principais")

    cols = st.columns(len(selected_cryptos))
    for i, symbol in enumerate(selected_cryptos):
        if symbol in crypto_data:
            data = crypto_data[symbol]
            with cols[i]:
                st.metric(
                    label=f"{symbol}",
                    value=f"${data['price']:,.2f}",
                    delta=f"{data['change_24h']:+.2f}%"
                )

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        price_chart = create_price_chart(crypto_data)
        st.plotly_chart(price_chart, use_container_width=True, key="price_chart")

    with col2:
        change_chart = create_change_chart(crypto_data)
        st.plotly_chart(change_chart, use_container_width=True, key="change_chart")

    # Tabela detalhada
    st.subheader("📋 Dados Detalhados")

    table_data = []
    for symbol in selected_cryptos:
        if symbol in crypto_data:
            data = crypto_data[symbol]
            table_data.append({
                'Símbolo': symbol,
                'Preço (USD)': f"${data['price']:,.2f}",
                'Mudança 24h (%)': f"{data['change_24h']:+.2f}%",
                'Market Cap': f"${data['market_cap']:,.0f}",
                'Volume 24h': f"${data['volume_24h']:,.0f}"
            })

    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True)

    # Alertas
    st.subheader("🚨 Alertas")
    alert_container = st.container()
    with alert_container:
        for symbol in selected_cryptos:
            if symbol in crypto_data:
                change = crypto_data[symbol]['change_24h']
                if abs(change) > 5:
                    alert_type = "🔥" if change > 0 else "❄️"
                    st.info(f"{alert_type} {symbol}: {change:+.2f}% nas últimas 24h")

    # Footer
    st.markdown("---")
    st.markdown("**Última atualização:** " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    st.markdown("*Dados fornecidos pela CoinGecko API*")

def main():
    # Header
    st.title("🚀 CryptoDash - Real-Time Analytics")
    st.markdown("Dashboard profissional para análise de criptomoedas em tempo real")

    # Sidebar
    st.sidebar.header("⚙️ Configurações")

    # Seleção de criptomoedas
    available_cryptos = ['BTC', 'ETH', 'ADA', 'DOT', 'SOL']
    selected_cryptos = st.sidebar.multiselect(
        "Selecionar Criptomoedas:",
        available_cryptos,
        default=['BTC', 'ETH', 'ADA'],
        key="crypto_selector"
    )

    if not selected_cryptos:
        st.warning("Por favor, selecione pelo menos uma criptomoeda.")
        return

    # Botão de refresh manual
    if st.sidebar.button("🔄 Atualizar Dados", key="refresh_button"):
        st.cache_data.clear()
        st.rerun()

    # Exibir dashboard
    display_dashboard(selected_cryptos)

if __name__ == "__main__":
    main()
