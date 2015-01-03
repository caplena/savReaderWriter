#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import datetime
import tempfile
import os
from math import isnan
import numpy as np
import numpy.testing
import sys; sys.path.insert(0, "/home/antonia/Desktop/savreaderwriter")
from savReaderWriter import *
from savReaderNp import *

class Test_SavReaderNp(unittest.TestCase):

    def setUp(self):
        self.filename = "./test_data/Employee data.sav"
        self.nfilename = "./test_data/all_numeric.sav"

    def test_getitem_indexing(self):
        self.npreader = SavReaderNp(self.filename)
        actual = self.npreader[0].tolist()
        desired = [(1.0, b'm', datetime.datetime(1952, 2, 3, 0, 0), 15.0, 
                    3.0, 57000.0, 27000.0, 98.0, 144.0, 0.0)]
        self.assertEqual(actual, desired)

    def test_getitem_indexing_IndexError(self):
        self.npreader = SavReaderNp(self.filename)
        with self.assertRaises(IndexError):
            self.npreader[474]

    def test_getitem_indexing_raw(self):
        self.npreader = SavReaderNp(self.filename, rawMode=True)
        actual = self.npreader[0].tolist()
        desired = [(1.0, b'm       ', 11654150400.0, 15.0, 
                    3.0, 57000.0, 27000.0, 98.0, 144.0, 0.0)]
        self.assertEqual(actual, desired)

    def test_getitem_slicing(self):
        self.npreader = SavReaderNp(self.filename)
        actual = self.npreader[0:2].tolist()
        desired = \
        [(1.0, b'm', datetime.datetime(1952, 2, 3, 0, 0), 15.0, 
          3.0, 57000.0, 27000.0, 98.0, 144.0, 0.0), 
         (2.0, b'm', datetime.datetime(1958, 5, 23, 0, 0), 16.0, 
          1.0, 40200.0, 18750.0, 98.0, 36.0, 0.0)]
        self.assertEqual(actual, desired)

    def test_getitem_indexing_IndexError(self):
        self.npreader = SavReaderNp(self.filename)
        self.assertEqual(self.npreader[475:666].tolist(), []) 

    def test_getitem_striding(self):
        self.npreader = SavReaderNp(self.filename)
        actual = self.npreader[3::-1].tolist()
        desired = \
        [(4.0, b'f', datetime.datetime(1947, 4, 15, 0, 0), 8.0, 
          1.0, 21900.0, 13200.0, 98.0, 190.0, 0.0), 
         (3.0, b'f', datetime.datetime(1929, 7, 26, 0, 0), 12.0, 
          1.0, 21450.0, 12000.0, 98.0, 381.0, 0.0), 
         (2.0, b'm', datetime.datetime(1958, 5, 23, 0, 0), 16.0, 
          1.0, 40200.0, 18750.0, 98.0, 36.0, 0.0), 
         (1.0, b'm', datetime.datetime(1952, 2, 3, 0, 0), 15.0, 
          3.0, 57000.0, 27000.0, 98.0, 144.0, 0.0)]
        self.assertEqual(actual, desired)

    # ---------------

    def test_to_recarray_inmemory(self):
        self.npreader = SavReaderNp(self.filename)
        actual = self.npreader.to_recarray()[:3]

        obj = \
        {'formats': ['<f4', 'S1', '<M8[us]', '<f4', '<f2',
                     '<f8', '<f8', '<f4', '<f8', '<f2'],
         'names': [u'id', u'gender', u'bdate', u'educ', u'jobcat',
                   u'salary', u'salbegin', u'jobtime', u'prevexp', 
                   u'minority'],
         'titles': [u'Employee Code', u'Gender', u'Date of Birth',
                    u'Educational Level (years)', u'Employment Category',
                    u'Current Salary', u'Beginning Salary', 
                    u'Months since Hire', u'Previous Experience (months)',
                    u'Minority Classification']}
        desired = np.array(\
        [(1.0, b'm', datetime.datetime(1952, 2, 3, 0, 0), 15.0, 
          3.0, 57000.0, 27000.0, 98.0, 144.0, 0.0),
         (2.0, b'm', datetime.datetime(1958, 5, 23, 0, 0), 16.0, 
          1.0, 40200.0, 18750.0, 98.0, 36.0, 0.0),
         (3.0, b'f', datetime.datetime(1929, 7, 26, 0, 0), 12.0, 
          1.0, 21450.0, 12000.0, 98.0, 381.0, 0.0)],
        dtype=np.dtype(obj))
        #numpy.testing.assert_allclose(actual, desired, rtol=1e-5)
        self.assertEqual(actual.tolist(), desired.tolist())
        self.assertEqual(actual.dtype, desired.dtype)

    def test_to_recarray_inmemory_raw(self):
        self.npreader = SavReaderNp(self.filename, rawMode=True)
        actual = self.npreader.to_recarray()[:3].tolist()
        desired = \
        [(1.0, b'm', 11654150400.0, 15.0, 3.0,
          57000.0, 27000.0, 98.0, 144.0, 0.0),
         (2.0, b'm', 11852956800.0, 16.0, 1.0, 
          40200.0, 18750.0, 98.0, 36.0, 0.0),
         (3.0, b'f', 10943337600.0, 12.0, 1.0, 
          21450.0, 12000.0, 98.0, 381.0, 0.0)]
        self.assertEqual(actual, desired)
  
    def test_to_recarray_memmap(self):
        self.npreader = SavReaderNp(self.filename)
        mmapfile = tempfile.mkstemp()[1]
        actual = self.npreader.to_recarray(mmapfile)[:3].tolist()
        desired = \
        [(1.0, b'm', datetime.datetime(1952, 2, 3, 0, 0), 15.0, 
          3.0, 57000.0, 27000.0, 98.0, 144.0, 0.0),
         (2.0, b'm', datetime.datetime(1958, 5, 23, 0, 0), 16.0, 
          1.0, 40200.0, 18750.0, 98.0, 36.0, 0.0),
         (3.0, b'f', datetime.datetime(1929, 7, 26, 0, 0), 12.0, 
          1.0, 21450.0, 12000.0, 98.0, 381.0, 0.0)]
        self.assertEqual(actual, desired)
        os.remove(mmapfile)

    def test_to_recarray_memmap_raw(self):
        self.npreader = SavReaderNp(self.filename, rawMode=True)
        mmapfile = tempfile.mkstemp()[1]
        actual = self.npreader.to_recarray(mmapfile)[:3].tolist()
        desired = \
        [(1.0, b'm', 11654150400.0, 15.0, 3.0,
          57000.0, 27000.0, 98.0, 144.0, 0.0),
         (2.0, b'm', 11852956800.0, 16.0, 1.0, 
          40200.0, 18750.0, 98.0, 36.0, 0.0),
         (3.0, b'f', 10943337600.0, 12.0, 1.0, 
          21450.0, 12000.0, 98.0, 381.0, 0.0)]
        self.assertEqual(actual, desired)
        os.remove(mmapfile)

    def test_getitem_then_iter(self):
        """check if cursor is rewound after __getitem__"""
        self.npreader = SavReaderNp(self.filename)
        self.npreader[5]
        actual = next(iter(self.npreader))
        desired = \
        (1.0, b'm', datetime.datetime(1952, 2, 3, 0, 0), 15.0, 
         3.0, 57000.0, 27000.0, 98.0, 144.0, 0.0)
        self.assertEqual(actual, desired)

    def test_to_ndarray(self):
        self.npreader = SavReaderNp(self.nfilename)
        actual = self.npreader.to_ndarray().tolist()[:5]
        desired = [[0.0, np.nan], [1.0, 1.0], [2.0, 4.0], 
                   [3.0, 9.0], [4.0, 16.0]]
        func = lambda a, d: isnan(a) and isnan(d) or a == d
        items = [func(a, d) for arec, drec in zip(actual, desired) 
                 for a, d in zip(arec, drec)]
        self.assertTrue(all(items))
      
    def tearDown(self):
        self.npreader.close()

if __name__ == "__main__":
    unittest.main()

