import re
import requests, bs4
from requests_html import HTMLSession
from retry import retry

tt_ksuji = str.maketrans('一二三四五六七八九〇壱弐参', '1234567890123')
re_suji = re.compile(r'[十拾百千万億兆\d]+')
re_kunit = re.compile(r'[十拾百千]|\d+')
re_manshin = re.compile(r'[万億兆]|[^万億兆]+')

TRANSUNIT = {'十': 10,
             '拾': 10,
             '百': 100,
             '千': 1000}
TRANSMANS = {'万': 10000,
             '億': 100000000,
             '兆': 1000000000000}

# 漢数字をアラビア数字に変換する関数
def kansuji2arabic(kstring: str, sep=False):
    def _transvalue(sj: str, re_obj=re_kunit, transdic=TRANSUNIT):
        unit = 1
        result = 0
        for piece in reversed(re_obj.findall(sj)):
            if piece in transdic:
                if unit > 1:
                    result += unit
                unit = transdic[piece]
            else:
                val = int(piece) if piece.isdecimal() else _transvalue(piece)
                result += val * unit
                unit = 1

        if unit > 1:
            result += unit

        return result

    transuji = kstring.translate(tt_ksuji)
    for suji in sorted(set(re_suji.findall(transuji)), key=lambda s: len(s),
                           reverse=True):
        if not suji.isdecimal():
            arabic = _transvalue(suji, re_manshin, TRANSMANS)
            arabic = format(arabic) if sep else str(arabic)
            transuji = transuji.replace(suji, arabic)
        elif sep and len(suji) > 3:
            transuji = transuji.replace(suji, format(int(suji)))

    return transuji

# スクレイピング再試行用関数
@retry(tries=3, delay=2, backoff=2)
def get_title_text(url):

    # セッション開始
    session = HTMLSession()
    r = session.get(url)
    soup = bs4.BeautifulSoup(r.content, "html.parser")
    title = soup.find(class_='title_area').get_text().strip()

    gikai = (soup.find(class_='uri_area').get_text().strip())
    text = soup.get_text() 

    return title, text
