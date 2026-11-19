-- デモデータ投入（リセット兼用）
-- 前提: schema.sql 実行済み。何度流しても同じ状態に戻る。

-- 子テーブルから親テーブルまでまとめて空にし、採番(id)も1に戻す
TRUNCATE TABLE stock_movements, items, suppliers RESTART IDENTITY;

-- 仕入れ先
INSERT INTO suppliers (name) VALUES
    ('文具堂'),
    ('オフィスサプライ東京'),
    ('事務機器センター');

-- 備品（supplier_id は名前で引いてid番号に依存しない）
/* 
    -- 処理説明 --
    1. FROM(VALUES)で手書きのテーブルを作成、エイリアス名とカラム名を記述
    （カラム名を記述しないとsqlが自動でcolumn1と記入する）
    2. JOINでsuppliers.nameと手書きのsupplier_nameを結合
    3. SELECTで必要なカラムを指定（itemテーブルのカラム名と一致させる）
    4. INSERTでitems内のカラムに手書きのデータを挿入
*/
INSERT INTO items (name, supplier_id, reorder_point, order_unit)
SELECT
    v.item_name,
    s.id,
    v.reorder_point,
    v.order_unit
FROM (VALUES
    ('ボールペン(黒)',     '文具堂',               20,  10),
    ('ボールペン(赤)',     '文具堂',               10,  10),
    ('蛍光ペン',           '文具堂',               12,   6),
    ('コピー用紙A4(冊)',   'オフィスサプライ東京', 10,   5),
    ('ホッチキス針',       'オフィスサプライ東京', 10,  10),
    ('クリアファイル',     'オフィスサプライ東京', 50, 100),
    ('コピー機トナー',     '事務機器センター',      2,   1),
    ('乾電池(単3)',        '事務機器センター',      8,   4),
    ('シュレッダーオイル', '事務機器センター',      1,   1)
) AS v(item_name, supplier_name, reorder_point, order_unit) 
JOIN suppliers AS s ON s.name = v.supplier_name;

-- 入出庫履歴（入庫は＋、出庫は−）
/* 
    -- 処理説明 --
    1. FROM(VALUES)で手書きのテーブルを作成、エイリアス名とカラム名を記述
    （カラム名を記述しないとsqlが自動でcolumn1と記入する）
    2. JOINでitem.nameと手書きのitem_nameを結合
    3. SELECTで必要なカラムを指定（itemテーブルのカラム名と一致させる）
    4. v.movement_dateをDATE型に変換（VALUES内の日付部分は文字列として判定されるため）
    5. INSERTでitems内のカラムに手書きのデータを挿入
*/
INSERT INTO stock_movements (item_id, movement_date, quantity)
SELECT 
    i.id,
    v.movement_date::date,
    v.quantity
FROM (VALUES
    ('ボールペン(黒)',     '2026-10-01',  50),
    ('ボールペン(黒)',     '2026-10-15', -20),
    ('ボールペン(黒)',     '2026-11-05', -15),
    ('ボールペン(赤)',     '2026-10-01',  30),
    ('ボールペン(赤)',     '2026-10-20',  -5),
    ('蛍光ペン',           '2026-10-01',  24),
    ('蛍光ペン',           '2026-11-02', -14),
    ('コピー用紙A4(冊)',   '2026-10-01',  30),
    ('コピー用紙A4(冊)',   '2026-10-18', -12),
    ('コピー用紙A4(冊)',   '2026-11-08', -10),
    ('ホッチキス針',       '2026-10-01',  40),
    ('ホッチキス針',       '2026-10-25', -10),
    ('クリアファイル',     '2026-10-01', 200),
    ('クリアファイル',     '2026-11-10', -140),
    ('コピー機トナー',     '2026-10-01',   4),
    ('コピー機トナー',     '2026-11-12',  -3),
    ('乾電池(単3)',        '2026-10-01',  12),
    ('乾電池(単3)',        '2026-10-30',  -2)
    -- シュレッダーオイルは履歴なし（在庫0）。LEFT JOIN + COALESCE の確認用
) AS v(item_name, movement_date, quantity)
JOIN items i ON i.name = v.item_name;
