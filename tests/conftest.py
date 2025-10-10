#!/usr/bin/env python
# ruff: noqa: E501

import cloudscraper
import httpx
import os
import pytest
import re
import respx
from pathlib import Path
from functools import partial
from mtg_parser.utils import HttpClientFacade


@pytest.fixture
def respx_mock():
    # Implementing my own respx_mock instead of relying on the fixture provided by respx
    # See: https://github.com/lundberg/respx/issues/277#issuecomment-2507693706

    def _mock_response(respx_mock, pattern, response, basedir='tests/mocks'):
        if not response:
            return
        with (Path(basedir) / response).open(encoding="utf-8") as file:
            body = file.read()
        matcher = re.compile(pattern)
        respx_mock.get(matcher).respond(status_code=200, text=body)

    with respx.mock(using='httpx', assert_all_called=False) as mock:
        yield partial(_mock_response, mock)


@pytest.fixture
def http_client_facade():
    return create_http_client_facade()


def create_http_client_facade():
    facade = HttpClientFacade(httpx.Client(timeout=10.0))
    facade.set_override('aetherhub.com', cloudscraper.create_scraper())
    facade.set_override('moxfield.com', httpx.Client(
        timeout=10.0,
        headers={'User-Agent': os.getenv('MOXFIELD_USER_AGENT')},
    ))
    return facade
