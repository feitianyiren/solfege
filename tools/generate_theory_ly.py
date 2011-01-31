﻿#!/usr/bin/python
# vim: set fileencoding=utf-8:
# Solfege - free ear training software
# Copyright (C) 2008, 2009, 2010  Tom Cato Amundsen
# License is GPL, see file COPYING

from __future__ import division

import codecs
import gettext
import optparse
import os
import sys
import time

def nop(s): return s

import __builtin__
__builtin__.__dict__['_'] = nop

sys.path.insert(0, ".")
from solfege.i18n import _i

opt = optparse.OptionParser()
opt.add_option('-f', dest='outfile')
opt.add_option('--png-targets', action='store_true', dest='png_targets')
opt.add_option('--ly-targets', action='store_true', dest='ly_targets')
opt.add_option('--ly-C-targets', action='store_true', dest='ly_C_targets')
opt.add_option('--all', action='store_true', dest='regen_all')
options, args = opt.parse_args()

ly_files = (
    'theory-intervals-1.ly',
    'theory-intervals-seconds.ly',
    'theory-intervals-thirds.ly',
    'theory-intervals-fourths.ly',
    'theory-intervals-fifths.ly',
    'theory-intervals-sixths.ly',
    'theory-intervals-sevenths.ly',
    'inverting-intervals.ly',
)

def get_data():
    return {
      "theory-intervals-1.ly":
    ur"""
    \version "2.8.1"
    \include "scale-common.ly"
    \score {
     \new Staff\relative c'{ \cadenzaOn <c c>1 <c d> <c e> <c f> <c g'> <c a'> <c b'> <c c'> <c d'> <c e'> }
     \addlyrics{ %s %s %s %s %s %s %s %s %s %s }
     \addlyrics{ "1" "2" "3" "4" "5" "6" "7" "8" "9" "10" }
    }
    """ %
     (_i("interval|Unison"), _i("interval|Second"), _i("interval|Third"),
      _i("interval|Fourth"), _i("interval|Fifth"), _i("interval|Sixth"),
      _i("interval|Seventh"), _i("interval|Octave"),
      _i("interval|Ninth"), _i("interval|Tenth")),

      "theory-intervals-seconds.ly":
    ur"""
    \version "2.7.40"
    \include "scale-common.ly"
    \score {
     \new Staff\relative c'{ \cadenzaOn
        <c d>1 <d e> <e f> <f g> <g a> <a b> <b c>}
     \addlyrics{ %(a)s %(a)s %(i)s %(a)s %(a)s %(a)s %(i)s }
    }
    """ % {'a': _i('interval|Major'), 'i': _i('interval|Minor')},

        "theory-intervals-thirds.ly":
    ur"""
    \version "2.7.40"
    \include "scale-common.ly"
    \score {
     \new Staff\relative c'{ \cadenzaOn
        <c e>1 <d f> <e g> <f a> <g b> <a c> <b d>}
     \addlyrics{ %(a)s %(i)s %(i)s %(a)s %(a)s %(i)s %(i)s }
    }
    """ % {'a': _i("interval|Major"), 'i': _i("interval|Minor")},

        "theory-intervals-fourths.ly":
    ur""" 
    \version "2.7.40"
    \include "scale-common.ly"
    \score {
     \new Staff\relative c'{ \cadenzaOn
        <c f>1 <d g> <e a> <f b> <g c> <a d> <b e>}
     \addlyrics{ %(p)s %(p)s %(p)s %(a)s %(p)s %(p)s %(p)s }
    }
    """ % {'p': _i('interval|Perfect'), 'a': _i('interval|Augmented')},

        "theory-intervals-fifths.ly":
    ur"""
    \version "2.7.40"
    \include "scale-common.ly"
    \score {
     \new Staff\relative c'{ \cadenzaOn
        <c g'>1 <d a'> <e b'> <f c'> <g d'> <a e'> <b f'>}
     \addlyrics{ %(p)s %(p)s %(p)s %(p)s %(p)s %(p)s %(d)s }
    }
    """ % {'p': _i('interval|Perfect'), 'd': _i('interval|Diminished')},

        "theory-intervals-sixths.ly":
    ur"""
    \version "2.7.40"
    \include "scale-common.ly"
    \score {
     \new Staff\relative c'{ \cadenzaOn
        <c a'>1 <d b'> <e c'> <f d'> <g e'> <a f'> <b g'>}
     \addlyrics{ %(a)s %(a)s %(i)s %(a)s %(a)s %(i)s %(i)s }
    }
    """ % {'a': _i("interval|Major"), 'i': _i("interval|Minor")},

        "theory-intervals-sevenths.ly":
    ur"""
    \version "2.7.40"
    \include "scale-common.ly"
    \score {
     \new Staff\relative c'{ \cadenzaOn
        <c b'>1 <d c'> <e d'> <f e'> <g f'> <a g'> <b a'>}
     \addlyrics{ %(a)s %(i)s %(i)s %(a)s %(i)s %(i)s %(i)s }
    }
    """ % {'a': _i("interval|Major"), 'i': _i("interval|Minor")},

        "inverting-intervals.ly":
    ur"""
    \version "2.7.40"
    \include "scale-common.ly"
    \score {
    <<
     \new Staff\relative c'{ <d fis>1  <fis d'> 
     <c bes'> <bes' c> }
     \new Lyrics\lyricmode {
        \override LyricText #'self-alignment-X = #-0.9
        "%s" "%s" "%s" "%s" } 
    >>
    }
    """ % (_("Major Third"), _("Minor Sixth"), _("Minor Seventh"),
          _("Major Second")),
    }


