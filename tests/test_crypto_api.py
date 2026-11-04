"""Deterministic CoinGecko integration contract tests (no external calls)."""
from unittest.mock import Mock, patch
import requests
from app.main import fetch_crypto_data, create_price_chart, create_change_chart


def test_fetch_crypto_data_success():
    response = Mock()
    response.json.return_value = {
        "bitcoin": {"usd": 60000, "usd_24h_change": 2.5,
                    "usd_market_cap": 1000000, "usd_24h_vol": 5000},
        "ethereum": {"usd": 3000, "usd_24h_change": -1.0,
                     "usd_market_cap": 500000, "usd_24h_vol": 1000},
    }
    with patch("app.main.requests.get", return_value=response) as get:
        fetch_crypto_data.clear()
        result = fetch_crypto_data(["BTC", "ETH"])
    assert result["BTC"]["price"] == 60000
    assert result["ETH"]["change_24h"] == -1.0
    assert get.call_args.kwargs["timeout"] == 10
    assert "bitcoin" in get.call_args.kwargs["params"]["ids"]
    assert len(create_price_chart(result).data) == 1
    assert len(create_change_chart(result).data) == 1


def test_api_error_does_not_fabricate_market_prices():
    with patch("app.main.requests.get", side_effect=requests.Timeout), \
         patch("app.main.st.error"):
        fetch_crypto_data.clear()
        assert fetch_crypto_data(["BTC"]) == {}


def test_partial_response_only_includes_returned_assets():
    response = Mock()
    response.json.return_value = {"bitcoin": {"usd": 100}}
    with patch("app.main.requests.get", return_value=response):
        fetch_crypto_data.clear()
        result = fetch_crypto_data(["BTC", "ETH"])
    assert list(result) == ["BTC"]
