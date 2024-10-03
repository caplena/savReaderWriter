#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
## Read a file containg all the supported date formats
##############################################################################

import os
import sys
import functools
import locale
from tempfile import gettempdir
from os.path import join
from time import strftime, strptime
import pytest

from savReaderWriter import *

locale.setlocale(locale.LC_ALL, "")


# ----------------
# make sure the test passes in other locales too
stamp  = lambda v, fmt: strftime(fmt, strptime(v, '%Y-%m-%d')).encode()
wed1, august = stamp('2010-08-11', '%A'), stamp('2010-08-11', '%B')
wed2, january = stamp('1910-01-12', '%A'), stamp('1910-01-12', '%B')
desired_records = \
    [[b'2010-08-11 00:00:00', b'32 WK 2010', b'2010-08-11', b'3 Q 2010',
      b'2010-08-11', b'2010-08-11', b'156260 00:00:00', b'2010-08-11', august,
      august + b' 2010', b'00:00:00.000000', b'2010-08-11', wed1],
     [b'1910-01-12 00:00:00', b'02 WK 1910', b'1910-01-12', b'1 Q 1910',
      b'1910-01-12', b'1910-01-12', b'119524 00:00:00', b'1910-01-12', january,
      january + b' 1910', b'00:00:00.000000', b'1910-01-12', wed2],
     [None, None, None, None, None, None, None,
      None, None, None, None, None, None],
     [None, None, None, None, None, None, None,
      None, None, None, None, None, None]]


# ----------------
# NOTE: PSPP does not know how to display all of these formats.
# Example use of DTIME in SPSS:
# COMPUTE #a_day = 24 * 60 * 60.
# COMPUTE x = 10 * #a_day + TIME.HMS(12, 03, 00).
# FORMATS x (DTIME14).
# will display as 10 12:03:00



@pytest.fixture
def savFileName(tmp_path):
    """create a test file"""
    filepath = str(tmp_path / "test_dates.sav")
    varNames = [b'var_datetime', b'var_wkyr', b'var_date', b'var_qyr', b'var_edate',
                b'var_sdate', b'var_dtime', b'var_jdate', b'var_month', b'var_moyr',
                b'var_time', b'var_adate', b'var_wkday']
    varTypes = {v : 0 for v in varNames}
    spssfmts = [b'DATETIME40', b'WKYR10', b'DATE10', b'QYR10', b'EDATE10',
                b'SDATE10', b'DTIME10', b'JDATE10', b'MONTH10', b'MOYR10',
                b'TIME10', b'ADATE10', b'WKDAY10']
    formats = dict(zip(varNames, spssfmts))
    records = [[b'2010-08-11' for v in varNames],
               [b'1910-01-12' for v in varNames],
               [b'' for v in varNames],
               [None for v in varNames]]

    kwargs = dict(savFileName=filepath, varNames=varNames,
                  varTypes=varTypes, formats=formats)
    with SavWriter(**kwargs) as writer:
        for i, record in enumerate(records):
            for pos, value in enumerate(record):
                record[pos] = writer.spssDateTime(record[pos], "%Y-%m-%d")
            writer.writerow(record)

    yield filepath


def test_date_values(savFileName):
    data = SavReader(savFileName)
    with data:
        actual_records = data.all()
    for desired_record, actual_record in zip(desired_records, actual_records):
        for desired, actual in zip(desired_record, actual_record):
            yield compare_value, desired, actual


def test_dates_recodeSysmisTo(savFileName):
    """Test if recodeSysmisTo arg recodes missing date value"""
    data = SavReader(savFileName, recodeSysmisTo=999)
    with data:
        actual_records = data.all()
    desired_records_ = desired_records[:2] + 2 * [13 * [999]]
    for desired_record, actual_record in zip(desired_records_, actual_records):
        for desired, actual in zip(desired_record, actual_record):
            yield compare_value, desired, actual

def compare_value(desired, actual):
    assert desired == actual


# ----------------
# issue #54 fractional datetimes trigger error which must
# be ignored, e.g. DATETIME11.1
def test_fractional_datetime():
    savFileName = join(gettempdir(), "test_dates_issue54_1.sav")
    args = (savFileName, [b'datetime'], {b'datetime': 0})
    with SavWriter(*args, formats={b'datetime': b"datetime22.1"}) as writer:
        before = [writer.spssDateTime(b"1952-02-03", "%Y-%m-%d")]
        writer.writerow(before)
    with SavReader(savFileName) as reader:
        after = reader.all(False)[0]
    assert before != after, "before: %s | after: %s" % (before, after)

def test_fractional_dtime():
    savFileName = join(gettempdir(), "test_dates_issue54_2.sav")
    args = (savFileName, [b'dtime'], {b'dtime': 0})
    with SavWriter(*args, formats={b'dtime': b"dtime13.1"}) as writer:
        before = [writer.spssDateTime(b"1952-02-03", "%Y-%m-%d")]
        writer.writerow(before)
    with SavReader(savFileName, rawMode=True) as reader:
        after = reader.all(False)[0]
    assert before == after, "before: %s | after: %s" % (before, after)
    with SavReader(savFileName) as reader:
        after = reader.all(False)[0]
    assert after == [b'134886 00:00:00'], after

def test_fractional_time():
    savFileName = join(gettempdir(), "test_dates_issue54_3.sav")
    args = (savFileName, [b'time'], {b'time': 0})
    with SavWriter(*args, formats={b'time': b"time10.1"}) as writer:
        before = [writer.spssDateTime(b"23:59:01", "%H:%M:%S")]
        writer.writerow(before)
    with SavReader(savFileName, rawMode=True) as reader:
        after = reader.all(False)[0]
    assert before == after, "before: %s | after: %s" % (before, after)
    with SavReader(savFileName) as reader:
        after = reader.all(False)[0]
    assert after == [b'23:59:01.000000'], after

def test_fractional_datetime_wrong():
    savFileName = join(gettempdir(), "test_dates_issue54_4.sav")
    args = (savFileName, [b'datetime'], {b'datetime': 0})
    with pytest.raises(ValueError) as error:
        with SavWriter(*args, formats={b'datetime': b"datime17.1_WRONG"}) as writer:
            before = [writer.spssDateTime(b"1952-02-03", "%Y-%m-%d")]
            writer.writerow(before)
        assert "Unknown format" in str(error.exception), str(error.exception)
