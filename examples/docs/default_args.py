from mando import command, main


@command
def po(a=2, b=3):
    print(a ** b)


if __name__ == '__main__':
    main()
