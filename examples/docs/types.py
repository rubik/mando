from mando import command, main


@command
def pow(a, b, mod=None):
    '''Mimic Python's pow() function.

    :param a <float>: The base.
    :param b <float>: The exponent.
    :param -m, --mod <int>: Modulus.'''

    if mod is not None:
        print((a ** b) % mod)
    else:
        print(a ** b)


if __name__ == '__main__':
    main()
