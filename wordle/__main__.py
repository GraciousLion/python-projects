#! python3
import re, requests
from misc import forceLength, greenToWord

noConnection = False

words = tuple(open('wordle/fiveLetterWords.txt').read().lower().split(' '))

green = [None, None, None, None, None]
yellow = {0: [], 1: [], 2: [], 3: [], 4: []}
black = []

guesses = []

ordinal = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth']

for i in range(6):
    # try:
    guesses.append(
        forceLength(
            '\nPlease enter your ' + ordinal[i] + ' guess: ', 5
        ).lower()
    )
    colors = forceLength('Please enter the color of the letters: ', 5).lower()
    # except KeyboardInterrupt:
    #   sendHelp()
    while not re.match('[gyb]{5}', colors):
        colors = forceLength(
            'Letters colored green should be represented by "g", yellow letters should be represented by "y", and black should be represented by "b". The string you enter should look like "ybbyg". ',
            5,
        ).lower()

    # Find good, close, and bad letters and add them to categories
    for i in range(5):
        color = colors[i]
        letter = guesses[-1][i]
        if color == 'g':
            green[i] = letter
        elif color == 'y':
            yellow[i].append(letter)
        elif color == 'b':
            black.append(letter)
        else:
            print(
                'String failed to pass any if. '
                + color
                + ' is not g, y, or b.'
            )

    print('\nKnown letters: ' + greenToWord(green))

    words = tuple(
        filter(
            (
                lambda word: all(
                    map(
                        lambda ind: all(
                            map(
                                lambda l: word[ind] != l and l in word,
                                yellow[ind],
                            )
                        ),
                        yellow,
                    )
                )
                and all(map((lambda l: l not in word), black))
                and all(
                    [
                        False
                        for should, actual in zip(green, word)
                        if should != actual and should
                    ]
                )
            ),
            words,
        )
    )

    if len(words) > 1:
        print(
            '\nThese are the '
            + str(len(words))
            + ' possible words based on your input: \n'
        )

        for word in words:
            try:
                printable = '\x1b[1m'
                if noConnection:
                    printable = word + '\x1b[0m'
                else:
                    try:
                        request = requests.get(
                            'https://api.dictionaryapi.dev/api/v2/entries/en/'
                            + word
                        )
                        response = request.json()
                        # Add "[word]: [part of speech]. [definition]" to print string
                        try:
                            response = response[0]
                            printable += (
                                word
                                + ':\x1b[22m '
                                + response['meanings'][0]['partOfSpeech']
                                + '. '
                                + response['meanings'][0]['definitions'][0][
                                    'definition'
                                ]
                            )
                        except KeyError:   # Add "[word]: No definitions found" to string
                            printable += (
                                '\x1b[2m'
                                + word
                                + ':\x1b[22m '
                                + response['title']
                                + '\x1b[0m'
                            )
                        try:   # Add example
                            printable += (
                                ' \x1b[3m"'
                                + response['meanings'][0]['definitions'][0][
                                    'example'
                                ]
                                + '"\x1b[0m'
                            )
                        except:
                            pass
                    except requests.exceptions.ConnectionError:
                        printable = word + '\x1b[0m'
                        noConnection = True
                print(printable)
            except KeyboardInterrupt:
                noConnection = not noConnection
                print(
                    '\nDefinitions turned '
                    + ('off.' if noConnection else 'on.')
                )
        # End of "for word in words" loop
    else:
        print(
            '\nYou won! The only possible word is "' + ' '.join(words) + '"!'
        )
        break

# :
# for word in words:
#   response = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/'+word)
#   # print(response.json()[0])

#   try:
#     response = dict(response.json()[0])
#     string = word+': '+response['meanings'][0]['partOfSpeech']+'. '+response['meanings'][0]['responseitions'][0]['responseition']
#   except KeyError:
#     response = dict(response.json())
#     string = word+': '+response['title']
#   try:
#     string += ' '+response['meanings'][0]['responseitions'][0]['example']
#   except:
#     pass

# map(lambda ind : all(map(lambda l : word[ind] != l, yellow[ind])), yellow)

# PLAIN
# gbbbb

# PROBE
# gyyby

# POWER
# ggggg
"""
ABCDEFGHIJKLMNOPQRSTUVWXYZ 01234
abcdefghijklmnopqrstuvwxyz 56789
 {}[]()><$*-+=/_%^@\&|~?'"!,.;:
"""
