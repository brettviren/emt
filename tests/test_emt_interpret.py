#!/usr/bin/env python

import common
import emt.parse
import emt.interpret


def test_dependencies():
    '''
    Test the "require" configuration item
    '''
    cfg = emt.parse.load_files('tests/configs/reqs.emt')

    expect = [[], [], [], ['gcc 4.8.2', 'worch', 'cmake 2.8.12']]
        

    for sec,want in zip(cfg, expect):
        deps = emt.interpret.dependencies(sec, cfg)
        #print (deps)
        assert deps == want, deps
