from mando import command, main, arg


@command
@arg("spam", "--spam", "-s")
def ex(foo, b=None, spam=None):
    """Nothing interesting.

    :param foo: Bla bla.
    :param b: A little flag.
    :param spam: Spam spam spam spam."""

    print((foo, b, spam))


if __name__ == "__main__":
    main()
