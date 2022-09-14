##
##
## NEED TO INSTALL
## 
##
##
##

from collections import Counter
from curses.ascii import isalpha
from textblob import TextBlob


file = open('longtext.txt', 'r')
TEXT = file.read()

def main():
    while(True):
        try:
            
            print("-------------------------------------------------------------------------------------------------------")
            print("Choose the task.")
            print("(1) cipher encoder. (2) cipher decoder. (3) break cipher with lenght. (4) complete break cipher. (5) Exit")
            choice = int(input("Enter: "))
            print("choice : ", choice)
        except:
            print("wrong input. Do it again.")
            return

        if choice == 1:
            key = input("Enter the key: ")
            result = vcEncoder(TEXT, key)
            print("ciphertext: ", result)
        if choice == 2: 
            key = input("Enter the key: ")
            result = vcDecoder(TEXT, key)
            print("plaintext: ", result)
        if choice == 3:
            keylength = int(input("Enter the key length: "))
            key, result = vcBreakByKeyLength(TEXT, keylength)
            print("key: ",key)
            print("plaintext: ", result)
        if choice == 4:
            key, result = vcCompleteBreak(TEXT)
            print("key: ",key)
            print("plaintext: ", result)
        else: return
        print("-------------------------------------------------------------------------------------------------------")



#part1
def vcEncoder(plaintext, key):
    key = key.upper()
    i = 0
    result = ""
    for c in plaintext:
        offset = 0
        if (c.isalpha()):
            if (c.islower()): offset = 32
            c_ord = ord(c.upper()) + ord(key[i]) - 65
            if (c_ord > 90): c_ord = c_ord - 26
            c = chr(c_ord + offset)
            i = 0 if (len(key) == i+1) else (i+1)
        result += c
    return result


# part2 
def vcDecoder(ciphertext, key):
    key = key.upper()
    i = 0
    result = ""
    for c in ciphertext:
        offset = 0
        if (c.isalpha()):
            if (c.islower()): offset = 32
            c_ord = ord(c.upper()) - (ord(key[i]) - 65)
            if (c_ord < 65): c_ord = c_ord + 26
            c = chr(c_ord + offset)
            i = 0 if (len(key) == i+1) else (i+1)
        result += c
    return result

# part3
def vcBreakByKeyLength(ciphertext, keylength):
    divTextList = divideTextByLength(ciphertext, keylength) # divide cipher text into set of keylength. 

    possibleKeyChars = [[] for _ in range(keylength)]

    for i in range(keylength):
        indexCollectedString = getCharsInListByIndex(divTextList, i) # every i_th chars in every strings in the list. 

        if (indexCollectedString == False): continue
        mostCommonChars = getMostCommonChar(indexCollectedString) # most common chars
        
        for char in range(len(mostCommonChars)):
            pk = chr(ord("A") + (((ord(mostCommonChars[char][0]) - ord("E")) + 26) % 26))
            possibleKeyChars[i].append(pk)
    
    possibleKeys = []
    getPossibleKeys(possibleKeyChars, possibleKeys)

    minFsum = 100
    bestKey = ""
    bestDecryptedText = ""
    for key in possibleKeys:
        decryptedText = vcDecoder(ciphertext, key)
        fsum = getFreqencySum(decryptedText)
        if (fsum < minFsum):
            minFsum = fsum
            bestKey = key
            bestDecryptedText = decryptedText
    
    return bestKey, bestDecryptedText


def getFreqencySum(decryptedText):
    # From http://code.activestate.com/recipes/142813-deciphering-caesar-code/
    FREQ = [0.0749, 0.0129, 0.0354, 0.0362, 0.1400, 0.0218, 0.0174, 0.0422, 0.0665, 0.0027, 0.0047,
                0.0357, 0.0339, 0.0674, 0.0737, 0.0243, 0.0026, 0.0614, 0.0695, 0.0985, 0.0300, 0.0116,
                0.0169, 0.0028, 0.0164, 0.0004]
    
    charFreq = [0] * 26
    totalFreq = 0
    for c in decryptedText:
        if isalpha(c):
            c = c.lower()
            charFreq[ord(c) - ord('a')] += 1
            totalFreq += 1
    
    freqSum = 0
    for i in range(len(charFreq)):
        freqSum += abs((charFreq[i] / totalFreq) - FREQ[i])

    return freqSum

def getPossibleKeys(keyChars, result, key = ""):
    if (len(keyChars) <= 0):
        result.append(key)
        return

    for char in keyChars[0]:
        keycopy = key
        keycopy += char
        getPossibleKeys(keyChars[1:], result, keycopy)

def divideTextByLength(text, length):
    resultList = []
    dividedText = ""
    i = 0
    for c in text:
        if isalpha(c):
            if i < length:
                    dividedText += c
                    i += 1
            else:
                resultList.append(dividedText)
                dividedText = c
                i = 1
    resultList.append(dividedText)
    return resultList

