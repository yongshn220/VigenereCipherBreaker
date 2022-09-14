
from collections import Counter
from curses.ascii import isalpha
import readline


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
            text = input("Enter the plaintext: ")
            result = vcEncoder(text, key)
            print("-------------------------------------------------------------------------------------------------------")
            print("ciphertext: ", result)
        elif choice == 2: 
            key = input("Enter the key: ")
            text = input("Enter the ciphertext: ")
            result = vcDecoder(text, key)
            print("-------------------------------------------------------------------------------------------------------")
            print("plaintext: ", result)
        elif choice == 3:
            keylength = int(input("Enter the key length: "))
            text = input("Enter the ciphertext: ")
            key, result = vcBreakByKeyLength(text, keylength)
            print("-------------------------------------------------------------------------------------------------------")
            print("key: ",key)
            print("plaintext: ", result)
        elif choice == 4:
            text = input("Enter the ciphertext: ")
            key, result = vcCompleteBreak(text)
            print("-------------------------------------------------------------------------------------------------------")
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

    alphabet = "abcdefghijklmnopqrstuvwxyz"

    possibleKey = ""

    for i in range(keylength):
        indexCollectedString = getCharsInListByIndex(divTextList, i) # every i_th chars in every strings in the list. 

        minSum = 100
        bestKey = ""
        for c in alphabet:
            decryptedString = vcDecoder(indexCollectedString, c.upper())
            sum = getFreqencySum(decryptedString)
            if minSum > sum:
                minSum = sum
                bestKey = c
        possibleKey += bestKey
    
    possibleKey = possibleKey.upper()
    
    decryptedText = vcDecoder(ciphertext, possibleKey)
    return possibleKey, decryptedText


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

# part4
def vcCompleteBreak(ciphertext):
    subsets = getSubsetsOfEvery23(ciphertext)
    mostsubsets = getMostFrequentSubset(subsets)
    factors = getHighestCommonFactors(subsets, mostsubsets)

    minSum = 100
    bestKey = ""
    bestText = ""
    print("Calculating...")
    for f in factors:
        key, text = vcBreakByKeyLength(ciphertext, f)
        sum = getFreqencySum(text)
        if (minSum > sum):
            minSum = sum
            bestKey = key
            bestText = text
        print(".")
    print("Calculation finished")
    bestKey = bestKey.upper()
    return bestKey, bestText

    
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
    top5 = sorted(count, key=count.get, reverse=True)[:5]
    return top5


def getSubsetsOfEvery23(str):
    newstr = ""
    for c in str:
        if isalpha(c):
            newstr += c.upper()
    return list(newstr[i:i+3] for i in range(len(newstr) - 2))

main()


