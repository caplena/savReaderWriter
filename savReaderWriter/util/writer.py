#!/usr/bin/env python
# -*- coding: utf-8 -*-

from savReaderWriter import *

try:
    range
except NameError:
    range = range

varNames = list("abcdefghij")
varTypes = dict(zip(varNames, [0 for i in range(10)]))
with SavWriter("big.sav", varNames, varTypes) as writer:
    record = [0 for i in range(10)]
    for i in range(10 ** 6):
        writer.writerow(record)
