#!/usr/bin/env python

import pytest

import mtg_parser

from .utils import assert_objects_are_equal


@pytest.mark.parametrize(('string', 'expected'), [
    # comment marker: //
    ("// test", { "comment": "test"}),
    ("//test", { "comment": "test"}),
    ("   // test", { "comment": "test"}),
    ("// test   ", { "comment": "test"}),
    ("//    test", { "comment": "test"}),
    # comment marker: #
    ("# test", { "comment": "test"}),
    ("#test", { "comment": "test"}),
    ("   # test", { "comment": "test"}),
    ("# test   ", { "comment": "test"}),
    ("#    test", { "comment": "test"}),
    # comment marker: //!
    ("//! test", { "comment": "test"}),
    ("//!test", { "comment": "test"}),
    ("   //! test", { "comment": "test"}),
    ("//! test   ", { "comment": "test"}),
    ("//!    test", { "comment": "test"}),
])
def test_comment_markers(string: str, expected: dict[str, str]):
    result = mtg_parser.parse_line(string)

    assert_objects_are_equal(result, expected)


@pytest.mark.parametrize(('string', 'expected'), [
    ("// word1 word2 word3", { "comment": "word1 word2 word3"}),
    ("// word1  word2  word3", { "comment": "word1  word2  word3"}),
    ("// WORD1  WORD2  WORD3", { "comment": "WORD1  WORD2  WORD3"}),
])
def test_comment_content(string: str, expected: dict[str, str]):
    result = mtg_parser.parse_line(string)

    assert_objects_are_equal(result, expected)


@pytest.mark.parametrize(("string", "expected"), [
    (
        "1 Gitaxian Probe",
        {
            "quantity": "1",
            "card_name": "Gitaxian Probe",
        },
    ),
    (
        "1 Barkchannel Pathway // Tidechannel Pathway",
        {
            "quantity": "1",
            "card_name": "Barkchannel Pathway // Tidechannel Pathway",
        },
    ),
    (
        "1 Lim-Dûl's Vault",
        {
            "quantity": "1",
            "card_name": "Lim-Dûl's Vault",
        },
    ),
    (
        "1 +2 Mace",
        {
            "quantity": "1",
            "card_name": "+2 Mace",
        },
    ),
])
def test_quantity_name(string: str, expected: dict[str, str]):
    result = mtg_parser.parse_line(string)

    assert_objects_are_equal(result, expected)


@pytest.mark.parametrize(("string", "expected"), [
    (
        "1 Gitaxian Probe (PLST)",
        {
            "quantity": "1",
            "card_name": "Gitaxian Probe",
            "extension": "PLST",
        },
    ),
    (
        "1 Barkchannel Pathway // Tidechannel Pathway (PKHM)",
        {
            "quantity": "1",
            "card_name": "Barkchannel Pathway // Tidechannel Pathway",
            "extension": "PKHM",
        },
    ),
    (
        "1 Lim-Dûl's Vault (C13)",
        {
            "quantity": "1",
            "card_name": "Lim-Dûl's Vault",
            "extension": "C13",
        },
    ),
    (
        "1 +2 Mace (AFR)",
        {
            "quantity": "1",
            "card_name": "+2 Mace",
            "extension": "AFR",
        },
    ),
])
def test_quantity_name_extension(string: str, expected: dict[str, str]):
    result = mtg_parser.parse_line(string)

    assert_objects_are_equal(result, expected)


@pytest.mark.parametrize(("string", "expected"), [
    (
        "1 Gitaxian Probe (PLST) NPH-35",
        {
            "quantity": "1",
            "card_name": "Gitaxian Probe",
            "extension": "PLST",
            "collector_number": "NPH-35",
        },
    ),
    (
        "1 Barkchannel Pathway // Tidechannel Pathway (PKHM) 251s",
        {
            "quantity": "1",
            "card_name": "Barkchannel Pathway // Tidechannel Pathway",
            "extension": "PKHM",
            "collector_number": "251s",
        },
    ),
    (
        "1 Lim-Dûl's Vault (C13) 197",
        {
            "quantity": "1",
            "card_name": "Lim-Dûl's Vault",
            "extension": "C13",
            "collector_number": "197",
        },
    ),
    (
        "1 +2 Mace (AFR) 1",
        {
            "quantity": "1",
            "card_name": "+2 Mace",
            "extension": "AFR",
            "collector_number": "1",
        },
    ),
])
def test_quantity_name_extension_collector_number(string: str, expected: dict[str, str]):
    result = mtg_parser.parse_line(string)

    assert_objects_are_equal(result, expected)


@pytest.mark.parametrize(("string", "expected"), [
    (
        "1 Gitaxian Probe (PLST) NPH-35 #interaction #!free spell",
        {
            "quantity": "1",
            "card_name": "Gitaxian Probe",
            "extension": "PLST",
            "collector_number": "NPH-35",
            "tags": [ "interaction", "free spell" ],
        },
    ),
    (
        "1 Barkchannel Pathway // Tidechannel Pathway (PKHM) 251s #fixing #!modal",
        {
            "quantity": "1",
            "card_name": "Barkchannel Pathway // Tidechannel Pathway",
            "extension": "PKHM",
            "collector_number": "251s",
            "tags": [ "fixing", "modal" ],
        },
    ),
    (
        "1 Lim-Dûl's Vault (C13) 197 #!tutor #card advantage",
        {
            "quantity": "1",
            "card_name": "Lim-Dûl's Vault",
            "extension": "C13",
            "collector_number": "197",
            "tags": [ "tutor", "card advantage" ],
        },
    ),
    (
        "1 +2 Mace (AFR) 1 #boost #equipment",
        {
            "quantity": "1",
            "card_name": "+2 Mace",
            "extension": "AFR",
            "collector_number": "1",
            "tags": [ "boost", "equipment" ],
        },
    ),
])
def test_quantity_name_extension_collector_number_tags(string: str, expected: dict[str, str]):
    result = mtg_parser.parse_line(string)

    assert_objects_are_equal(result, expected)
