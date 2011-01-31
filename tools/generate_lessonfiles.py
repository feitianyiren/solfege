#!/usr/bin/python
# Solfege - ear training for GNOME
# Copyright (C) 2007, 2008 Tom Cato Amundsen
# License is GPL, see file COPYING

from __future__ import division

import codecs
import sys
import os

# Need this to run under debuild, but not from the shell. Strange...
sys.path.insert(0, ".")
import solfege.i18n
solfege.i18n.setup(".")

import solfege.frontpage as fp
from solfege.mpd.musicalpitch import MusicalPitch
from solfege.mpd.interval import Interval

header = """
header {
  lesson_id = "generated-hear-tones-%s"
  title = %s
  module = singanswer
  version = "3.9.2"
}
"""


ratio_dict = {
        'm2': (16/12, "16:12"),
        'M2': (9/8, "9:8"),
        'm3': (6/5, "6:5"),
        'M3': (5/4, "5:4"),
        'p4': (4/3, "4:3"),
        'p5': (3/2, "3:2"),
        'm6': (8/5, "8:5"),
        'M6': (5/3, "5:3"),
        'm7': (16/9, "16:9"),
        'M7': (15/8, "15:8"),
        'p8': (2, "2:1"),
        'm9': (1 + 16/12, "1+16:12"),
        'M9': (1 + 9/8, "1+9:8"),
        'm10': (1 + 6/5, "1+6:5"),
        'M10': (1 + 5/4, "1+5:4"),
        }

def icmp(a, b):
    if a[1:] == b[1:]:
        k = {'m': 0, 'M': 1, 'p': 0}
        return cmp(k[a[0]], k[b[0]])
    return cmp(int(a[1:]), int(b[1:]))

interval_names = ratio_dict.keys()
interval_names.sort(icmp)

# different number of cents the intonation questions should be wrong.
cents = (40, 30, 20, 15, 10, 8, 6, 5)


def write_file_copyright(f):
    print >> f, "# Solfege - ear training for GNOME"
    print >> f, "# Copyright (C) 2007, 2008 Tom Cato Amundsen"
    print >> f, "# License is GPL, see file COPYING"
    print >> f, "# Generated by tools/generate_lessonfiles.py"

def question(f, b, c):
    low = 60
    tone_a = MusicalPitch.new_from_int(low)
    tone_b = MusicalPitch.new_from_int(low + b)
    tone_c = MusicalPitch.new_from_int(low + c)
    print >> f, 'question {'
    print >> f, '  question_text = _("Sing the three tones")'
    print >> f, '  music = voice("< %s2 %s %s >")' % (
        (tone_a.get_octave_notename(),
         tone_b.get_octave_notename(),
         tone_c.get_octave_notename()))
    print >> f, '  answer = voice("%s8 %s %s")' % (
        (tone_a.get_octave_notename(),
         tone_b.get_octave_notename(),
         tone_c.get_octave_notename()))
    print >> f, '}'

def three_tones_less_than_octave(filename):
    """3 toner innenfor en oktav
    0 1 2-12
    0 2 3-12
    0 3 4-12
    0 10 11-12
    0 11 12
    a  b  c
    """
    f = codecs.open(filename, 'w', 'utf-8')
    write_file_copyright(f)
    f.write("""header {
  lesson_id = "80cc940b-c47b-4264-a7b5-6cbd7a997bb0"
  title = _("Triads")
  module = singanswer
  version = "3.9.2"
}
""")
    for b in range(1, 12):
        for c in range(b + 1, 13):
            question(f, b, c)
    f.close()


def three_tones_larger_than_octave(filename):
    """3 toner innenfor en oktav
    0 1  13-24      13==cis  24=c
    0 2  13-24
    0 11 13-24
    0 12 13-24    c c cis-c

   #0 12 13-24
    0 13 14-24
    0 14 15-24
    0 22 23-24
    0 23    24
    a  b  c
    """
    f = codecs.open(filename, 'w', 'utf-8')
    write_file_copyright(f)
    f.write("""header {
  lesson_id = "3f1c7305-9978-4fe3-9bb3-8c01ff776a08"
  title = _("Triads, difficult")
  module = singanswer
  version = "3.9.2"
}
""")
    for b in range(1, 13):
        for c in range(13, 25):
            question(f, b, c)
    for b in range(13, 24):
        for c in range(b+1, 25):
            question(f, b, c)
    f.close()

def csound_intonation(filename_fmt, mod, lesson_id):
    filename = filename_fmt % mod
    f = codecs.open(filename, 'w', 'utf-8')
    print >> f, "# Solfege - ear training for GNOME"
    print >> f, "# Copyright (C) 2004, 2005 Tom Cato Amundsen"
    print >> f, "# License is GPL, see file COPYING"
    print >> f
    print >> f, "header {"
    print >> f, '    lesson_id = "%s"' % lesson_id
    print >> f, '        module = idbyname'
    print >> f, '        help = "idbyname-intonation"'
    print >> f, '        title = _("Is the fifth flat, in tune or sharp? %%s") %% "(%s)"' % mod
    print >> f, '        filldir = vertic'
    print >> f, '        fillnum = 4'
    print >> f, '}'
    for s, d in enumerate((1, 9/8, 4/3, 3/2, 5/3, 15/8, 2)):
        for label, mult in (("intonation|flat", float(mod)), ("intonation|in tune", 1), ("intonation|sharp", 1/float(mod))):
            print >> f
            print >> f, 'question {'
            print >> f, ' name = _i("%s")' % label
            print >> f, ' set=%i' % s
            print >> f, ' csound(load("share/sinus.orc"), """'
            print >> f, '    f1 0 4096 10 1 1.25 0.95 0.8 0.6 0.4 0.2 '
            print >> f, '    i1 0 1 %f' % (220.0 * d)
            print >> f, '    i1 + 1 %f' % (220.0 * d * 3/2 * mult)
            print >> f, ' """)'
            print >> f, "}"
    f.close()

