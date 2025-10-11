#!/usr/bin/env python

import pytest
from unittest.mock import Mock
from mtg_parser import HttpClientFacade


@pytest.mark.parametrize("url", [
    "https://example.com/deck/123",
    "https://api.example.com/deck/123",
])
def test_get_uses_default_client(url):
    default_client = Mock()
    facade = HttpClientFacade(default_client)

    facade.get(url)

    default_client.get.assert_called_once_with(url)


@pytest.mark.parametrize(("domain", "url"), [
    ("example.com", "https://example.com/deck/123"),
    ("example.com", "https://api.example.com/deck/123"),
    ("api.example.com", "https://api.example.com/deck/123"),
])
def test_get_uses_override_client(domain, url):
    default_client = Mock()
    override_client = Mock()
    facade = HttpClientFacade(default_client)
    facade.set_override(domain, override_client)

    facade.get(url)

    override_client.get.assert_called_once_with(url)
    default_client.get.assert_not_called()


@pytest.mark.parametrize(("domain", "url"), [
    ("example.com", "https://different.com/deck/123"),
    ("example.com", "https://test-example.com/deck/123"),
])
def test_get_uses_default_client_for_different_domain(domain, url):
    default_client = Mock()
    override_client = Mock()
    facade = HttpClientFacade(default_client)
    facade.set_override(domain, override_client)

    facade.get(url)

    default_client.get.assert_called_once_with(url)
    override_client.get.assert_not_called()


def test_multiple_overrides():
    default_client = Mock()
    override_client_1 = Mock()
    override_client_2 = Mock()
    facade = HttpClientFacade(default_client)
    facade.set_override("override.client1.com", override_client_1)
    facade.set_override("override.client2.com", override_client_2)

    facade.get("https://example.com/deck/123")
    facade.get("https://override.client1.com/deck/123")
    facade.get("https://override.client2.com/deck/123")

    default_client.get.assert_called_once_with("https://example.com/deck/123")
    override_client_1.get.assert_called_once_with("https://override.client1.com/deck/123")
    override_client_2.get.assert_called_once_with("https://override.client2.com/deck/123")


@pytest.mark.parametrize(("url", "args", "kwargs"), [
    ("https://example.com/deck/123", ("arg1", "arg2"), {"timeout": 30, "headers": {"User-Agent": "test"}}),
    ("https://api.example.com/deck/123", ("arg1", "arg2"), {"timeout": 30, "headers": {"User-Agent": "test"}}),
])
def test_get_passes_args_and_kwargs(url, args, kwargs):
    default_client = Mock()
    facade = HttpClientFacade(default_client)

    facade.get(url, *args, **kwargs)

    default_client.get.assert_called_once_with(url, *args, **kwargs)
