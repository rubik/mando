from mando import command, main, arg


@command
@arg("force", "--force", "-f")
@arg("dry_run", "--dry_run", "-n")
def push(repository, all=False, dry_run=False, force=False, thin=False):
    """Update remote refs along with associated objects.

    :param repository: Repository to push to.
    :param all: Push all refs.
    :param dry_run: Dry run.
    :param force: Force updates.
    :param thin: Use thin pack."""

    print(
        "Pushing to {0}. All: {1}, dry run: {2}, force: {3}, thin: {4}".format(
            repository, all, dry_run, force, thin
        )
    )


if __name__ == "__main__":
    main()
