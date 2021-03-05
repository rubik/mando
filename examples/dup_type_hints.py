from mando import command, main

# Note: don't actually do this.
def double_int(n):
    return int(n) * 2


@command
def dup(string, times: double_int):
    """
    Duplicate text.

    :param string: The text to duplicate.
    :param times: How many times to duplicate.
    """
    print(string * times)


if __name__ == "__main__":
    main()
