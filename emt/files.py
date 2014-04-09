#!/usr/bin/env python

import os
from glob import glob as pyglob
from . import parse

def expanduservars(name):
    return os.path.expanduser(os.path.expandvars(name))

def find(name, path = None):
    '''Find file named <name> which can be composed of environment and
    user home directory markers ("~").  

    If path is given it is either a list of a colon-separated string
    under which the file is additionally searched (assuming <name> is
    a relative path).

    Return the expanded path to the first found file or None if not
    found.
    '''
    name = expanduservars(name)
    if os.path.exists(name):
        return name
    if name.startswith(os.pathsep):
        return
    if not path:
        return
    if isinstance(path, type("")):
        path = path.split(':')
    for p in path:
        n = os.path.join(expanduservars(p), name)
        if os.path.exists(n):
            return n

def glob(pattern, path = None):
    '''
    Like find() but interpret <pattern> as a glob.  A list is returned.
    '''
    name = expanduservars(pattern)
    maybe = pyglob(name)
    if maybe:
        return maybe
    if name.startswith(os.pathsep):
        return list()
    if not path:
        return list()
    if isinstance(path, type("")):
        path = path.split(':')
    ret = list()
    for p in path:
        n = os.path.join(expanduservars(p), name)
        maybe = pyglob(n)
        if maybe: 
            ret += maybe
    return ret

    
def discover(files = ['~/.emt', './config.emt', "*.emt"], 
             path = os.environ.get('EMT_PATH')):
    '''Discover EMT files'''
    ret = list()
    if isinstance(files, type("")):
        files = [files]
    for p in files:
        ret += glob(p, path)
    return ret

def includes(files):
    '''Scan the <files> list for the "includes" section.  Found files are
    inserted the including one and OSError is raised if file an
    included file is not found.  Files are found via glob().'''
    collect = list()
    for f in files:
        p = parse.ConfigParser()
        p.read(f)
        if not p.has_section('includes'):
            collect.append(f)
            continue

        path = os.path.dirname(f)
        for k,v in p.items('includes'):
            if k != 'include':
                continue
            toinclude = glob(v, path)
            if not toinclude:
                raise OSError('no such file: %s' % v)
            collect = includes(toinclude) + collect
        collect.append(f)
    ret = list()
    for f in collect:
        if f in ret:
            continue
        ret.append(f)
    return ret