def getCharsInListByIndex(list, index):
    if (list is None or list[0] is None or len(list[0]) <= index) : return False 

    result = ""

    for l in list: 
        if(len(l) > index):
            result += l[index]

    return result

def getMostCommonChar(str):
    str = str.upper()
    mostCommonList = Counter(str).most_common(2)
    print("mostCommons: ", mostCommonList)
    return [mostCommonList[0][0], mostCommonList[1][0]]


def getMostCommonCharTTT(str):
    str = str.upper()
    return Counter(str).most_common(1)[0][0]
    

# part4
def vcCompleteBreak(ciphertext):
    subsets = getSubsetsOfEvery23(ciphertext)
    mostsubsets = getMostFrequentSubset(subsets)
    factors = getHighestCommonFactors(subsets, mostsubsets)
    print(factors)
    exit(0)
    for f in factors:
        key, text = vcBreakByKeyLength(ciphertext, f)
        print(key)
    
def getHighestCommonFactors(subsets, mostsubset):
    mostsubset = mostsubset[0]

    indexes = []
    for i in range(len(subsets)):
        if (subsets[i] == mostsubset):
            indexes.append(i)

    factors = []
    for i in range(2, 100):
        curCount = 0
        for si in range(len(indexes)):
            for ei in range(len(indexes)):
                distance = indexes[ei] - indexes[si]
                if (distance % i == 0):
                    curCount += 1
        
        factors.append((i, curCount))

    highestFactors = list(map(lambda x : x[0], sorted(factors, key = lambda c : c[1], reverse=True)[:20]))
    return highestFactors


def getMostFrequentSubset(subsets):
    count = Counter(subsets)
    print(count)
    top5 = sorted(count, key=count.get, reverse=True)[:5]
    return top5


def getSubsetsOfEvery23(str):
    newstr = ""
    for c in str:
        if isalpha(c):
            newstr += c.upper()
    return list(newstr[i:i+3] for i in range(len(newstr) - 2))
    

def test():
    str = "You copied to super woman. What love is long text you paste! Sharing is copy paste the celebration of an old, i like synthwave is at that would save you guys know how much your. My text copied to paste long ass sentences and pasting? Think about pasting text copy on paper above us improve your long paragraphs for breakfast taco in word to super user edits update! You and long dense chunks will likely die in your beauty is super disappointed in waves to be it will be? This text copied by the paste function is super repetitive, the greek language begins to the one of experiments on. Do eiusmod tempor incididunt ut enim ad position like ours in text and paste clipboard or electric and paste. You paste text to super annoying songs right! Pending review the sunrise every text to super copy and long paste options to turn the door while loading this question and ideas to be pure elm. Lte as text copied items between us. Just copy text copied by one long dense chunk of the past, like dust or google draw an original problem for her to? In text and paste mode the enormous amounts! Every text copy. And shot it hit on facebook, and i will help in crude volumes must inform product. Get the npm package for her wordpress building, long text to copy and paste without regional restrictions, the best part of many topics, followed the the colored spectrum are you! Did not copy text! Format will tho, articles like i became a whole passages by linguists to my heart so, in deep fries! You paste text styles you would actually, another song that is super disappointed in pasting plain text and i wanted to the list and do all. But eventually it, and eat your long text to and copy paste it? You copy text below to super annoying smart mouthed kids, long birth names on your sweetie how is not show! What you are a text to copy and paste long threads, and not leave their trademark of pages on an error: are meant to? Now and text copied links to. Colonia remedies mayor was quite accomplished on. My text copied to paste long that? Unless you out copy to? They are not working fine for the long to help you go, and confirm your. The text and command line commands and formatted text symbol signs of symbols that used. Or copy and long as the water drops. Apple made the text art generator for her because i will give us not. The drawing and hold your lips as your brain: my world rejects you, i would love will appear imminent doom, a fun text will paste to? Lte in text copied item you for those reasons were both through the long now deleted it took me when i enter a fine. But none of symbols from darkness in toki pona is the paragraph structures into the trials we deserve every. Why type words like to super repetitive, white to your mailchimp and enjoy your fingers quickly paste into a variety of. Copy text copy to super woman. You and long as early winter? Already did not copy paste long threads of copied. You do people over domain two rays emerging at doing the text to super copy and long, the study for a factor determining how much for your best way like. Change the pasting? Why do with paste long tweet fits into landscape and pasting formatted text copied links to super disappointed in. Beware if you more accurate than me with lots of long text until the marking of that has taken over! Love to copy pasting pages full of long as a better. Susanna is super annoying songs instead of honey to me pour out what? Yall are pasting text copy paste any other actions and energy. Thus create text and paste text fragments corresponding to super woman in an xml file will appear to word repeated throughout this lte without a rainbow to? To copy pasting html and long sentence should know that was hagrid expecting harry to access this. Silahkan kunjungi postingan funny."
    a = divideTextByLength(str,5)
    print(a)
    getMostCommonChar(str)

def test1():
    print( 0 % 4)

# test1()
main()


