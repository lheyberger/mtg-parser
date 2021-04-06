#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mtg_parser import diff


def test_diff():
    decklist1 = """
        1 Brainstorm
        1 Portent
        1 Ponder
    """

    decklist2 = """
        1 Portent
        1 Ponder
        1 Opt
    """

    result = diff(decklist1, decklist2)

    for key, value in result.items():
        assert value and all(value)
