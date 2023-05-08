def forceLength(prompt, length):
    response = input(prompt)
    while len(response) != length:
        response = input(
            'Expected string with ' + str(length) + ' characters: '
        )
    return response


def greenToWord(green):
    return ''.join(map(lambda ele: ele if ele else '_', green))
