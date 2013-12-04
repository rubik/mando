# gnu.py
from mando import main, command, arg


@command
@arg('maxdepth', metavar='<levels>')
def find(path, pattern, maxdepth=None, P=False, D=None):
    '''Mock some features of the GNU find command.

    This is not at all a complete program, but a simple representation to
    showcase mando's coolest features.

    :param path: The starting path.
    :param pattern: The pattern to look for.
    :param -d, --maxdepth <int>: Descend at most <levels>.
    :param -P: Do not follow symlinks.
    :param -D <debug-opt>: Debug option, print diagnostic information.'''

    if maxdepth is not None and maxdepth < 2:
        print('If you choose maxdepth, at least set it > 1')
    if P:
        print('Following symlinks...')
    print('Debug options: {0}'.format(D))
    print('Starting search with pattern: {0}'.format(pattern))
    print('No file found!')


if __name__ == '__main__':
    main()
