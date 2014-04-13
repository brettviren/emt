#!/usr/bin/env python

from collections import OrderedDict

def python2parser():
    '''
    Return a ConfigParser (Python 2)
    '''
    import ConfigParser
    cp2 = ConfigParser.SafeConfigParser(dict_type = OrderedDict)
    cp2.optionxform = str
    return cp2

def python3parser():
    '''
    Return a ConfigParser (Python 3)
    '''
    from configparser import ConfigParser
    cp3 = ConfigParser()
    cp3.optionxform = str
    return cp3

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
    defaults = cfg.defaults()

    ret = OrderedDict()
    for sec in cfg.sections():
        secdat = OrderedDict()
        secdat['ID'] = sec
        ret[sec] = secdat
        for k,v in cfg.items(sec):
            secdat[k] = v
        for k,v in defaults.items():
            secdat.setdefault(k, v)

    return ret

subn_reobj = re.compile(r'{([:\w]+)}')
def format_string(string, sec, dat, **kwds):
    '''
    Format a <string> in the context of section <sec> of a dict of dicts <dat>.
    '''
    def f(match):
        key = match.group(1)
        mysec = sec
        if ':' in key:
            mysec, key = key.split(':',1)
        try:
            return dat[mysec][key]
        except KeyError:
            pass
        try:
            return kwds[key]
        except KeyError:
            pass
        return '{%s}' % key

    return re.subn(subn_reobj, f, string)[0]

def interpolate(cfgdat, **kwds):
    '''
    Interpolate all values of a configuration data structure <cfgdat>.

    The <kwds> may hold any extra values used for interpolation.
    '''
    clean = True
    for sec,secdat in cfgdat.items():
        for k,v in secdat.items():
            new_v = format_string(v, sec, cfgdat, **kwds)
            if new_v == v:
                continue
            secdat[k] = new_v
            clean = False
    if clean:
        return cfgdat
    return interpolate(cfgdat)


def load_text(text, **kwds):
    '''
    Parse configuration text, return configuration data structure. 
    '''
    cfg = ConfigParser()
    if hasattr(cfg, 'read_string'):
        cfg.read_string(text)
    else:
        import io
        cfg.readfp(io.BytesIO(text))
    d = dictify(cfg)
    return interpolate(d, **kwds)
    

def load_files(filenames, **kwds):
    '''
    Parse configuration files, return configuration data structure. 
    '''
    cfg = ConfigParser()
    cfg.read(filenames)
    d = dictify(cfg)
    return interpolate(d, **kwds)

