import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
import time
from datetime import datetime, timedelta
import asyncio
import aiohttp
from typing import Dict, List
import json

# Configuração da página
st.set_page_config(
    page_title="CryptoDash - Real-Time Analytics",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="expanded"
)

class CryptoAPI:
    """Classe para interagir com APIs de criptomoedas"""

    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"

    async def get_crypto_data(self, coins: List[str]) -> Dict:
        """Busca dados de múltiplas criptomoedas"""
        coins_str = ",".join(coins)
        url = f"{self.base_url}/simple/price"
        params = {
            'ids': coins_str,
            'vs_currencies': 'usd',
            'include_24hr_change': 'true',
            'include_market_cap': 'true',
            'include_24hr_vol': 'true'
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params) as response:
                    return await response.json()
            except Exception as e:
                st.error(f"Erro ao buscar dados: {e}")
                return {}

    def get_historical_data(self, coin_id: str, days: int = 7) -> pd.DataFrame:
        """Busca dados históricos de uma criptomoeda"""
        url = f"{self.base_url}/coins/{coin_id}/market_chart"
        params = {'vs_currency': 'usd', 'days': days}

        try:
            response = requests.get(url, params=params)
            data = response.json()

            df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['volume'] = [vol[1] for vol in data['total_volumes']]

            return df
        except Exception as e:
            st.error(f"Erro ao buscar dados históricos: {e}")
            return pd.DataFrame()

def create_price_chart(df: pd.DataFrame, coin_name: str) -> go.Figure:
    """Cria gráfico de preços com volume"""
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=(f'{coin_name} - Preço (USD)', 'Volume'),
        row_width=[0.7, 0.3]
    )

    # Gráfico de preços
    fig.add_trace(
        go.Scatter(
            x=df['timestamp'],
            y=df['price'],
            mode='lines',
            name='Preço',
            line=dict(color='#00D4AA', width=2)
        ),
        row=1, col=1
    )

    # Gráfico de volume
    fig.add_trace(
        go.Bar(
            x=df['timestamp'],
            y=df['volume'],
            name='Volume',
            marker_color='rgba(0, 212, 170, 0.3)'
        ),
        row=2, col=1
    )

    fig.update_layout(
        title=f"Análise de {coin_name}",
        xaxis_title="Tempo",
        yaxis_title="Preço (USD)",
        template="plotly_dark",
        height=500,
        showlegend=False
    )

    return fig

def create_portfolio_chart(crypto_data: Dict) -> go.Figure:
    """Cria gráfico de distribuição do portfólio"""
    coins = list(crypto_data.keys())
    market_caps = [crypto_data[coin].get('usd_market_cap', 0) for coin in coins]

    fig = go.Figure(data=[
        go.Pie(
            labels=[coin.replace('-', ' ').title() for coin in coins],
            values=market_caps,
            hole=0.4,
            marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        )
    ])

    fig.update_layout(
        title="Distribuição por Market Cap",
        template="plotly_dark",
        height=400
    )

    return fig

def format_currency(value: float) -> str:
    """Formata valores monetários"""
    if value >= 1e9:
        return f"${value/1e9:.2f}B"
    elif value >= 1e6:
        return f"${value/1e6:.2f}M"
    elif value >= 1e3:
        return f"${value/1e3:.2f}K"
    else:
        return f"${value:.2f}"

