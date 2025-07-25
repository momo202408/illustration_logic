# Nonogram Solver (イラストロジックソルバー)

## 概要

このプロジェクトは、**ノノグラム**（イラストロジックやお絵かきロジックとも呼ばれる）パズルを解くためのPythonスクリプトです。
行と列のヒント数字を頼りに、ロジックのみを使用して盤面を塗りつぶし、隠されたイラストを明らかにします。

## 主な機能

- **ロジックベースの解法**:
  - 各行・各列について、ヒントに合致する可能性のあるすべてのパターンを生成します。
  - 現在の盤面の状態と矛盾しないパターンに絞り込みます。
  - すべての有効なパターンで共通して塗りつぶされる（または空白になる）マスを特定し、盤面を確定させます。
  - このプロセスを、盤面に変化がなくなるまで繰り返すことで解を導きます。

- **盤面の可視化**:
  - 現在の盤面の状態を、ヒント数字と共にコンソール上に分かりやすく表示します。
    - 塗りつぶしマス: `■`
    - 空白マス: `.`
    - 未確定マス: `?`

## 使い方

1.  `solver.py` ファイルを開きます。
2.  ファイル末尾の `if __name__ == '__main__':` ブロック内にある `row_hints` と `col_hints` の値を、解きたいパズルのヒントに書き換えます。
3.  ターミナルで以下のコマンドを実行します。

    ```bash
    python solver.py
    ```

4.  初期盤面と、解答が完了した最終的な盤面が出力されます。

## 免責事項

このプロジェクトはAIアシスタント「OpenHands」の支援を受けて作成されました。そのため、動作を完全に保証するものではありません。
