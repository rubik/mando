from mando import command, main, arg


@command
@arg("mod", "-m", "--mod")
def pow(a, b, mod=None):
    """Mimic Python's pow() function.

    :param float a: The base.
    :param float b: The exponent.
    :param int mod: Modulus."""

    if mod is not None:
        print((a ** b) % mod)
    else:
        print(a ** b)


if __name__ == "__main__":
    main()
