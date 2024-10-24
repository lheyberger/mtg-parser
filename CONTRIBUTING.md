# How to contribute to mtg-parser


## Getting started

This project uses `poetry`, please refer to [their website](https://python-poetry.org) on how to install it.

Then, clone the repository and run:

```shell
$ make install
```

## Run tests

For fast iteration, run (this only executes tests with mockups):
```shell
$ make test
```

For a full checkup (includes slow tests that don't use mock data):
```shell
$ make test-all
```


## Run linters

Check syntax on the main `src` directory:
```shell
$ make lint
```

Check syntax on `src` + `tests` directories:
```shell
$ make lint-all
```


## How to publish a new version

Start by updating the version number:
```shell
$ poetry version (premajor|preminor|prepatch|prerelease|major|minor|patch)
```

Build the release and publish it on test.pypi.org:
```shell
$ make release
$ make test-publish
```

Push the latest files on github and publish the release on pypi.org:
```shell
$ git ls-files | xargs grep -l `poetry version -s` | xargs git add
$ git commit -m "feat: new version mtg-deckstats v`poetry version -s`"
$ git push
$ make publish
```

## (Optional) Cleanup

Cleanup temporary files (including code coverage reports):
```shell
$ make clean
```

Cleanup temporary files + package files:
```shell
$ make distclean
```

Deletes workflow runs from Github actions that are older than 120 days:
```shell
$ make clean-old-runs
```


## Setting up Poetry + PyPI

### PyPI Test

Get token from https://test.pypi.org/manage/account/token/ and store it in a token file.
```shell
$ poetry config repositories.testpypi https://test.pypi.org/legacy/
$ poetry config pypi-token.testpypi `cat token`
$ poetry publish -r testpypi
```

### PyPI Production

Get token from https://pypi.org/manage/account/token/ and store it in a token file.
```shell
$ poetry config pypi-token.pypi `cat token`
$ poetry publish
```
