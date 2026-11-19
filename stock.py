# 在庫の整形と不足判定。Streamlit・DB には依存しない純粋関数だけを置く（単体テストしやすくするため）。

from typing import Any

import pandas as pd

STOCK_COLUMNS = [
    "item_id",
    "item_name",
    "supplier_name",
    "reorder_point",
    "order_unit",
    "current_stock",
]


def to_stock_df(rows: list[dict[str, Any]]) -> pd.DataFrame:
    """DBの行（dictのリスト）を在庫一覧のDataFrameにする。0件でも列は保つ。"""
    return pd.DataFrame(data=rows, columns=STOCK_COLUMNS)


def extract_shortage(stock_df: pd.DataFrame) -> pd.DataFrame:
    """現在庫が発注点以下の行を抽出し、不足数 shortage（発注点 - 現在庫）列を付ける。
    在庫 == 発注点のとき shortage は 0 になる（発注数量の扱いは Phase 2 で決める）。
    
    ---手順---
    1. 現在庫 <= 発注点 のみ一致しているdfを取り出し、copy()で元のdfから切り離す（次の列追加でpandasの警告が表示される可能性があるため）
    2. 不足数を示す新規の列「shortage」を追加する。内容は在庫不足数（発注点 - 現在庫）を表示する列
    3. reset_index(drop=True) で古い番号を0,1に振り直す
    """
    shortage_df = stock_df[stock_df["current_stock"] <= stock_df["reorder_point"]].copy()
    shortage_df["shortage"] = shortage_df["reorder_point"] - shortage_df["current_stock"]
    return shortage_df.reset_index(drop=True)
