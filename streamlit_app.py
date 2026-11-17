import psycopg
import streamlit as st

from db.connection import fetch_items_count

st.title("備品在庫・発注書自動作成")

# 仮の接続確認（画面実装時に置き換える）
try:
    count = fetch_items_count()
except RuntimeError as e:
    st.error(str(e))
except psycopg.Error:
    # 接続文字列を含み得るため、例外の詳細は表示しない
    st.error("DBに接続できませんでした。接続文字列とNeonの状態を確認してください。")
else:
    st.success(f"DB接続OK: items {count} 件")
