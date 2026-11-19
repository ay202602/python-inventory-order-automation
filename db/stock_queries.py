from typing import Any

from psycopg.rows import dict_row

from db.connection import get_connection

# 在庫に関するSQL。現在庫は列に持たず stock_movements の SUM で計算する。
# 履歴が0件の備品も在庫0で出すため LEFT JOIN + COALESCE を使う
# current_stock はPythonのintとして扱いやすくするためint型に変換
CURRENT_STOCK_SQL = """
SELECT
    i.id                              AS item_id,
    i.name                            AS item_name,
    s.name                            AS supplier_name,
    i.reorder_point                   AS reorder_point,
    i.order_unit                      AS order_unit,
    COALESCE(SUM(m.quantity), 0)::int AS current_stock
FROM items AS i
INNER JOIN suppliers AS s ON s.id = i.supplier_id
LEFT JOIN stock_movements AS m ON m.item_id = i.id
GROUP BY i.id, i.name, s.name, i.reorder_point, i.order_unit
ORDER BY i.id ASC
"""


def fetch_current_stock() -> (
    list[dict[str, Any]]
):  # dict[DB列名, なんでも入る型（上記のクエリはintとstrが混在しているため）]
    """全備品の現在庫を1備品1行で返す（キーは SQL の別名と同じ）。"""
    with get_connection() as conn:
        with conn.cursor(
            row_factory=dict_row
        ) as cur:  # pandasに渡しやすくするため取り出した1行をdictとして変換
            cur.execute(CURRENT_STOCK_SQL)
            return cur.fetchall()
