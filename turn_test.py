# 단어 리스트 로드
wordList = []

f = open('word_list.txt','r')
while True:
    line = f.readline()
    if not line: break
    wordList.append(line.strip())


# 끝말 일치 확인
def isMatched(first,later):
    return list(first)[-1] == list(later)[0]


# AI 단어 탐색
def getAIWord(myWord):
    for word in wordList:
        if isMatched(myWord,word):
            return word



lastWord = ""

# 턴 진행
while True:
    myWord = input("[내 차례] : ").strip()

    # GG
    if myWord == "":
        print('게임 종료')
        break
    
    # 매치 실패
    if lastWord != "":
        if not isMatched(lastWord, myWord):
            print(lastWord+"와 끝말이 일치하지 않습니다.")
            continue
    
    # AI 단어 불러오기
    aiWord = getAIWord(myWord)

    # 실패 시 플레이어 승리
    if aiWord is None:
        print('당신의 승리!')
        break

    # AI 단어 출력
    print('[AI 차례] : ' + aiWord)
    print()

    # 마지막 단어 갱신
    lastWord = aiWord