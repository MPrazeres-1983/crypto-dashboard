import pytest
import asyncio
from app.main import CryptoAPI

class TestCryptoAPI:
    def setup_method(self):
        self.api = CryptoAPI()

    @pytest.mark.asyncio
    async def test_get_crypto_data(self):
        """Testa a busca de dados de criptomoedas"""
        coins = ['bitcoin', 'ethereum']
        data = await self.api.get_crypto_data(coins)

        assert isinstance(data, dict)
        assert 'bitcoin' in data or 'ethereum' in data

    def test_get_historical_data(self):
        """Testa a busca de dados históricos"""
        df = self.api.get_historical_data('bitcoin', days=1)

        if not df.empty:
            assert 'timestamp' in df.columns
            assert 'price' in df.columns
            assert len(df) > 0
