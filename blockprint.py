#!/usr/bin/env python3

import sys, re
from os import get_terminal_size
from json import dumps

letters = {
    ' ': """
     
     
     
     
     """,
    'A': """
        
   /\\   
  /__\\  
 /    \\ 
/      \\""",
    'B': r"""
 ___ 
|   \
|___/
|   \
|___/""",
    'C': """
  ____ 
 /    \\
/      
\\      
 \\____/""",
    'D': r"""
 ___  
|   \ 
|    \
|    /
|___/ """,
    'E': """
 ____ 
|     
|____ 
|     
|____ """,
    'F': """
 ____ 
|     
|____ 
|     
|     """,
    'G': r"""
  _____ 
 /     \
/    ___
\      /
 \____/ """,
    'H': """
      
|    |
|____|
|    |
|    |""",
    'I': """
_____
  |  
  |  
  |  
__|__""",
    'J': r"""
 ____
   | 
   | 
   | 
\__/ """,
    'K': """
    
|  /
|_/ 
| \\ 
|  \\""",
    'L': """
     
|    
|    
|    
|____""",
    'M': r"""
          
|\      /|
| \    / |
|  \  /  |
|   \/   |""",
    'N': r"""
      
|\   |
| \  |
|  \ |
|   \|""",
    'O': r"""
  ___  
 /   \ 
/     \
\     /
 \___/ """,
    'P': r"""
 ___ 
|   \
|___/
|    
|    """,
    'Q': """
  ___  
 /   \\ 
/     \\
\\    \\/
 \\___/\\""",
    'R': """
 ___  
|   \\ 
|___/ 
|   \\ 
|    \\""",
    'S': r"""
 __ 
/  \
\__ 
   \
\__/""",
    'T': """
_____
  |  
  |  
  |  
  |  """,
    'U': r"""
       
|     |
|     |
\     /
 \___/ """,
    'V': r"""
        
\      /
 \    / 
  \  /  
   \/   """,
    'W': r"""
         
|   |   |
|   |   |
\  / \  /
 \/   \/ """,
    'X': """
    
\\  /
 \\/ 
 /\\ 
/  \\""",
    'Y': r"""
     
\   /
 \ / 
  |  
  |  """,
    'Z': """
____
   /
  / 
 /  
/___""",
    '!': """
   
 ||
 ||
 ||
 ..""",
    '.': """
   
   
   
   
 \x1b[4m-\x1b[0m """,
    '?': r"""
 __ 
/  \
   /
  | 
  . """,
    '1': """
   
/| 
 | 
 | 
_|_""",
    '2': """
 ___ 
|   |
   / 
  /  
 /___""",
    '3': r"""
 __  
/   \
  __/
    \
\__ /""",
    '4': """
  __
 /  |
/___|
    |
    |""",
}
blank = ['      '] * 5
blankWidth = len(blank[0])
letters = dict((key, block.split('\n')[1:]) for key, block in letters.items())
letterWidths = dict(
    (letter, len(block[1])) for letter, block in letters.items()
)


def blockprint(string):
    width, height = get_terminal_size()

    string = string.upper()
    words = string.split(' ')

    lineWidth = blockHeight = 0
    currentRow = 1
    rows = ['']

    for word in words:
        wordWidth = 0
        if len(rows[0]):
            word = ' ' + word
        for letter, index in zip(word, range(len(word))):
            wordWidth += letterWidths.get(letter, blankWidth)
            if wordWidth - blankWidth > width:
                word = word[:index]
                break
        if lineWidth + wordWidth > width:
            lineWidth = wordWidth - blankWidth
            word = word[1:]
            currentRow += 1
            rows.append('')
            blockHeight += 5
        else:
            lineWidth += wordWidth
        # words[word] = currentRow
        rows[currentRow - 1] += word

    # print(dumps(rows, indent=2))
    # print(rows)

    for row in rows:
        for charrow in range(5):
            for letter in row:
                print(letters.get(letter, blank)[charrow], end='')
            print()


if __name__ == '__main__':
    # for letter in letters.values():
    #   print('\n'.join(letter))
    blockprint(' '.join(sys.argv[1:]))
