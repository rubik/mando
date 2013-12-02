from mando import command, main

@command
def echo(text, capitalyze=False):
    '''Echo the given text.'''
    if capitalyze:
        text = text.upper()
    print text


if __name__ == '__main__':
    main()
