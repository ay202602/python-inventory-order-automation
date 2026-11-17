# DB接続。接続は使い回さず、呼び出し側が処理ごとに `with` で開閉する。

import psycopg

from config import get_database_url

CONNECT_TIMEOUT_SEC = (
    10  # Neon の無料枠は停止状態からの起動に時間がかかるため余裕を持たせる
)


def get_connection() -> psycopg.Connection:
    """新しい接続を返す。`with get_connection() as conn:` で使うこと。"""
    return psycopg.connect(get_database_url(), connect_timeout=CONNECT_TIMEOUT_SEC)


def fetch_items_count() -> int:
    """items テーブルの件数を返す（接続確認用）。"""
    # ブロックを抜けると接続を閉じる
    with get_connection() as conn:
        row = conn.execute("SELECT COUNT(*) FROM items").fetchone() # 1行をタプルで返す（このクエリ内容は必ず1行になるため）
    return int(row[0]) if row else 0 # if文はPylanceの型チェック対策
