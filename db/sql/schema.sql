/* 
    再実行できるようにする（子 → 親の順で削除）
    注意：共有DBで実行すると全データが消えるため実行後はseed.sqlを流す
*/
DROP TABLE IF EXISTS stock_movements;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS suppliers;

-- 仕入れ先テーブル（親）
CREATE TABLE suppliers (
    id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- 備品テーブル（suppliersテーブルの子）
CREATE TABLE items (
    id              INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,
    supplier_id     INTEGER NOT NULL REFERENCES suppliers(id),
    reorder_point   INTEGER NOT NULL CHECK (reorder_point >= 0),
    order_unit      INTEGER NOT NULL CHECK (order_unit > 0)
);

-- 出入庫履歴テーブル（itemテーブルの子）
CREATE TABLE stock_movements (
    id              INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    item_id         INTEGER NOT NULL REFERENCES items(id),
    movement_date   DATE NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Tokyo')::date,
    quantity        INTEGER NOT NULL CHECK (quantity <> 0)
);

