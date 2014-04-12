#!/usr/bin/env python

from collections import OrderedDict

def python2parser():
    '''
    Return a ConfigParser (Python 2)
    '''
    import ConfigParser
    return ConfigParser.SafeConfigParser(dict_type = OrderedDict)

def python3parser():
    '''
    Return a ConfigParser (Python 3)
    '''
    from configparser import ConfigParser
    return ConfigParser()

try:
    import configparser
except ImportError:
    ConfigParser = python2parser
else:
    ConfigParser = python3parser

import re

def dictify(cfg):
    '''Take a ConfigParser object and return an ordered dict of ordered
    dicts of configuration items.  Configuration items consist of a
    key and a value
    '''
    ret = OrderedDict()
    for sec in cfg.sections():
        secdat = OrderedDict()
        secdat['ID'] = sec
        ret[sec] = secdat
        for k,v in cfg.items(sec):
            secdat[k] = v
    return ret

subn_reobj = re.compile(r'{([:\w]+)}')
def format_string(string, sec, dat):
    '''
    Format a <string> in the context of section <sec> of a dict of dicts <dat>.
    '''
    def f(match):
        key = match.group(1)
        mysec = sec
        if ':' in key:
            mysec, key = key.split(':',1)
        return dat[mysec].get(key, '{%s}'%key)
    return re.subn(subn_reobj, f, string)[0]

def interpolate(cfgdat):
    '''
    Interpolate all values of a configuration data structure <cfgdat>
    '''
    clean = True
    for sec,secdat in cfgdat.items():
        for k,v in secdat.items():
            new_v = format_string(v, sec, cfgdat)
            if new_v == v:
                continue
            secdat[k] = new_v
            clean = False
    if clean:
        return cfgdat
    return interpolate(cfgdat)


def load_files(filenames):
    '''
    Parse configuration files, return configuration data structure. 
    '''
    cfg = ConfigParser()
    cfg.read(filenames)
    d = dictify(cfg)
    return interpolate(d)

