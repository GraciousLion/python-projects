#!/usr/bin/python3


def limit(n, min=False, max=False):
    if min and n < min:
        return min
    if max and n > max:
        return max
    return n


with open('.local/lib/python3.7/site-packages/hidden/words.txt') as w:
    p = 4   # This value represents how important it is that the word be nearly 10 letters
    words = {
        line.strip().lower(): limit(
            15 - (abs(10 - len(line.strip())) * p), 0.5
        )
        for line in w
        if len(line.strip()) >= 5
    }
    # masterOldList = []
    # for i in range(len(max(words, key=len))+1):
    #   masterOldList.append([word for word in words if len(word) == i])
# with open('newWords.txt') as w:
#   p = 4 # This value represents how important it is that the word be nearly 10 letters
#   words.update({
#     line.strip().lower():
#     limit(15 - (abs(10-len(line.strip()))*p), 0.5)
#     for line in w if len(line.strip()) >= 5
#   })

men = {
    0: '\n\n\n',
    1: '\n  O\n\n',
    2: """
  O
  |\n""",
    3: """
__O
  |\n""",
    4: """
__O__
  |\n""",
    5: """
__O__
  |
 /""",
    6: """
__O__
  |
 / \ """,
    7: """
__O__
  |
_/ \ """,
    8: """
__O__
  |
_/ \_""",
    9: """   |
__O__
  |
_/ \_""",
    10: """   |
__X__
  |
_/ \_""",
}

# print(words)
# for i in range(5, len(max(words.keys(), key=len))+1):
#  print(f'{i} letters: {limit(15 - (abs(10-i)*p), 0.5)}')

"""print(f'len(words): {len(words)} ')#len(newWords): len(newWords) len(superWords): {len(superWords)}')
print('           old  new')
for i in range(5, len(max(max(words, key=len), max(newWords, key=len), key=len))):
  print(f'{i} letters: {len(masterOldList[i]) if i < len(masterOldList) else 0}  {len(masterNewList[i]) if i < len(masterNewList) else 0}')"""

# Define text colors
# Credit: IcemasterEric of The ASIAN Difficulty Game.
black = '\x1b[30m'
red = '\x1b[31m'
green = '\x1b[32m'
orange = '\x1b[33m'
blue = '\x1b[34m'
magenta = '\x1b[35m'
lightBlue = '\x1b[36m'
reset = '\x1b[0m'


allwords = ''.join(words.keys())
alphabet = [
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k',
    'l',
    'm',
    'n',
    'o',
    'p',
    'q',
    'r',
    's',
    't',
    'u',
    'v',
    'w',
    'x',
    'y',
    'z',
]
""":
  alphaDict = {}
  
  for x in alphabet:
    alphaDict.update({x: allwords.count(x)})
  
  lettersInOrder = sorted(alphaDict, key=alphaDict.get, reverse=True)
  alphaDict = {letter:alphaDict[letter] for letter in lettersInOrder}
  for n in alphaDict:
    print(n + ': ' + str(alphaDict[n]))
  
  
  lettersInWordsTable = []
  
  for letter in alphabet:
    lettersInWordsTable.append([])
    for otherLetter in alphabet:
      countTwoLetters = (len(tuple(filter(lambda word : letter in word and otherLetter in word, words.keys())))) if letter != otherLetter else 0
      lettersInWordsTable[-1].append(countTwoLetters)
  
  
  for i in range(len(max(masterlist, key=len))):
    print('|' + (' {:^15} |'*len(masterlist)).format(*tuple(zip(*masterlist))[i]))
  
  
  print('   ' + '   '.join(alphabet))
  for i in range(len(max(lettersInWordsTable, key=len))):
    print(f'{alphabet[i]} '+('{:^4}'*len(lettersInWordsTable)).format(*lettersInWordsTable[i]))
  
input('Press enter to continue. ')"""
# wordsWithLetterInThem.update(letter:countOneLetter(letter))


def makeGuessWord():
    import os, random

    clearScreenCommand = 'cls' if os.name in ('nt', 'dos') else 'clear'
    randomWord = random.choices(
        tuple(words.keys()), weights=tuple(words.values())
    )[0]
    guessedLetters = []
    blankWord = '_' * len(randomWord)
    numGuesses = 0
    wrongGuesses = 0

    while True:
        os.system(clearScreenCommand)
        print(men[wrongGuesses])
        print('\n' + blankWord)
        print(', '.join(sorted(guessedLetters)))
        if '_' not in blankWord:
            won = True
            break
        if wrongGuesses == len(men) - 1:
            break
        guessedLetters.append(input('Guess a letter: '))
        if guessedLetters[-1] == randomWord:
            numGuesses += 1
            won = True
            break
        if len(guessedLetters[-1]) > 1:
            numGuesses += len(guessedLetters[-1])
            wrongGuesses += len(
                [x for x in guessedLetters[-1] if x not in randomWord]
            )
            guessedLetters += list(guessedLetters.pop())
        else:
            if guessedLetters[-1] not in randomWord:
                wrongGuesses += 1
            numGuesses += 1
        if wrongGuesses == len(men) - 2:
            won = False

        blankWord = ''.join(
            [
                (letter if letter in guessedLetters else '_')
                for letter in randomWord
            ]
        )

    if won:
        print(
            f'\nYou guessed {blue+randomWord+reset} in {magenta+str(numGuesses)+reset} guesses!\n'
        )
    else:
        print(
            f"Out of tries, you lose. The word you didn't guess was {red+randomWord+reset}."
        )


firstTime = True
while firstTime or input('To continue, press enter. ') == '':
    makeGuessWord()
    firstTime = False
