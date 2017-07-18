# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest

from pgsmo.objects.sequence import Sequence
from tests.pgsmo_tests.node_test_base import NodeObjectTestBase


class TestSequence(NodeObjectTestBase, unittest.TestCase):
    NODE_ROW = {
        'name': 'rulename',
        'oid': 123
    }

    @property
    def class_for_test(self):
        return Sequence

    @property
    def basic_properties(self):
        return {}

    @property
    def collections(self):
        return []

    @property
    def node_query(self) -> dict:
        return TestSequence.NODE_ROW