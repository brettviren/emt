#!/usr/bin/env python

def python2parser():
    import ConfigParser
    # fixme: need to add some thing custom to support ${section:key} type interpolation
    return ConfigParser.SafeConfigParser()

def python3parser():
    import configparser
    return configparser.ConfigParser(configparser.ExtendedInterpolation())

try:
    import configparser
except ImportError:
    ConfigParser = python2parser
else:
    ConfigParser = python3parser
