#!/usr/bin/env python

import common
import emt.parse


def test_simple():

    def _test_sec(sec):
        name = cfg.get(sec, 'name')
        version = cfg.get(sec, 'version')
        want = name + '-' + version
        theid = cfg.get(sec, 'id')
        assert theid == want, 'Unresolved values "%s"' % theid


    cfg = emt.parse.ConfigParser()
    cfg.read('tests/configs/simple.emt')
    for want in ['packageA','packageB','packageC']:
        assert cfg.has_section(want), 'No section "%s"' % want
    for sec in cfg.sections():
        _test_sec(sec)
    for sec in cfg:
        if str(sec) == 'DEFAULT':
            continue
        _test_sec(sec)
