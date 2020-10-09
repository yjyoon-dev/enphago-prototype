import requests
from bs4 import BeautifulSoup

openApiKey = "6BA64977BF783DF87C9AAD7B59F834D9"
params = "&type_search=search&q="

word = input("검색할 단어를 입력하시오 : ").strip()

openUrl = "https://stdict.korean.go.kr/api/search.do?certkey_no=1945&key=" + openApiKey + params + word

res = requests.get(openUrl)
soup = BeautifulSoup(res.content, 'html.parser')

# 단어 유효성 체크
check = soup.find('total').get_text()
if check=='0':
    print('존재하지 않는 단어입니다')

wordPos = soup.find('pos').get_text().strip() # 단어의 품사
wordType = soup.find('type').get_text().strip() # 단어의 어휘
wordLen = len(soup.find('word').get_text()) # 단어의 길이
wordDef = soup.find('definition').get_text() # 단어의 정의

if wordPos != "명사":
    print('명사가 아닙니다!')
elif wordType != "일반어":
    print('일반어가 아닙니다!')
elif wordLen < 2:
    print('단어가 너무 짧습니다!')
else:
    print('['+wordPos+']\n'+wordDef)
    