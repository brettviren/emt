#!/usr/bin/env python


def python2parser():
    '''
    Return a ConfigParser (Python 2)
    '''
    import ConfigParser
    import collections.OrderedDict
    return ConfigParser.SafeConfigParser(dict_type = collections.OrderedDict)

def python3parser():
    '''
    Return a ConfigParser (Python 3)
    '''
    from configparser import ConfigParser, ExtendedInterpolation
    return ConfigParser(interpolation=ExtendedInterpolation())

try:
    import configparser
except ImportError:
    ConfigParser = python2parser
else:
    ConfigParser = python3parser

import re
def mgetter(callable):
    def f(match):
        key = match.group(1)
        val = callable(key,'{'+key+'}')
        return val
    return f

subn_reobj = re.compile(r'{(\w+)}')
def format_get(string, getter):
    '''Format <string> using the function <getter(key, default)> which
    returns the value for the <key> or <default> if not found.
    '''
    ret = re.subn(subn_reobj, mgetter(getter), string)
    return ret[0]

def _format(string, **items):
    '''Format <string> using <items>'''
    return format_get(string, items.get)


def interpolate(cfg):
    # fixme: do something here using the above _format()
    return cfg

def parse_files(filenames):
    cfg = ConfigParser()
    cfg.read(filenames)
    return interpolate(cfg)

