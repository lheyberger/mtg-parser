#!/usr/bin/env python

from urllib.parse import urlparse


__all__ = ['HttpClientFacade']


class HttpClientFacade:

    def __init__(self, default_client):
        self._default_client = default_client
        self._overrides = {}

    def set_override(self, domain: str, client):
        self._overrides[domain] = client

    def get(self, url, *args, **kwargs):
        domain = urlparse(url).netloc
        client = self._get_client(domain)
        return client.get(url, *args, **kwargs)

    def _get_client(self, subdomain: str):
        for domain, client in self._overrides.items():
            if self._is_subdomain(subdomain, domain):
                return client
        return self._default_client

    @classmethod
    def _is_subdomain(cls, subdomain: str, domain: str) -> bool:
        subdomain = subdomain.lower().strip('.')
        domain = domain.lower().strip('.')
        return subdomain == domain or subdomain.endswith('.' + domain)

