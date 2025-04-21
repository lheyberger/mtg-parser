#!/usr/bin/make -f

SRC_DIR = src
TESTS_DIR = tests
DIST_DIR = dist
TMP_DIR = tmp
COVERAGE_DIR = htmlcov

##
# ALL
##
all: install test build clean

.PHONY: all


##
# RELEASE
##
release: update test-all lint-all distclean build clean

.PHONY: all


##
# INSTALL
##
install:
	poetry install --sync

update:
	poetry update

.PHONY: install update


##
# LINT & TESTS
##
lint:
	poetry run ruff check ${SRC_DIR}

lint-all: lint
	poetry run ruff check ${TESTS_DIR} || true

test:
	poetry run dotenv run coverage run -m pytest -m 'not slow'
	poetry run coverage report --fail-under=100

test-all:
	poetry run dotenv run coverage run -m pytest || \
	poetry run dotenv run coverage run -a -m pytest --last-failed --last-failed-no-failures none
	poetry run coverage report --fail-under=100

coverage:
	poetry run coverage html -d ${COVERAGE_DIR}
	open ${COVERAGE_DIR}/index.html

.PHONY: lint lint-all test test-all coverage


##
# BUILD
#
sync-version:
	git grep -l "__version__\s*=" ${SRC_DIR} | xargs -I {} \
	sed -i '' "s/^\s*__version__.*/__version__ = \'`poetry version -s`\'/" {}

build: sync-version
	poetry check
	poetry build
	poetry run check-wheel-contents ${DIST_DIR}

.PHONY: build sync-version


##
# PUBLISH
##
test-publish:
	poetry config repositories.testpypi https://test.pypi.org/legacy/
	poetry publish -r testpypi

publish:
	poetry publish
	gh release create -p "v`poetry version -s`" ./${DIST_DIR}/mtg_parser-* --generate-notes

.PHONY: test-publish publish


##
# CLEAN
##
define remove_dir
	find $(2) -type d -name $(1) -print0 | xargs -0 -I {} rm -rf '{}'
endef

clean-old-runs:
	@echo 'Cleaning runs older than 120 days'
	@gh run list --json startedAt,databaseId --limit 100 \
	| jq '.[] | select(now - (.startedAt | fromdateiso8601) > 10368000) | .databaseId' \
	| xargs -I {} gh run delete {}

clean-packages:
	$(call remove_dir,${DIST_DIR},.)

clean:
	poetry run coverage erase
	$(call remove_dir,${COVERAGE_DIR},.)
	$(call remove_dir,${TMP_DIR},.)
	$(call remove_dir,'__pycache__',.)
	$(call remove_dir,'.pytest_cache',.)
	$(call remove_dir,'.ruff_cache',.)
	$(call remove_dir,'*.egg-info',${SRC_DIR} ${TESTS_DIR})

distclean: clean clean-packages

.PHONY: clean-old-runs clean clean-packages distclean
