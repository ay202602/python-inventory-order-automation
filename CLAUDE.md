## プロジェクト概要
オフィス備品の在庫を管理し、発注点を下回った品目の発注書をExcelで自動作成するStreamlitアプリ。方針は「小さく作り切る」。凝った機能より、エラー処理・読みやすさ・README の完成度を優先する。利用者は総務担当1人のみ（ユーザー管理・同時更新は考えない）。
画面は3つ: ①入出庫登録 ②在庫一覧＋不足一覧 ③発注書出力。DB仕様・作らない機能・開発フェーズと進捗は `docs/plan.md` を参照。

## 技術
Python / pandas / Streamlit / PostgreSQL（Neon）/ **psycopg 3**（`psycopg`。psycopg2 は使わない）/ openpyxl / pytest。公開先は Streamlit Community Cloud。バージョンは `requirements.txt` が正。

## コマンド
Windows + `.venv`（Git管理外）を使う。

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run streamlit_app.py
pytest                            # 単体: pytest tests/test_xxx.py::test_name
```

## アーキテクチャ
**依存は一方向**: `ui` → `stock`・`orders` → `db`。`db` が `orders` を呼ばない、`stock` に Streamlit のコードを書かない。
- `ui/` 画面表示と入力のみ / `db/` 接続とSQL / `stock/` 不足判定・pandas整形 / `orders/` 発注数量計算とExcel作成 / `config.py` 設定読み込み
- 最初は `db.py` `stock.py` `orders.py` の1ファイルずつで始め、長くなったらフォルダ化する。フォルダ化する場合はルート直下に置き、各フォルダに空の `__init__.py`、import はルート基準（`from orders.xxx import ...`）。

## 実装上の決まり
- SQLは必ずパラメータ化（プレースホルダ使用、文字列連結しない）。
- 接続は使い回さず処理ごとに `with psycopg.connect(...)` で開く（`st.cache_resource` で接続を保持しない。Neon無料枠は計算資源が停止するため）。接続文字列は `st.secrets` で管理し、コミットしない。
- Excelは `BytesIO` でメモリ上に作り `st.download_button` で渡す（ファイル保存はしない）。
- 状態保持は `st.session_state`（操作ごとにスクリプト全体が再実行される）。
- 公開アプリは誰でも書き込めるため、デモデータのリセット手段を用意する。
- 発注状態管理・発注残・一括取込・グラフ・複数発注先は**作らない**。
- Pylance(standard)に沿ったコーディング。

## Git運用
- `main` は常に動く状態に保ち、機能ごとにブランチを切ってPR経由でマージする。
- コミットのスコープはモジュール名（`db` / `stock` / `orders` / `ui` / `config`）を付ける。
- Claude Codeが編集した変更はコミットメッセージの最後尾に`Co-Authored-By: Claude`の文言を足す。
