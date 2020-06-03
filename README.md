# NTCIR15-Dictionary-python-script
NTCIR15-Stance-classification-task用の「議員/所属会派辞書」とその作成に使ったプログラム

## プログラム概要
議員の発言などを利用してその議員の属する会派の議題に対しての[賛否を予測するタスク](https://github.com/cat415/NTCIR15-rulebase-python-script)用に作成した「議員/所属会派辞書」
[東京都議会HP](https://search.metro.tokyo.lg.jp/?kw=&temp=JP&ie=u&sitesearch=www.gikai.metro.tokyo.jp)の検索エンジンに議員名を与え, その議員が所属する政党名を抽出する.

## 内容
自分の実行環境に合わせて適切にインストールしてください.
- NTCIR15-makedic.py
  - 辞書作成用プログラム

- NTCIR15Util.py
  - 使った関数など

- PoliInfo2-StanceClassification-JA-Dry-Dictionary-v**.json
  - NTCIR15-makedic.pyで作成した辞書
  
- PoliInfo2-StanceClassification-JA-Dry-Test-v20200522.json
  - 議事録jsonファイル

- README.md
  - 説明書MDファイル
  
## 必要ライブラリ

- bs4(BeautifulSoup4)
- requests-html
- jeraconv
- retry
