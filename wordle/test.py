import requests

with open('20,000 Most Used Words in English.txt') as k20:
    words20k = tuple(k20.read().lower().split('\n'))
    print(', '.join(words20k[:50]))

    # I was going to make a file of only five-letter words, but decided not to.
    # I will leave all words in there to have more accurate word frequency information.
    fiveLetters = tuple(filter(lambda word: len(word) == 5, words20k))
    print(fiveLetters[:50])
    print(
        '\x1b[1mNumber of five-letter words in top 20,000: '
        + str(len(fiveLetters))
        + '\x1b[0m'
    )

with open('wiki-100k.txt') as k100:
    words100k = tuple(
        filter(
            lambda line: not line.startswith('#!comment:'),
            k100.read().lower().split('\n'),
        )
    )
    print('Number of lines left: ' + str(len(words100k)))

    fiveLetters = tuple(filter(lambda word: len(word) == 5, words100k))
    print(fiveLetters[:50])
    print(
        '\x1b[1mNumber of five-letter words in top 98,913: '
        + str(len(fiveLetters))
    )

del fiveLetters

file = open('fiveLetterWords.txt')
words = tuple(file.read().lower().split(' '))[:50]
file.close()

wordObject = {}
for word in words:

    # Get the print string
    # <b>word:</b> part of speech. Definition 1. <i>"Example."</i>
    descrip = '\x1b[1m'
    request = requests.get(
        'https://api.dictionaryapi.dev/api/v2/entries/en/' + word
    )
    response = request.json()
    # Add "[word]: [part of speech]. [definition]" to print string
    try:
        response = response[0]
        descrip += ''.join(
            [
                word,
                ':\x1b[22m ',
                response['meanings'][0]['partOfSpeech'],
                '. ',
                response['meanings'][0]['definitions'][0]['definition'],
            ]
        )
        hasDef = True
    except KeyError:   # Add "[word]: No definitions found" to string
        descrip += ''.join(
            ['\x1b[2m', word, ':\x1b[22m ', response['title'], '\x1b[0m']
        )
        hasDef = False
    try:   # Add example
        descrip += (
            ' \x1b[3m"'
            + response['meanings'][0]['definitions'][0]['example']
            + '"\x1b[0m'
        )
    except KeyError:
        pass

    # Try to get frequency score from Wiki list
    # Else score 0
    try:
        wiki = (
            100000 / (words100k.index(word) + 1) / 6000
        )   # Range of 0.00016-16
    except ValueError:
        wiki = 0

    # Try to get the frequency score from Google's list
    # If it doesn't work, score 0
    try:
        google = (
            20000 / (words20k.index(word) + 1) / 750
        )   # Range of 0.0013-26
    except ValueError:
        google = 0
        print(word + ' not in Google list. Score in Wiki list: ' + str(wiki))

    wordObject.update(
        {
            word: {
                'description': descrip,
                'googleScore': google,
                'wikiScore': wiki,
                'hasDefinition': hasDef,
            }
        }
    )

    """:
      To make a dictionary of letters
      Each sub-value is the number of words both keys are in.
      {letter: {alsoLetter: (sum((letter in word and alsoLetter in word) for word in words)) for alsoLetter in alpha} for letter in alpha}
      From the whole word list:
      
        {'a': {'a': 5122, 'b': 586, 'c': 739, 'd': 806, 'e': 1700, 'f': 313, 'g': 604, 'h': 625, 'i': 959, 'j': 120, 'k': 536, 'l': 1281, 'm': 774, 'n': 1080, 'o': 847, 'p': 696, 'q': 47, 'r': 1591, 's': 2158, 't': 1126, 'u': 600, 'v': 284, 'w': 398, 'x': 90, 'y': 627, 'z': 174}, 'b': {'a': 586, 'b': 1447, 'c': 123, 'd': 195, 'e': 572, 'f': 44, 'g': 120, 'h': 97, 'i': 334, 'j': 30, 'k': 116, 'l': 310, 'm': 164, 'n': 216, 'o': 453, 'p': 36, 'q': 6, 'r': 426, 's': 537, 't': 225, 'u': 326, 'v': 21, 'w': 56, 'x': 16, 'y': 216, 'z': 39}, 'c': {'a': 739, 'b': 123, 'c': 1841, 'd': 209, 'e': 663, 'f': 83, 'g': 67, 'h': 383, 'i': 502, 'j': 12, 'k': 236, 'l': 359, 'm': 190, 'n': 288, 'o': 597, 'p': 200, 'q': 3, 'r': 487, 's': 647, 't': 331, 'u': 342, 'v': 59, 'w': 66, 'x': 22, 'y': 217, 'z': 26}, 'd': {'a': 806, 'b': 195, 'c': 209, 'd': 2213, 'e': 1213, 'f': 106, 'g': 174, 'h': 167, 'i': 607, 'j': 32, 'k': 133, 'l': 396, 'm': 207, 'n': 403, 'o': 661, 'p': 189, 'q': 10, 'r': 580, 's': 732, 't': 269, 'u': 389, 'v': 89, 'w': 180, 'x': 48, 'y': 333, 'z': 42}, 'e': {'a': 1700, 'b': 572, 'c': 663, 'd': 1213, 'e': 5514, 'f': 383, 'g': 550, 'h': 562, 'i': 1165, 'j': 103, 'k': 487, 'l': 1269, 'm': 704, 'n': 1050, 'o': 1163, 'p': 739, 'q': 33, 'r': 1826, 's': 2246, 't': 1198, 'u': 630, 'v': 419, 'w': 444, 'x': 186, 'y': 635, 'z': 176}, 'f': {'a': 313, 'b': 44, 'c': 83, 'd': 106, 'e': 383, 'f': 953, 'g': 72, 'h': 70, 'i': 279, 'j': 10, 'k': 64, 'l': 247, 'm': 57, 'n': 127, 'o': 242, 'p': 25, 'q': 6, 'r': 290, 's': 404, 't': 201, 'u': 197, 'v': 12, 'w': 50, 'x': 18, 'y': 144, 'z': 24}, 'g': {'a': 604, 'b': 120, 'c': 67, 'd': 174, 'e': 550, 'f': 72, 'g': 1478, 'h': 128, 'i': 414, 'j': 22, 'k': 53, 'l': 315, 'm': 140, 'n': 402, 'o': 447, 'p': 126, 'q': 2, 'r': 406, 's': 516, 't': 195, 'u': 309, 'v': 46, 'w': 64, 'x': 4, 'y': 231, 'z': 29}, 'h': {'a': 625, 'b': 97, 'c': 383, 'd': 167, 'e': 562, 'f': 70, 'g': 128, 'h': 1632, 'i': 379, 'j': 20, 'k': 138, 'l': 272, 'm': 187, 'n': 224, 'o': 460, 'p': 166, 'q': 5, 'r': 330, 's': 686, 't': 442, 'u': 273, 'v': 44, 'w': 154, 'x': 13, 'y': 202, 'z': 22}, 'i': {'a': 959, 'b': 334, 'c': 502, 'd': 607, 'e': 1165, 'f': 279, 'g': 414, 'h': 379, 'i': 3437, 'j': 64, 'k': 370, 'l': 827, 'm': 498, 'n': 856, 'o': 557, 'p': 446, 'q': 45, 'r': 942, 's': 1400, 't': 828, 'u': 317, 'v': 237, 'w': 209, 'x': 98, 'y': 315, 'z': 123}, 'j': {'a': 120, 'b': 30, 'c': 12, 'd': 32, 'e': 103, 'f': 10, 'g': 22, 'h': 20, 'i': 64, 'j': 268, 'k': 29, 'l': 41, 'm': 26, 'n': 49, 'o': 88, 'p': 26, 'q': 0, 'r': 43, 's': 103, 't': 33, 'u': 69, 'v': 8, 'w': 11, 'x': 1, 'y': 36, 'z': 2}, 'k': {'a': 536, 'b': 116, 'c': 236, 'd': 133, 'e': 487, 'f': 64, 'g': 53, 'h': 138, 'i': 370, 'j': 29, 'k': 1372, 'l': 239, 'm': 95, 'n': 294, 'o': 352, 'p': 142, 'q': 7, 'r': 319, 's': 713, 't': 175, 'u': 229, 'v': 17, 'w': 81, 'x': 2, 'y': 214, 'z': 19}, 'l': {'a': 1281, 'b': 310, 'c': 359, 'd': 396, 'e': 1269, 'f': 247, 'g': 315, 'h': 272, 'i': 827, 'j': 41, 'k': 239, 'l': 3016, 'm': 329, 'n': 365, 'o': 846, 'p': 382, 'q': 10, 'r': 459, 's': 1201, 't': 474, 'u': 545, 'v': 163, 'w': 197, 'x': 55, 'y': 454, 'z': 49}, 'm': {'a': 774, 'b': 164, 'c': 190, 'd': 207, 'e': 704, 'f': 57, 'g': 140, 'h': 187, 'i': 498, 'j': 26, 'k': 95, 'l': 329, 'm': 1806, 'n': 249, 'o': 534, 'p': 193, 'q': 6, 'r': 418, 's': 740, 't': 270, 'u': 383, 'v': 32, 'w': 60, 'x': 39, 'y': 255, 'z': 42}, 'n': {'a': 1080, 'b': 216, 'c': 288, 'd': 403, 'e': 1050, 'f': 127, 'g': 402, 'h': 224, 'i': 856, 'j': 49, 'k': 294, 'l': 365, 'm': 249, 'n': 2694, 'o': 823, 'p': 256, 'q': 16, 'r': 515, 's': 997, 't': 523, 'u': 478, 'v': 110, 'w': 217, 'x': 42, 'y': 362, 'z': 64}, 'o': {'a': 847, 'b': 453, 'c': 597, 'd': 661, 'e': 1163, 'f': 242, 'g': 447, 'h': 460, 'i': 557, 'j': 88, 'k': 352, 'l': 846, 'm': 534, 'n': 823, 'o': 3743, 'p': 543, 'q': 17, 'r': 1061, 's': 1586, 't': 833, 'u': 443, 'v': 167, 'w': 319, 'x': 76, 'y': 496, 'z': 126}, 'p': {'a': 696, 'b': 36, 'c': 200, 'd': 189, 'e': 739, 'f': 25, 'g': 126, 'h': 166, 'i': 446, 'j': 26, 'k': 142, 'l': 382, 'm': 193, 'n': 256, 'o': 543, 'p': 1817, 'q': 7, 'r': 473, 's': 849, 't': 337, 'u': 341, 'v': 29, 'w': 79, 'x': 23, 'y': 321, 'z': 26}, 'q': {'a': 47, 'b': 6, 'c': 3, 'd': 10, 'e': 33, 'f': 6, 'g': 2, 'h': 5, 'i': 45, 'j': 0, 'k': 7, 'l': 10, 'm': 6, 'n': 16, 'o': 17, 'p': 7, 'q': 104, 'r': 16, 's': 34, 't': 25, 'u': 93, 'v': 0, 'w': 2, 'x': 0, 'y': 7, 'z': 1}, 'r': {'a': 1591, 'b': 426, 'c': 487, 'd': 580, 'e': 1826, 'f': 290, 'g': 406, 'h': 330, 'i': 942, 'j': 43, 'k': 319, 'l': 459, 'm': 418, 'n': 515, 'o': 1061, 'p': 473, 'q': 16, 'r': 3788, 's': 1415, 't': 772, 'u': 646, 'v': 182, 'w': 231, 'x': 48, 'y': 476, 'z': 75}, 's': {'a': 2158, 'b': 537, 'c': 647, 'd': 732, 'e': 2246, 'f': 404, 'g': 516, 'h': 686, 'i': 1400, 'j': 103, 'k': 713, 'l': 1201, 'm': 740, 'n': 997, 'o': 1586, 'p': 849, 'q': 34, 'r': 1415, 's': 5719, 't': 1333, 'u': 1041, 'v': 210, 'w': 474, 'x': 82, 'y': 576, 'z': 99}, 't': {'a': 1126, 'b': 225, 'c': 331, 'd': 269, 'e': 1198, 'f': 201, 'g': 195, 'h': 442, 'i': 828, 'j': 33, 'k': 175, 'l': 474, 'm': 270, 'n': 523, 'o': 833, 'p': 337, 'q': 25, 'r': 772, 's': 1333, 't': 2950, 'u': 529, 'v': 71, 'w': 200, 'x': 46, 'y': 372, 'z': 51}, 'u': {'a': 600, 'b': 326, 'c': 342, 'd': 389, 'e': 630, 'f': 197, 'g': 309, 'h': 273, 'i': 317, 'j': 69, 'k': 229, 'l': 545, 'm': 383, 'n': 478, 'o': 443, 'p': 341, 'q': 93, 'r': 646, 's': 1041, 't': 529, 'u': 2327, 'v': 59, 'w': 37, 'x': 29, 'y': 303, 'z': 47}, 'v': {'a': 284, 'b': 21, 'c': 59, 'd': 89, 'e': 419, 'f': 12, 'g': 46, 'h': 44, 'i': 237, 'j': 8, 'k': 17, 'l': 163, 'm': 32, 'n': 110, 'o': 167, 'p': 29, 'q': 0, 'r': 182, 's': 210, 't': 71, 'u': 59, 'v': 642, 'w': 25, 'x': 9, 'y': 58, 'z': 6}, 'w': {'a': 398, 'b': 56, 'c': 66, 'd': 180, 'e': 444, 'f': 50, 'g': 64, 'h': 154, 'i': 209, 'j': 11, 'k': 81, 'l': 197, 'm': 60, 'n': 217, 'o': 319, 'p': 79, 'q': 2, 'r': 231, 's': 474, 't': 200, 'u': 37, 'v': 25, 'w': 1003, 'x': 12, 'y': 128, 'z': 17}, 'x': {'a': 90, 'b': 16, 'c': 22, 'd': 48, 'e': 186, 'f': 18, 'g': 4, 'h': 13, 'i': 98, 'j': 1, 'k': 2, 'l': 55, 'm': 39, 'n': 42, 'o': 76, 'p': 23, 'q': 0, 'r': 48, 's': 82, 't': 46, 'u': 29, 'v': 9, 'w': 12, 'x': 267, 'y': 31, 'z': 2}, 'y': {'a': 627, 'b': 216, 'c': 217, 'd': 333, 'e': 635, 'f': 144, 'g': 231, 'h': 202, 'i': 315, 'j': 36, 'k': 214, 'l': 454, 'm': 255, 'n': 362, 'o': 496, 'p': 321, 'q': 7, 'r': 476, 's': 576, 't': 372, 'u': 303, 'v': 58, 'w': 128, 'x': 31, 'y': 1952, 'z': 50}, 'z': {'a': 174, 'b': 39, 'c': 26, 'd': 42, 'e': 176, 'f': 24, 'g': 29, 'h': 22, 'i': 123, 'j': 2, 'k': 19, 'l': 49, 'm': 42, 'n': 64, 'o': 126, 'p': 26, 'q': 1, 'r': 75, 's': 99, 't': 51, 'u': 47, 'v': 6, 'w': 17, 'x': 2, 'y': 50, 'z': 371}}
      """

with open('fiveLetterWords.py', 'a') as file:
    file.write('words = ' + str(wordObject))
