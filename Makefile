#!/usr/bin/make -f
# -*- coding: utf-8 -*-

SRC_DIR = src
TESTS_DIR = tests
DIST_DIR = dist
TMP_DIR = tmp

##
# ALL
##
all: install test build clean

.PHONY: all


##
# INSTALL
##
install:
	poetry install --remove-untracked

update:
	poetry update

.PHONY: install update


##
# LINT & TESTS
##
lint:
	poetry run flake8 ${SRC_DIR}
	poetry run pylint ${SRC_DIR}

lint-all: lint
	poetry run flake8 ${TESTS_DIR} || true
	poetry run pylint ${TESTS_DIR} || true

test:
	poetry run coverage run -m pytest -rP -m 'not slow'
	poetry run coverage report --fail-under=100

test-all:
	poetry run coverage run -m pytest -rP
	poetry run coverage report --fail-under=100

.PHONY: lint lint-all test test-all


##
# BUILD
#
sync-version:
	sed -i '' "s/__version__.*/__version__ = \'`poetry version -s`\'/" `find ${SRC_DIR} -type f -print | xargs grep -l "__version__"` || true

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

.PHONY: test-publish


##
# CLEAN
##
define remove_dir
	find $(2) -type d -name $(1) -print0 | xargs -0 -I {} rm -rf '{}'
endef

clean-packages:
	$(call remove_dir,${DIST_DIR},.)

clean:
	poetry run coverage erase
	$(call remove_dir,${TMP_DIR},.)
	$(call remove_dir,'__pycache__',.)
	$(call remove_dir,'.pytest_cache',.)
	$(call remove_dir,'*.egg-info',${SRC_DIR} ${TESTS_DIR})

distclean: clean clean-packages

.PHONY: clean clean-packages distclean
