#!/usr/bin/env python

import pytest
from unittest.mock import Mock
from mtg_parser import HttpClientFacade


@pytest.mark.parametrize("method", ["get", "post"])
@pytest.mark.parametrize("url", [
    ("https://example.com/deck/123" ),
    "https://api.example.com/deck/123",
])
def test_facade_uses_default_client(method, url):
    default_client = Mock()
    facade = HttpClientFacade(default_client)

    getattr(facade, method)(url)

    getattr(default_client, method).assert_called_once_with(url)


@pytest.mark.parametrize("method", ["get", "post"])
@pytest.mark.parametrize(("domain", "url"), [
    ("example.com", "https://example.com/deck/123"),
    ("example.com", "https://api.example.com/deck/123"),
    ("api.example.com", "https://api.example.com/deck/123"),
])
def test_facade_uses_override_client(method, domain, url):
    default_client = Mock()
    override_client = Mock()
    facade = HttpClientFacade(default_client)
    facade.set_override(domain, override_client)

    getattr(facade, method)(url)

    getattr(override_client, method).assert_called_once_with(url)
    getattr(default_client, method).assert_not_called()


@pytest.mark.parametrize("method", ["get", "post"])
@pytest.mark.parametrize(("domain", "url"), [
    ("example.com", "https://different.com/deck/123"),
    ("example.com", "https://test-example.com/deck/123"),
])
def test_facade_uses_default_client_for_different_domain(method, domain, url):
    default_client = Mock()
    override_client = Mock()
    facade = HttpClientFacade(default_client)
    facade.set_override(domain, override_client)

    getattr(facade, method)(url)

    getattr(default_client, method).assert_called_once_with(url)
    getattr(override_client, method).assert_not_called()


@pytest.mark.parametrize("method", ["get", "post"])
def test_multiple_overrides(method):
    default_client = Mock()
    override_client_1 = Mock()
    override_client_2 = Mock()
    facade = HttpClientFacade(default_client)
    facade.set_override("override.client1.com", override_client_1)
    facade.set_override("override.client2.com", override_client_2)

    getattr(facade, method)("https://example.com/deck/123")
    getattr(facade, method)("https://override.client1.com/deck/123")
    getattr(facade, method)("https://override.client2.com/deck/123")

    getattr(default_client, method).assert_called_once_with("https://example.com/deck/123")
    getattr(override_client_1, method).assert_called_once_with("https://override.client1.com/deck/123")
    getattr(override_client_2, method).assert_called_once_with("https://override.client2.com/deck/123")


@pytest.mark.parametrize("method", ["get", "post"])
@pytest.mark.parametrize(("url", "args", "kwargs"), [
    ("https://example.com/deck/123", ("arg1", "arg2"), {"timeout": 30, "headers": {"User-Agent": "test"}}),
    ("https://api.example.com/deck/123", ("arg1", "arg2"), {"timeout": 30, "headers": {"User-Agent": "test"}}),
])
def test_get_passes_args_and_kwargs(method, url, args, kwargs):
    default_client = Mock()
    facade = HttpClientFacade(default_client)

    getattr(facade, method)(url, *args, **kwargs)

    getattr(default_client, method).assert_called_once_with(url, *args, **kwargs)
