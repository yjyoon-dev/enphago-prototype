import requests
from bs4 import BeautifulSoup

def checkWords(openUrl):
    res = requests.get(openUrl)
    soup = BeautifulSoup(res.content, 'html.parser')

    # 단어 존재 유무 체크
    check = soup.find('total')
    if check is None or check.get_text()=='0':
        return (-1, "")

    # 단어의 유형 파악
    wordPos = soup.find('pos')
    wordCat = soup.find('cat')
    wordType = soup.find('type')

    # 추출한 단어
    word = soup.find('word')
    if word is not None:
        word = word.get_text().strip()

    # 단어 유효성 검사
    if len(word) < 2:
        return (-2,"")
    elif wordPos is not None and wordPos.get_text().strip() != "명사":
        return (-3, "")
    elif wordType is not None and wordType.get_text().strip() != "일반어":
        return (-4, "")
    elif wordCat is not None:
        return (-5, "")
    elif word.count('-') > 0 or word.count('^') > 0 or word.count(' ') > 0:
        return (-6, "")
    else:
        return (0, word)


openApiKey = "your_open_api_key"
params = "&target_type=view&method=target_code&q="

wordList = []

# api 문서의 500000번째 index까지 조회
for i in range(1,500000):
    openUrl = "https://opendict.korean.go.kr/api/view?certkey_no=1949&key=" + openApiKey + params + str(i)
    checkResult, word = checkWords(openUrl)
    if checkResult == 0 and word not in wordList:
            wordList.append(word)

# 외부 로컬에 백업
f = open("wordList.txt",'w')
for word in wordList:
    f.write(word)
f.close()

print(str(len(wordList))+"개의 단어가 준비되었습니다")