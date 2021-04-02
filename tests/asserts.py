#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


def _to_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'))


def assert_objects_are_equal(result, expected):
    assert _to_json(result) == _to_json(expected)
