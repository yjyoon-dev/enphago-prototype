import requests
import random
from bs4 import BeautifulSoup
from two_pronoun_rules import convert

wordList = []
usedList = []
learningList = []
lastWord = ""

# 단어 리스트 로드
def wordInit():
    try:
        f = open('word_list.txt','r')
    except FileNotFoundError:
        print('단어 리스트를 로드할 수 없습니다.')
        exit(0)

    while True:
        line = f.readline().strip()
        if not line: break
        wordList.append(line)

    f.close()

    random.shuffle(wordList)


# 학습 단어 리스트 로드
def learningInit():
    try:
        f = open('learning_list.txt','r')
        
    except FileNotFoundError:
        print('학습 리스트를 로드할 수 없습니다.')
        exit(0)

    while True:
        line = f.readline().strip()
        if not line: break
        learningList.append(line)

    f.close()

    random.shuffle(learningList)


# 한글표준어대사전 Open API
def getUrl(word):    
    openApiKey = "6BA64977BF783DF87C9AAD7B59F834D9"
    params = "&type_search=search&q="
    baseUrl = "https://stdict.korean.go.kr/api/search.do?certkey_no=1945&key="
    return baseUrl + openApiKey + params + word


# 플레이어 단어 유효성 검사
def checkWord(word):

    # 단어 길이 검사
    if len(word) < 2:
        print('단어가 너무 짧습니다')
        return -1

    # beautifulsoup
    openUrl = getUrl(word)
    res = requests.get(openUrl)
    soup = BeautifulSoup(res.content, 'html.parser')

    # 단어 존재 유무 확인
    check = soup.find('total').get_text()
    if check=='0':
        print('존재하지 않는 단어입니다.')
        return -1

    wordPos = soup.find('pos').get_text().strip() # 단어의 품사
    wordType = soup.find('type').get_text().strip() # 단어의 어휘

    if wordPos != "명사":
        print('명사가 아닙니다.')
    elif wordType != "일반어":
        print('일반어가 아닙니다.')
    else: return 0
    return -1


# 단어 사전 출력
def printWordInfo(word,wordPos,wordDef):
    print()
    print(word)
    print('['+wordPos+'] ' + wordDef)


# beautifulsoup
def searchWord(word):
    openUrl = getUrl(word)
    res = requests.get(openUrl)
    soup = BeautifulSoup(res.content, 'html.parser')

    wordPos = soup.find('pos').get_text().strip() # 단어의 품사
    wordDef = soup.find('definition').get_text() # 단어의 정의

    printWordInfo(word,wordPos,wordDef)


# 끝말 일치 확인
def isMatched(first,later):
    rear = first[-1]
    front = later[0]

    rear = convert(rear) # 두음법칙 변환

    return rear == front


# AI 단어 탐색
def getAIWord(myWord):
    # 학습 리스트 탐색
    for word in learningList:
        if isMatched(myWord,word) and word not in usedList:
            return word
    
    # 단어 리스트 탐색
    for word in wordList:
        if isMatched(myWord,word) and word not in usedList:
            return word


# 단어 리스트 추가
def addWord(word):
    f = open("word_list.txt", 'a')
    f.write(word+'\n')
    f.close()


# AI 단어 학습
def learnWord(word):
    if word not in learningList:
        f = open("learning_list.txt", 'a')
        f.write(word+'\n')
        f.close()


# 게임 진행
wordInit()
learningInit()
while True:
    print()
    myWord = input("[내 차례] : ").strip()

    # GG
    if myWord == "/기권":
        print('패배하셨습니다.')

        # hint 출력
        hint = getAIWord(lastWord)
        if hint is not None:
            print('*Hint : '+hint)
        
        learnWord(lastWord) # 단어 학습

        break
    
    # 공백 입력 시
    if myWord == "":
        print('단어를 입력해주세요.')
        continue

    # 단어 검색
    if myWord =="?":
        searchWord(lastWord.strip())
        continue

    # 매치 실패
    if lastWord != "":
        if not isMatched(lastWord, myWord):
            print('"'+lastWord+'"'+"와 끝말이 일치하지 않습니다.")
            continue

    # 유효성 검사
    if checkWord(myWord) != 0: continue

    # 단어 사용 여부 체크
    if myWord in usedList:
        print('이미 사용된 단어입니다.')
        continue

    # 플레이어 단어 사용 반영
    usedList.append(myWord)
    
    # 플레이어 단어 학습
    if myWord not in wordList:
        addWord(myWord)

    # AI 단어 불러오기
    aiWord = getAIWord(myWord)

    # 실패 시 플레이어 승리
    if aiWord is None:
        print('당신의 승리!')
        learnWord(myWord)
        break

    # AI 단어 사용 반영
    usedList.append(aiWord)

    # AI 단어 출력
    print('[AI 차례] : ' + aiWord)

    # 마지막 단어 갱신
    lastWord = aiWord