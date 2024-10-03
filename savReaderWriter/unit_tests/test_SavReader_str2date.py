#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import savReaderWriter as rw

class Test_spss2strDate(unittest.TestCase):

    def setUp(self):
        self.savFileName = 'test_data/test_dates.sav'
        self.reader = rw.SavReader(self.savFileName)
        self.convert = self.reader.spss2strDate

    def test_time(self):
        got = self.convert(1, "%H:%M:%S", None)
        self.assertEqual(b'00:00:01', got)

        got = self.convert(86399, "%H:%M:%S", None)
        self.assertEqual(b'23:59:59', got)

    def test_datetime(self):
        got = self.convert(11654150400.0, "%Y-%m-%d %H:%M:%S", None)
        self.assertEqual(b'1952-02-03 00:00:00', got)

        got = self.convert(11654150400.0, "%Y-%m-%d", None)
        self.assertEqual(b'1952-02-03', got)

        got = self.convert(11654150400.0, "%d-%m-%Y", None)
        self.assertEqual(b'03-02-1952', got)

    def tearDown(self):
        self.reader.close()

if __name__ == "__main__":
    unittest.main()
