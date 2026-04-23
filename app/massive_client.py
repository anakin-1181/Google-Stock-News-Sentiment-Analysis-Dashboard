from collections.abc import Mapping

import requests

from .config import get_massive_api_key


class MassiveClient:
    BASE_URL = "https://api.massive.com"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or get_massive_api_key()
        if not self.api_key:
            raise ValueError(
                "Set MASSIVE_API_KEY in your environment or Streamlit secrets to fetch stock data."
            )

    def _request_json(self, path: str, params: Mapping[str, object] | None = None) -> dict:
        request_params = dict(params or {})
        request_params["apiKey"] = self.api_key

        response = requests.get(f"{self.BASE_URL}{path}", params=request_params, timeout=15)
        try:
            payload = response.json()
        except ValueError:
            payload = None

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            if isinstance(payload, dict):
                message = payload.get("error") or payload.get("message") or payload.get("status")
                if message:
                    raise ValueError(str(message)) from exc
            raise

        if not isinstance(payload, dict):
            raise ValueError("Massive returned a non-JSON response.")

        error_message = payload.get("error") or payload.get("message")
        if error_message:
            raise ValueError(str(error_message))

        return payload

    def lookup_stock_ticker(self, ticker: str) -> dict | None:
        payload = self._request_json(
            "/v3/reference/tickers",
            params={
                "ticker": ticker,
                "market": "stocks",
                "active": "true",
                "limit": 10,
            },
        )
        results = payload.get("results") or []
        if not results:
            return None

        ticker_upper = ticker.upper()
        exact_match = next(
            (item for item in results if str(item.get("ticker", "")).upper() == ticker_upper),
            results[0],
        )
        return exact_match

    def get_daily_bars(self, ticker: str, start_date: str, end_date: str) -> list[dict]:
        payload = self._request_json(
            f"/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}",
            params={
                "adjusted": "true",
                "sort": "asc",
                "limit": 5000,
            },
        )
        return payload.get("results") or []
