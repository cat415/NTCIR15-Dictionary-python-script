import re
import json
import bs4
import urllib.request
from makedicUtil import kansuji2arabic, get_title_text
from collections import defaultdict
from requests_html import HTMLSession
from jeraconv import jeraconv
from urllib.parse import urlparse
from retry import retry

# 和暦西暦変換用
j2w = jeraconv.J2W()

# 発言での宣言と、実際の議事録だよりの略称対応辞書
PARTY_DIC = {
    "自民党": ["都議会自由民主党","自民党"],
    "民主党": ["都議会民主党"],
    "公明党": ["都議会公明党"],
    "ネット": ["生活者ネットワーク"],
    "ネット・み": ["生活者ネットワーク・みらい"],
    "無（1/2の会）": ["1/2の会"],
    "無（行革110番）": ["行革110番"],
    "無（自治市民）": ["自治市民"],
    "日本共産党": ["日本共産党"],
    "無（市民の党）": ["市民の党"],
    "都ファースト": ["都民ファースト"],
    "民進党": ["民進党"],
    "立憲・民主": ["立憲民主党・民主クラブ"],
    "民進・立憲": ["民進党・立憲民主党"],
    "東京改革": ["東京改革"],
    "東京みらい": ["東京みらい"],
    "かがやけ": ["かがやけ"],
    "維新・あた": ["維新・あたらしい"],
    "みんな": ["みんなの党Tokyo"],
    "みんなの党": ["都議会会派みんなの党"],
    "維新の党": ["維新の党"],
    "日本維新": ["日本維新"],
    "無（維新の会）": ["維新の会"],
    "結いと維新": ["結いと維新"],
    #一部略称不明な政党
    "無（無所属の会）": ["無所属の会"],
    "無（平成維新）": ["無（平成維新）"],
    "無（フォーラム）": ["無（フォーラム）"],
    "無（東京幸志会）": ["無（東京幸志会）"],
    "無（緑の地球ク）": ["無（緑の地球ク）"],
    "無（深呼吸東京）": ["無（深呼吸東京）"],
    "無（新風自民党）": ["無（新風自民党）"],
    "無（みんな改革）": ["無（みんな改革）"],
    "東京維新": ["東京維新"]
}

# 役職削除リスト(議員に関連する役職or議題通達時の頭語)
POST = [
        "委員長","第一位","第二位","第三位","辞任","へ",
        "兼務","部長","局長","知事","総監","室長","選任","理事","次長","場長","会事","本部",
        ]

# 議員名と所属政党ペアの辞書
POLI_DIC = {}

# 議員名リストを作成
json_open = open('PoliInfo2-StanceClassification-JA-Dry-Test-v20200522.json', 'r')
json_load = json.load(json_open)
SpeakerList = []

# SpeakerListの議員を追加
for i in range(len(json_load)):
    for key in json_load[i]["SpeakerList"].keys():
        """
        議員は9字未満の姓名であると仮定
        SpeakerListには「オリンピック・パラリンピック招致特別委員会の中間報告」等が含まれるため
        """
        if len(key) < 9:
            SpeakerList.append(key)


json_open = open('utterances_tokyo_proceeding_withURL.json', 'r')
json_load = json.load(json_open)

Proceeding = []

# SpeakerList以外の定例会の議事録内で指名されている全ての氏名のリストを作成
for i in range(len(json_load)):
    proceeding = json_load[i]["Proceeding"]
    for n in range(len(proceeding)):
        utterance = list(proceeding[n]["Utterance"].replace('　', '').split('\n'))
        utterance = list(filter(lambda str:str != '', utterance))
        for s in range(len(utterance)):
            if utterance[s][-1] == '君':
                Proceeding.append(utterance[s].split('番')[-1].split('君')[0])

# 氏名に含まれる不要な役職名等を削除
for key in POST:
    for i, text in enumerate(Proceeding):
        if key in text:
            Proceeding[i] = text.split(key)[1]

# 議員と予想される氏名をまとめる
SpeakerList = list(set(SpeakerList + Proceeding))

# 偽装用
url = "https://search.metro.tokyo.lg.jp/?sitesearch=www.gikai.metro.tokyo.jp&filetype=&start_dt=&end_dt=&ord=&category_serialized=&temp=JP&ie=u&kw="
session = HTMLSession()
r = session.get(url)
soup = bs4.BeautifulSoup(r.content, "html.parser")

for parl in range(len(SpeakerList)):

    name = SpeakerList[parl].replace(' ', '') + '（'
    print(name)

    nameurl = url + name

    # セッション開始
    session = HTMLSession()
    r = session.get(nameurl)
    soup = bs4.BeautifulSoup(r.content, "html.parser")

    
    # 検索した議員名の発言が含まれる議事録ページ数
    pages = int((soup.find(class_='count')).get_text().replace(',', ''))
    print(pages)

    for i in range(pages):
        num = str(i+1)
        print(num)
        page = "&num=1&page=" + num
        pageurl = nameurl + page

        # タイトルを取得
        try:
            title, text = get_title_text(pageurl)
        # まれに抽出に失敗するためretryingで強制再試行
        except:
            print('TRY AGAIN')


        # 検索時にPDFファイルがヒットするとデコードに失敗するので回避する
        if title != []:
            title = kansuji2arabic(title, True)
            era = re.search(r'(昭和|平成|令和)(\d{2}|\元)\年', title)
            if era:
                year = j2w.convert(kansuji2arabic(era.group(), True))

        name = name.replace('（', '')
        POLI_DIC.setdefault(name,{}) 
        for key in PARTY_DIC.keys():
            POLI_DIC[name].setdefault(key, [])
            kets = name + "（" + key + "）"
            if kets in text:
                POLI_DIC[name][key].append(year)
                POLI_DIC[name][key] = sorted(list(set(POLI_DIC[name][key])))
        for key in PARTY_DIC.keys():
            if POLI_DIC[name][key] == []:
                POLI_DIC[name].pop(key)
            if POLI_DIC[name] == {}:
                POLI_DIC.pop(name)
    print(POLI_DIC)