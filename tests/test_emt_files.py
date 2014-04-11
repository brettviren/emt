#!/usr/bin/env python

import os
import common
import emt.files

def test_find():
    '''
    Find some configuration files
    '''
    for p in ['tests/configs', './tests/configs', os.path.join(common.test_dir,'configs') ]:
        for n in ['simple.emt', 'reqs.emt']:
            path = p
            res = emt.files.find(n, path)
            assert res, '%s in %s' % (n, path)
            path = [p]
            res = emt.files.find(n, path)
            assert res, '%s in %s' % (n, path)

def test_glob():
    'Test glob finding'
    res = emt.files.glob('tests/configs/*.emt')
    assert res
    res = emt.files.glob('configs/*.emt','tests')
    assert res
    res = emt.files.glob('*.emt','tests/configs')
    assert res
    

def test_discover():
    'Test file discovery'
    res = emt.files.discover(path='tests/configs')
    assert res

def test_includes():
    'Test file inclusion'
    start = emt.files.glob('tests/configs/start.emt')
    assert len(start) == 1
    full = emt.files.includes(start)
    assert len(full) == 3
    assert 'include2.emt' in full[0]
    assert 'include1.emt' in full[1]
    assert 'start.emt' in full[2]


