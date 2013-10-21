"""
Qt Stylesheet module
Allow you to load a styleSheet to use in PySide/PyQt4 applications

The MIT License (MIT)

Copyright (c) 2013 Sylvain Berger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
__author__ = "Sylvain Berger"
__email__ = "sylvain.berger@gmail.com"
__copyright__ = "Sylvain Berger"
__version__ = "0.1.0"
__status__ = "Development"

import os
import sys
import re
from math import ceil
from string import Template
from jsonDict import JsonDict
import stylesheet.icons

STYLESHEET_FILE = os.path.join(os.path.dirname(__file__), 'styleSheet', 'template.stylesheet')
REGEX = re.compile("(#([abcdef0123456789]{1,6})#([abcdef0123456789]{1,6}))")

# The toRgb and toHex convertion were taken from Stackoverflow
# http://stackoverflow.com/questions/4296249/how-do-i-convert-a-hex-triplet-to-an-rgb-tuple-and-back
_NUMERALS = '0123456789abcdefABCDEF'
_HEXDEC = {v: int(v, 16) for v in (x+y for x in _NUMERALS for y in _NUMERALS)}
LOWERCASE, UPPERCASE = 'x', 'X'

def toRgb(hex):
    return (_HEXDEC[hex[0:2]], _HEXDEC[hex[2:4]], _HEXDEC[hex[4:6]])

def toHex(rgb, lettercase=LOWERCASE):
    return format((rgb[0]<<16 | rgb[1]<<8 | rgb[2]), '06'+lettercase)

def multHex(color1, color2):
    rgb1 = toRgb(color1)
    rgb2 = toRgb(color2)
    return (int(ceil(rgb1[0]*rgb2[0]/255)), int(ceil(rgb1[1]*rgb2[1]/255)), int(ceil(rgb1[2]*rgb2[2]/255)))

def _getThemeFile(theme):
    """ Return the path of the styleSheet file matching the provided theme """
    root = os.path.join(os.path.dirname(__file__), 'themes')
    for f in os.listdir(root):
        if os.path.splitext(f)[1] == '.theme' and f.lower().startswith(theme.lower()):
            return os.path.join(root, f)

def getStyleSheet(theme='default'):
    """ Return the stylesheet file content or the provided theme
    Return the default stylesheet if the provided one could not be found
    """
    # find the requested theme
    themeFile = _getThemeFile(theme)

    if not themeFile:
        # The requested theme could not be found, get the default one
        themeFile = _getThemeFile('default')
    if not themeFile:
        # Not even the default theme could be found ...
        return ''

    # read the stylesheet file content
    f = open(STYLESHEET_FILE, 'r')
    stylesheet = ''.join(f.readlines())
    f.close()

    # replace the color keys in the stylesheet by the real color values from the theme file
    colors = JsonDict.fromFile(themeFile)
    # print stylesheet[0:800]
    stylesheet = Template(stylesheet)
    stylesheet = stylesheet.substitute(**colors)
    # handle the color multiply (i.e.: Two color next to one another #ffffff#aa10bb)
    while True:
        match = re.search(REGEX, stylesheet)
        if match:
            block, rgb1, rgb2 = match.groups()
            newColor = toHex(multHex(rgb1, rgb2))
            stylesheet = stylesheet.replace(block, '#%s' % newColor, 1)
        else:
            break
    return stylesheet

if __name__ == '__main__':
    styleSheet = getStyleSheet('default')
    print styleSheet[:400]
