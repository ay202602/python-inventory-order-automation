from stock import to_stock_df, extract_shortage
# to_stock_df(rows: list[dict[str, Any]]) -> pd.DataFrame
# extract_shortage(stock_df: pd.DataFrame) -> pd.DataFrame

def _row(item_id: int, current_stock: int, reorder_point: int = 10) -> dict:
    return {
        "item_id": item_id,
        "item_name": "item_name",
        "supplier_name": "supplier",
        "reorder_point": reorder_point, # 発注点は規定で10とする
        "order_unit": 10,
        "current_stock": current_stock,
    }


def test_no_shortage_when_stock_above_reorder_point():
    """在庫が発注点より多ければ不足対象にならない"""
    df = to_stock_df([_row(item_id=1, current_stock=11)])
    
    # 不足対象が0件（空のDataFrame）であること
    assert extract_shortage(df).empty


def test_shortage_zero_when_stock_equals_reorder_point():
    """在庫数 = 発注点は対象で、不足数は0になる（境界値）"""
    result = extract_shortage(to_stock_df([_row(item_id=1, current_stock=10)]))
    
    # 境界の品目(id=1)が抽出されること
    assert result["item_id"].tolist() == [1]
    
    # 不足数が0であること
    assert result["shortage"].tolist() == [0]


def test_shortage_quantity_when_stock_below_reorder_point():
    """在庫が発注点未満なら「発注点 - 現在庫」を不足数にする"""
    result = extract_shortage(to_stock_df([_row(item_id=1, current_stock=9), _row(item_id=2, current_stock=0)]))
    
    # 不足数が 10-9=1、10-0=10 であること
    assert result["shortage"].tolist() == [1, 10]


def test_extract_only_items_at_or_below_reorder_point():
    """発注点以下の品目だけが抽出される。"""
    result = extract_shortage(to_stock_df([_row(item_id=1, current_stock=50), _row(item_id=2, current_stock=3), _row(item_id=3, current_stock=10)]))
    
    # 在庫50の品目が除外され、在庫3・10が残ること
    assert result["item_id"].tolist() == [2, 3]


def test_empty_input_keeps_columns():
    """入力が空でも shortage 列を含む空のDataFrameを返す"""
    result = extract_shortage(to_stock_df([]))
    
    # 結果が0件であること
    assert result.empty
    
    # shortage列が存在すること
    assert "shortage" in result.columns
