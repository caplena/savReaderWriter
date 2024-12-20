#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from savReaderWriter import *

# See also issue #26
# TODO: add test data with 'Extended' multiple response groups.
# I have no idea how to define these
# Email syntax or datafile to "@".join(["fomcl", "yahoo.%s" % ".com"])

savFileName = "test_data/spssio_test.sav"
desired = \
{b'V': {b'countedValue': b'1',     # dichotomy (MDGROUP)
        b'label': b'',
        b'setType': b'D',
        b'varNames': [b'V1', b'V2', b'V3']},
 b'ages': {b'label': b'the ages',  # categorical (MCGROUP)
           b'setType': b'C',
           b'varNames': [b'Age', b'AGE2', b'AGE3']},
 b'incomes': {b'label': b'three kinds of income',  # categorical (once more)
              b'setType': b'C',
              b'varNames': [b'Income1',
                            b'Income2',
                            b'Income3',
                            b'Age',
                            b'AGE2',
                            b'AGE3']}}

udesired = \
{'V': {'countedValue': '1',
        'label': '',
        'setType': 'D',
        'varNames': ['V1', 'V2', 'V3']},
 'ages': {'label': 'the ages',
           'setType': 'C',
           'varNames': ['Age', 'AGE2', 'AGE3']},
 'incomes': {'label': 'three kinds of income',
              'setType': 'C',
              'varNames': ['Income1',
                            'Income2',
                            'Income3',
                            'Age',
                            'AGE2',
                            'AGE3']}}

class Test_Mrsets(unittest.TestCase):

    """
    Read multiple response sets (dichotomy and categorical)
    """

    def setUp(self):
        self.maxDiff = None

    def test_multRespDefs(self):
        with SavHeaderReader(savFileName) as header:
            actual = header.multRespDefs
        self.assertEqual(desired, actual)

    def test_multRespDefs_unicode_mode(self):
        with SavHeaderReader(savFileName, ioUtf8=True) as header:
            uactual = header.multRespDefs
        # Python 3: returned as <map object> --> turn into list
        uactual["V"]["varNames"] = list(uactual["V"]["varNames"])
        uactual["ages"]["varNames"] = list(uactual["ages"]["varNames"])
        uactual["incomes"]["varNames"] = list(uactual["incomes"]["varNames"])
        self.assertEqual(udesired, uactual)

if __name__ == "__main__":
    unittest.main()

