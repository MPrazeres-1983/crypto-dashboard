"""
Configurações do CryptoDash
"""

# APIs
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

# Configurações de cache
CACHE_DURATION = 60  # segundos

# Criptomoedas disponíveis
AVAILABLE_CRYPTOCURRENCIES = {
    'bitcoin': 'Bitcoin',
    'ethereum': 'Ethereum',
    'cardano': 'Cardano',
    'polkadot': 'Polkadot',
    'chainlink': 'Chainlink',
    'solana': 'Solana',
    'avalanche-2': 'Avalanche',
    'polygon': 'Polygon'
}

# Configurações de visualização
CHART_COLORS = {
    'primary': '#00D4AA',
    'secondary': '#FF6B6B',
    'success': '#4ECDC4',
    'warning': '#FFEAA7',
    'danger': '#FF7675'
}
