#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json


def _to_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'))


def assert_objects_are_equal(result, expected):
    assert _to_json(result) == _to_json(expected)


def mock_response(requests_mock, pattern, response, basedir='tests/mocks'):
    if response:
        matcher = re.compile(pattern)
        with open(os.path.join(basedir, response), 'r') as file:
            requests_mock.get(matcher, text=file.read())
