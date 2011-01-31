#!/usr/bin/python

import os
import sys
import re

r = re.compile("(?P<left>\# Copyright \(C\) )(?P<years>(\d\d\d\d,\s)*(\d\d\d\d))(?P<right>\s+Tom Cato Amundsen)")
def do_file(filename):
    f = file(filename, 'r')
    s = f.read()
    f.close()
    m = r.search(s)
    def func(r):
        years = r.group('years')
        if '2008' not in years:
            years ="%s, 2008" % years
        return r.group('left') + years + r.group('right')
    s2 = r.sub(func, s)
    if s2 != s:
        f = file(filename, 'w')
        f.write(s2)
        f.close()

def motto(filename):
    f = file(filename, 'r')
    s = f.read()
    f.close()
    s2 = s.replace('ear trai'+'ning for GNOME', 'free ear training software')
    if s2 != s:
        f = file(filename, 'w')
        f.write(s2)
        f.close()


for root, dirs, files in os.walk("."):
    for f in files:
        if f.endswith(".py") or f == 'Makefile':
            do_file(os.path.join(root, f))
            #motto(os.path.join(root, f))
