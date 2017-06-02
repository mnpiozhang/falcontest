#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
from bisect import bisect
def grade(score, breakpoints=[60, 70, 80, 90], grades='FDCBA'):
    i = bisect(breakpoints, score)
    print i
    return grades[i]

print [grade(score) for score in [33, 99, 77, 70, 89, 90, 100]]
'''



a = "风卷残云"
print type(a)
b = a.unicode() 
print b
print type(b)