def iname_to_fn(s):
    return s.replace("m", "min").replace("M", "maj")

def csound_intonation2(harmonic, interval_name, cent):
    i = Interval(interval_name)
    if harmonic:
        hs = "harmonic-"
    else:
        hs = ""
    filename = os.path.join("exercises", "standard", "lesson-files", "csound-intonation-%s%s-%icent" % (hs, iname_to_fn(interval_name), cent))
    f = codecs.open(filename, 'w', 'utf-8')
    print >> f, "# Solfege - ear training for GNOME"
    print >> f, "# Copyright (C) 2004, 2005 Tom Cato Amundsen"
    print >> f, "# License is GPL, see file COPYING"
    print >> f
    print >> f, "header {"
    print >> f, '    lesson_id = "csound-intonation-%s%s-%icent"' % (hs, iname_to_fn(interval_name), cent)
    print >> f, '        module = idbyname'
    print >> f, '        help = "idbyname-intonation"'
    print >> f, '        title = _("Is the interval flat, in tune or sharp? %%s cent wrong") %% %i' % cent
    print >> f, '        lesson_heading = _("Just interval: %%s") %% _("%s") + " (%s)"' % (i.get_cname(), ratio_dict[i.get_cname_short()][1])
    print >> f, '        filldir = vertic'
    print >> f, '}'
    for c in range(12):
        hz = 220 * 2 ** (c/12)
        hz2 = hz * ratio_dict[i.get_cname_short()][0]
        for label, mult in (("intonation|flat", -cent),
                            ("intonation|in tune", 0),
                            ("intonation|sharp", cent)):
            print >> f
            print >> f, 'question {'
            print >> f, ' name = _i("%s")' % label
            print >> f, ' set=%i' % c
            print >> f, ' csound(load("share/sinus.orc"), """'
            print >> f, '   f1 0 4096 10 1 1.25 0.95 0.8 0.6 0.4 0.2 '
            if harmonic:
                print >> f, '   i1 0 1 %f' % hz
                print >> f, '   i1 0 1 %f' % (hz2 * 2**(mult / 1200))
            else:
                print >> f, '   i1 0 1 %f' % hz
                print >> f, '   i1 + 1 %f' % (hz2 * 2**(mult / 1200))
            print >> f, ' """)'
            print >> f, "}"
    f.close()

def generate_csound_intonation():
    # We don't specify a lessonfile manager since we don't need
    # any of the methods that depend on it.
    page = fp.Page(u"Experimental CSound exercises", fp.Column())
    fileheader = fp.FileHeader(1, page)
    section = fp.LinkList(u"Melodic intervals")
    page[-1].append(section)
    for idx, cname in enumerate(interval_names):
        subpage = fp.Page(Interval(cname).get_cname().title(), fp.Column())
        section.append(subpage)
        sect = fp.LinkList(Interval(cname).get_cname().title())
        subpage[-1].append(sect)
        for cent in cents:
            csound_intonation2(False, cname, cent)
            sect.append("solfege:lesson-files/csound-intonation-%s-%icent" % (
                iname_to_fn(cname), cent))
    section = fp.LinkList(u"Harmonic intervals")
    col = fp.Column()
    page.append(col)
    page[-1].append(section)
    for idx, cname in enumerate(interval_names):
        subpage = fp.Page(Interval(cname).get_cname().title(), fp.Column())
        section.append(subpage)
        sect = fp.LinkList(Interval(cname).get_cname().title())
        subpage[-1].append(sect)
        for cent in cents:
            csound_intonation2(True, cname, cent)
            sect.append("solfege:lesson-files/csound-intonation-harmonic-%s-%icent" % (
                iname_to_fn(cname), cent))
    f = codecs.open("exercises/standard/csound-tree.txt", "w", "utf-8")
    fileheader.dump(f)
    f.close()

generate_csound_intonation()

csound_intonation("exercises/standard/lesson-files/csound-fifth-%s", "0.97",
    "b465c807-d7bf-4e3a-a6da-54c78d5b59a1")
csound_intonation("exercises/standard/lesson-files/csound-fifth-%s", "0.98",
    "aa5c3b18-664b-4e3d-b42d-2f06582f4135")
csound_intonation("exercises/standard/lesson-files/csound-fifth-%s", "0.99",
    "5098fb96-c362-45b9-bbb3-703db149a079")
csound_intonation("exercises/standard/lesson-files/csound-fifth-%s", "0.995",
    "3b1f57e8-2983-4a74-96da-468aa5414e5e")
csound_intonation("exercises/standard/lesson-files/csound-fifth-%s", "0.996",
    "a06b5531-7422-4ea3-8711-ec57e2a4ce22")
csound_intonation("exercises/standard/lesson-files/csound-fifth-%s", "0.997",
    "e67c5bd2-a275-4d9a-96a8-52e43a1e8987")
csound_intonation("exercises/standard/lesson-files/csound-fifth-%s", "0.998",
    "1cadef8c-859e-4482-a6c4-31bd715b4787")
three_tones_less_than_octave("exercises/standard/lesson-files/hear-tones-triads")
three_tones_larger_than_octave("exercises/standard/lesson-files/hear-tones-triads-difficult")
