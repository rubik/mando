from mando import command, main


@command
def cmd(foo, bar):
    '''Here stands the help.

    And here the description of this useless command.

    :param foo: Well, the first arg.
    :param bar: Obviously the second arg. Nonsense.'''

    print(foo, bar)


if __name__ == '__main__':
    main()
