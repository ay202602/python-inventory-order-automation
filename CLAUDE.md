## プロジェクト概要
オフィス備品の在庫を管理し、発注点を下回った品目の発注書をExcelで自動作成するStreamlitアプリ。方針は「小さく作り切る」。凝った機能より、エラー処理・読みやすさ・README の完成度を優先する。利用者は総務担当1人のみ（ユーザー管理・同時更新は考えない）。

## 技術
- Python / pandas / Streamlit / PostgreSQL（Neon）/ **psycopg 3**（`psycopg`。psycopg2 は使わない）/ openpyxl / pytest。
- 公開先は Streamlit Community Cloud。

## コマンド
Windows + `.venv`（Git管理外）を使う。

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run streamlit_app.py    
pytest                            # 単体: pytest tests/test_xxx.py::test_name
```

## アーキテクチャ（計画）
画面3つ: ①入出庫登録 ②在庫一覧＋不足一覧 ③発注書出力。  

**依存は一方向**: `ui` → `stock`・`orders` → `db`。`db` が `orders` を呼ばない、`stock` に Streamlit のコードを書かない。
- `ui/` 画面表示と入力のみ / `db/` 接続とSQL / `stock/` 不足判定・pandas整形 / `orders/` 発注数量計算とExcel作成 / `config.py` 設定読み込み
- 最初は `db.py` `stock.py` `orders.py` の1ファイルずつで始め、長くなったらフォルダ化する。フォルダ化する場合はルート直下に置き、各フォルダに空の `__init__.py`、import はルート基準（`from orders.xxx import ...`）。
- SQLで集計できることはSQL、複雑な加工はPython。判断が分かれたらREADMEの設計意図に理由を書く。

**DB（3テーブル）**: `suppliers`(id, 名前) / `items`(id, 名前, supplier_id, 発注点, 発注単位) / `stock_movements`(id, item_id, 日付, 数量)。
- 現在庫は列に持たず `stock_movements` の SUM で計算（入庫は＋、出庫は−）。
- 1備品につき発注先は1社固定。在庫は常に最小単位（本）で管理し、発注数量 = 不足数を発注単位で切り上げ。
- 発注状態管理・発注残・一括取込・グラフ・複数発注先は**作らない**。「発注書を出しても入荷登録までは不足一覧に残り続ける」はREADMEの「既知の制限」に明記する。

## 実装上の決まり
- SQLは必ずパラメータ化（プレースホルダ使用、文字列連結しない）。
- Neonは無料枠で計算資源が停止するため、接続は使い回さず処理ごとに `with psycopg.connect(...)` で開く（`st.cache_resource` で接続を保持しない）。接続文字列は `st.secrets` で管理し、コミットしない。
- クラウド上ではファイル保存してもユーザーに届かない。Excelは `BytesIO` でメモリ上に作り `st.download_button` で渡す。雛形Excelを1枚固定で `load_workbook` し、セルに値を書き込む。
- Streamlitは操作ごとにスクリプト全体が再実行される。状態保持は `st.session_state`。
- 公開アプリは誰でも書き込めるため、デモデータのリセット手段を用意する。
- 余力があれば後半で: 在庫マイナス防止のCHECK制約、トランザクション、logging、エラーハンドリング、テスト。
- Pylance(standard)に沿ったコーディング。

## 開発フェーズ
- Phase 1: ①config+db接続 → ②db現在庫SQL+stock不足判定 → ③画面②在庫一覧＋不足一覧 → ④画面①入出庫登録 → ⑤デモデータリセット → 公開
- Phase 2: orders発注数量計算（切り上げ）→ Excel作成（発注先ごと）→ 画面③発注書出力
- Phase 3: logging・エラー処理・テスト・README（ER図はmermaidで可）。

## Git運用
GitHub Flow + Conventional Commits。`main` は常に動く状態に保ち、機能ごとにブランチを切ってPR経由でマージする。Claude Codeが編集した変更はコミットメッセージの最後尾に`Co-Authored-By: Claude`の文言を足す。

## ドキュメント
READMEの章立て: 概要 / 機能 / 出力例 / 実行方法 / 動作環境・使用技術 / 設計意図 / ディレクトリ構成。「設計意図」には画面とロジックを分けて発注数量計算を単体テストしやすくした点を書く。
