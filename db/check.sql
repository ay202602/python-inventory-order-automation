-- 生データの確認
SELECT * FROM suppliers;
SELECT * FROM items;
SELECT * FROM stock_movements;

-- 1. 在庫一覧（履歴なしの品目も0で出るか）
SELECT
    i.name,
    COALESCE(SUM(m.quantity), 0) AS stock
FROM items AS i
LEFT JOIN stock_movements AS m ON m.item_id = i.id
GROUP BY i.id, i.name
ORDER BY i.id;

-- 2. 発注対象の品目（在庫　<= 発注点）
SELECT
    i.name,
    COALESCE(SUM(m.quantity), 0) AS stock,
    i.reorder_point
FROM items AS i
LEFT JOIN stock_movements AS m ON m.item_id = i.id
GROUP BY i.id, i.name, i.reorder_point
HAVING COALESCE(SUM(m.quantity), 0) <= i.reorder_point;

-- 3. 件数チェック（期待: suppliers=3, items=9, stock_movements=18）
SELECT
    (SELECT COUNT(*) FROM suppliers)       AS suppliers,
    (SELECT COUNT(*) FROM items)           AS items,
    (SELECT COUNT(*) FROM stock_movements) AS movements;
