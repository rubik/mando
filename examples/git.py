from mando import command, main


@command
def push(repository, all=False, dry_run=False, force=False, thin=False):
    '''Update remote refs along with associated objects.

    :param repository: Repository to push to.
    :param --all: Push all refs.
    :param -n, --dry-run: Dry run.
    :param -f, --force: Force updates.
    :param --thin: Use thin pack.'''

    print ('Pushing to {0}. All: {1}, dry run: {2}, force: {3}, thin: {4}'
           .format(repository, all, dry_run, force, thin))


if __name__ == '__main__':
    main()