def main():
    # Título principal
    st.title("₿ CryptoDash - Real-Time Analytics")
    st.markdown("---")

    # Sidebar para configurações
    st.sidebar.header("⚙️ Configurações")

    # Seleção de criptomoedas
    available_coins = {
        'Bitcoin': 'bitcoin',
        'Ethereum': 'ethereum',
        'Cardano': 'cardano',
        'Polkadot': 'polkadot',
        'Chainlink': 'chainlink'
    }

    selected_coins = st.sidebar.multiselect(
        "Selecione as criptomoedas:",
        options=list(available_coins.keys()),
        default=['Bitcoin', 'Ethereum', 'Cardano']
    )

    # Período para dados históricos
    period = st.sidebar.selectbox(
        "Período histórico:",
        options=[1, 7, 30, 90],
        index=1,
        format_func=lambda x: f"{x} dia{'s' if x > 1 else ''}"
    )

    # Auto-refresh
    auto_refresh = st.sidebar.checkbox("Auto-refresh (30s)", value=True)

    if auto_refresh:
        time.sleep(30)
        st.rerun()

    # Buscar dados das criptomoedas selecionadas
    if selected_coins:
        coin_ids = [available_coins[coin] for coin in selected_coins]

        # Placeholder para loading
        with st.spinner('Carregando dados...'):
            crypto_api = CryptoAPI()

            # Buscar dados atuais
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            crypto_data = loop.run_until_complete(crypto_api.get_crypto_data(coin_ids))
            loop.close()

        if crypto_data:
            # Métricas principais
            st.header("📊 Visão Geral")

            cols = st.columns(len(selected_coins))

            for i, coin in enumerate(selected_coins):
                coin_id = available_coins[coin]
                data = crypto_data.get(coin_id, {})

                with cols[i]:
                    price = data.get('usd', 0)
                    change_24h = data.get('usd_24h_change', 0)

                    # Cor baseada na variação
                    color = "green" if change_24h >= 0 else "red"
                    arrow = "↗️" if change_24h >= 0 else "↘️"

                    st.metric(
                        label=f"{arrow} {coin}",
                        value=f"${price:,.2f}",
                        delta=f"{change_24h:.2f}%"
                    )

            # Gráficos
            st.header("📈 Análise Técnica")

            # Tabs para diferentes visualizações
            tab1, tab2, tab3 = st.tabs(["Preços Históricos", "Distribuição", "Comparação"])

            with tab1:
                # Seletor de moeda para gráfico detalhado
                selected_coin_detail = st.selectbox(
                    "Selecione uma criptomoeda para análise detalhada:",
                    options=selected_coins
                )

                coin_id_detail = available_coins[selected_coin_detail]
                historical_data = crypto_api.get_historical_data(coin_id_detail, period)

                if not historical_data.empty:
                    fig = create_price_chart(historical_data, selected_coin_detail)
                    st.plotly_chart(fig, use_container_width=True)

            with tab2:
                # Gráfico de pizza com market cap
                if len(crypto_data) > 1:
                    fig_pie = create_portfolio_chart(crypto_data)
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("Selecione mais de uma criptomoeda para ver a distribuição")

            with tab3:
                # Comparação de preços
                comparison_data = []
                for coin in selected_coins:
                    coin_id = available_coins[coin]
                    data = crypto_data.get(coin_id, {})
                    comparison_data.append({
                        'Moeda': coin,
                        'Preço (USD)': data.get('usd', 0),
                        'Variação 24h (%)': data.get('usd_24h_change', 0),
                        'Market Cap': format_currency(data.get('usd_market_cap', 0)),
                        'Volume 24h': format_currency(data.get('usd_24h_vol', 0))
                    })

                df_comparison = pd.DataFrame(comparison_data)

                # Gráfico de barras para comparação
                fig_bar = px.bar(
                    df_comparison,
                    x='Moeda',
                    y='Preço (USD)',
                    color='Variação 24h (%)',
                    color_continuous_scale='RdYlGn',
                    title="Comparação de Preços"
                )
                fig_bar.update_layout(template="plotly_dark")
                st.plotly_chart(fig_bar, use_container_width=True)

                # Tabela detalhada
                st.subheader("Dados Detalhados")
                st.dataframe(df_comparison, use_container_width=True)

            # Alertas e insights
            st.header("🚨 Alertas e Insights")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Maiores Altas")
                gainers = [(coin, crypto_data[available_coins[coin]].get('usd_24h_change', 0)) 
                          for coin in selected_coins]
                gainers.sort(key=lambda x: x[1], reverse=True)

                for coin, change in gainers[:3]:
                    if change > 0:
                        st.success(f"🚀 {coin}: +{change:.2f}%")

            with col2:
                st.subheader("Maiores Baixas")
                losers = [(coin, crypto_data[available_coins[coin]].get('usd_24h_change', 0)) 
                         for coin in selected_coins]
                losers.sort(key=lambda x: x[1])

                for coin, change in losers[:3]:
                    if change < 0:
                        st.error(f"📉 {coin}: {change:.2f}%")

        else:
            st.error("Não foi possível carregar os dados. Tente novamente.")

    else:
        st.info("Selecione pelo menos uma criptomoeda na barra lateral para começar.")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>🔄 Dados atualizados em tempo real via CoinGecko API</p>
            <p>Desenvolvido com ❤️ usando Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
