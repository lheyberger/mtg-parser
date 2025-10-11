#!/usr/bin/env python
# ruff: noqa: E501

import cloudscraper
import httpx
import os
import pytest
import zlib
import pickle
from urllib.parse import urlparse
from pathlib import Path
from mtg_parser.http_client import HttpClientFacade
from .utils import _to_json


@pytest.fixture
def http_client_facade():
    return create_http_client_facade()


def create_http_client_facade():
    facade = TestsHttpClientFacade(httpx.Client(timeout=10.0))
    facade.set_override('aetherhub.com', cloudscraper.create_scraper())
    facade.set_override('moxfield.com', httpx.Client(
        timeout=10.0,
        headers={'User-Agent': os.getenv('MOXFIELD_USER_AGENT')},
    ))
    return facade



class TestsHttpClientFacade(HttpClientFacade):

    def __init__(self, default_client, mocks_dir:Path=None, read_mocks:bool=False, write_mocks:bool=False):
        super().__init__(default_client)
        self._mocks_dir = mocks_dir
        self._read_mocks = read_mocks
        self._write_mocks = write_mocks


    def read_mocks_from(self,mocks_dir:Path):
        self._mocks_dir = mocks_dir
        self._read_mocks = True
        self._write_mocks = False


    def write_mocks_to(self,mocks_dir:Path):
        self._mocks_dir = mocks_dir
        self._read_mocks = False
        self._write_mocks = True


    def get(self, url, *args, **kwargs):

        if self._read_mocks:
            key = self._query_key(url, *args, **kwargs)
            with (self._mocks_dir / key).open('rb') as file:
                return pickle.load(file)

        result = super().get(url, *args, **kwargs)

        if self._write_mocks:
            key = self._query_key(url, *args, **kwargs)
            with (self._mocks_dir / key).open('wb') as file:
                pickle.dump(result, file, pickle.HIGHEST_PROTOCOL)

        return result


    @classmethod
    def _query_key(cls, url, *args, **kwargs):
        key_info = _to_json({
            'url': url,
            'args': sorted(args),
            'kwargs': dict(sorted(kwargs.items())),
        })
        domain = urlparse(url).netloc.replace('.', '_')
        key_hash = hex(zlib.crc32(key_info.encode()))[2:]
        return f"{domain}_{key_hash}"
