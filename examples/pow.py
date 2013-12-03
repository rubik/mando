from mando import main, command


@command
def pow(base, exp):
    '''Compute base ^ exp.

    :param base <int>: The base.
    :param exp <int>: The exponent.'''
    print base ** exp


if __name__ == '__main__':
    main()
