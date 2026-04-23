import os


def _get_streamlit_secret(name: str) -> str | None:
    try:
        import streamlit as st

        return st.secrets.get(name)
    except Exception:
        return None


def get_massive_api_key() -> str | None:
    for key_name in ("MASSIVE_API_KEY", "POLYGON_API_KEY"):
        api_key = os.getenv(key_name) or _get_streamlit_secret(key_name)
        if api_key:
            return api_key
    return None