def write_if_changed(filename, contents):
    if not os.path.exists(os.path.split(filename)[0]):
        os.makedirs(os.path.split(filename)[0])
    try:
        infile = codecs.open(filename, 'r', 'utf-8')
        old_contents = infile.read()
        infile.close()
        equal = contents == old_contents
    except IOError:
        equal = False
    pngfilename = filename[:-2]+'png'
    if not equal:
        outfile = codecs.open(filename, 'w', 'utf-8')
        outfile.write(contents)
        outfile.close()
    else:
        now = time.time()
        os.utime(filename, (now - 1, now - 1))
        if os.path.exists(pngfilename):
            os.utime(pngfilename, (now, now))


def set_lang(lang):
    if lang == 'C':
        __builtin__.__dict__['_'] = nop
    else:
        g = gettext.GNUTranslations(open(os.path.join("po", "%s.mo" % lang), 'r'))
        __builtin__.__dict__['_'] = g.ugettext


languages = [fn for fn in os.listdir("help") if os.path.isdir(os.path.join("help", fn))]


if options.ly_targets:
    ret = []
    for lang in [x for x in os.listdir("help") if os.path.isdir(os.path.join("help", x))]:
        for fn in ly_files:
            ret.append(os.path.join("help", lang, "ly", fn))
    print " ".join(ret)
elif options.ly_C_targets:
    print " ".join([os.path.join("help", "C", "ly", x) for x in ly_files])
elif options.png_targets:
    ret = []
    for lang in [x for x in os.listdir("help") if os.path.isdir(os.path.join("help", x))]:
        for fn in ly_files:
            ret.append(os.path.join("help", lang, "ly", fn[:-2]+"png"))
    print " ".join(ret)
elif options.outfile:
    lang = options.outfile.split(os.sep)[1]
    fn = options.outfile.split(os.sep)[-1]
    set_lang(lang)
    if not os.path.exists(os.path.join("help", lang, 'ly')):
        os.makedirs(os.path.join("help", lang, 'ly'))
    contents = get_data()[fn]
    write_if_changed(options.outfile, contents)
elif options.regen_all:
    for lang in languages:
        set_lang(lang)
        for ly_file in ly_files:
            contents = get_data()[ly_file]
            filename = os.path.join("help", lang, "ly", ly_file)
            write_if_changed(filename, contents)
