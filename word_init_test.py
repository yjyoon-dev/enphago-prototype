import requests
from bs4 import BeautifulSoup

def checkWords(openUrl):
    res = requests.get(openUrl)
    soup = BeautifulSoup(res.content, 'html.parser')

    # 단어 유효성 체크
    check = soup.find('total').get_text()
    if check=='0':
        return (-1, "")

    wordPos = soup.find('pos').get_text().strip() # 단어의 품사
    wordType = soup.find('word_type').get_text().strip()
    word = soup.find('word').get_text() # 추출한 단어

    if wordPos != "명사":
        return (-2, "")
    elif wordType == "혼종어" or word.count('^') > 0 or word.count('-') > 0:
        return (-3, "")
    elif len(word) < 2:
        return (-4, "")
    else:
        return (0, word)

openApiKey = "6BA64977BF783DF87C9AAD7B59F834D9"
params = "&type_search=view&method=TARGET_CODE&q="

validIndex = []
wordList = {}

for i in range(1,500000):
    openUrl = "https://stdict.korean.go.kr/api/view.do?certkey_no=1945&key=" + openApiKey + params + str(i)
    checkResult, word = checkWords(openUrl)
    if checkResult == 0:
        if word not in wordList:
            wordList[word]=False
            validIndex.append((i,word))
            print(word)
    else: print(i, checkResult)

f = open("./validIndex.txt",'w')
for index, word in validIndex:
    f.write(str(index)+' '+word+'\n')

print(str(len(wordList))+"개의 단어가 준비되었습니다")