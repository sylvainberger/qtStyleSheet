"""
Json dictionary class.
Use this to simplify the loading, saving of json data

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
__version__ = "1.0.0"
__status__ = "Production"

import os
import json

class JsonDict(dict):
    """ Dictionary that can load, save and perform different thing on json data """
    filename = None

    def __init__(self, filename=None, autoLoad=True):
        super(JsonDict, self).__init__()
        if filename:
            self.filename = filename
        if autoLoad and self.filename:
            self.load()

    @classmethod
    def fromFile(cls, filename):
        """ Constructor that create a jsonDict from a json file """
        inst = JsonDict()
        inst.load(filename=filename)
        return inst

    @classmethod
    def fromJson(cls, jsonString):
        """ Constructor that takes a json string as input data """
        inst = JsonDict()
        inst.loads(jsonString)
        return inst

    def load(self, filename=None):
        """ Load a json file from disk """
        if filename:
            self.filename = filename
        if not self.filename or not os.path.exists(self.filename):
            return
        f = open(self.filename, 'r')
        _json = json.load(f)
        self.update(_json)
        return self.filename

    def save(self, filename=None):
        """ Save the data in a json formated file on disk"""
        if filename:
            self.filename = filename
        if not self.filename:
            return
        f = open(self.filename, 'w')
        json.dump(self, f, indent=4, sort_keys=True)
        return self.filename

    def loads(self, jsonString):
        """ Load a json string """
        _json = json.loads(jsonString)
        self.update(_json)

    def dumps(self, indent=4):
        """ Return a json string of the data """
        return json.dumps(self, indent=indent, sort_keys=True)

    def toJson(self, *args, **kwargs):
        """ Return a json string of the data """
        return self.dumps(**kwargs)

