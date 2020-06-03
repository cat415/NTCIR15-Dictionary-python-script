# NTCIR15-Dictionary-python-script
NTCIR15-Stance-classification-task用の「議員/所属会派辞書」とその作成に使ったプログラム

## プログラム概要
議員の発言などを利用してその議員の属する会派の議題に対しての[賛否を予測するタスク](https://github.com/cat415/NTCIR15-rulebase-python-script)用に作成した「議員/所属会派辞書」
[東京都議会HP](https://search.metro.tokyo.lg.jp/?kw=&temp=JP&ie=u&sitesearch=www.gikai.metro.tokyo.jp)の検索エンジンに議員名を与え, その議員が所属する政党名を抽出する.

## 辞書について
議員の政党変えを考慮したネスト構造の辞書となっています.
```
---構造例---

	"中屋文孝": {
		"自民党": [
			2002,
			2009,
			2011,
			2012,
			2014,
			2016
		]
	},
	"たきぐち学": {
		"民主党": [
			2010,
			2011
		],
		"都ファースト": [
			2018
		]
	},
 ```

## 内容
- NTCIR15-makedic.py
  - 辞書作成用プログラム

- NTCIR15Util.py
  - 使った関数など

- PoliInfo2-StanceClassification-JA-Dry-Dictionary-v**.json
  - NTCIR15-makedic.pyを利用して作成した議員/所属会派
  
- PoliInfo2-StanceClassification-JA-Dry-Test-v20200522.json
  - 議事録jsonファイル

- README.md
  - 説明書MDファイル
  
## 必要ライブラリ
自分の実行環境に合わせて適切にインストールしてください.
- bs4(BeautifulSoup4)
- requests-html
- jeraconv
- retry

## 実行
json dumpは未実装.
```
python NTCIR15-makedic.py
```

## 現状の問題点, 不具合等
- 検索エンジンからPDFファイルが返されることがあり, ファイル内容の抽出は未実装.
- 議員の政党変えについて, 現時点では詳細な年月日までを収録していないため, 同じ年に2つ以上の会派に所属している議員が存在することがある.
