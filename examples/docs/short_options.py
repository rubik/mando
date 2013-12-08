from mando import command, main


@command
def ex(foo, b=None, spam=None):
    '''Nothing interesting.

    :param foo: Bla bla.
    :param -b: A little flag.
    :param -s, --spam: Spam spam spam spam.'''

    print(foo, b, spam)

if __name__ == '__main__':
    main()
