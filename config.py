# 設定の読み込み。接続文字列は st.secrets から取得する。

import streamlit as st


def get_database_url() -> str:
    """DB接続文字列を返す。未設定の場合は日本語メッセージの RuntimeError を送出する。

    例外メッセージには接続文字列（パスワードを含む）を含めない。
    """
    try:
        url = st.secrets["database"]["url"]
    except (KeyError, FileNotFoundError):
        raise RuntimeError(
            "DB接続文字列が設定されていません。"
            ".streamlit/secrets.toml の [database] に url を設定してください"
            "（見本: .streamlit/secrets.toml.example）。"
        ) from None

    if not isinstance(url, str) or not url.strip():
        raise RuntimeError(
            "DB接続文字列が空です。.streamlit/secrets.toml の [database] url を確認してください。"
        )
    return url
