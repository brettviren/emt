#!/usr/bin/env python

import common
import emt.parse


def test_simple():
    '''
    Read in simple.emt make sure basic parsing works
    '''

    def _test_sec(sec):
        want = '{name}-{version}'
        theid = cfg.get(sec, 'namever')
        assert theid == want, 'Unresolved values "%s"' % theid


    cfg = emt.parse.ConfigParser()
    cfg.read('tests/configs/simple.emt')
    for want in ['packageA','packageB','packageC']:
        assert cfg.has_section(want), 'No section "%s"' % want
    for sec in cfg.sections():
        _test_sec(sec)


def test_dictify_and_interpolate():
    '''
    Read in and test inter-section variable interpolation.
    '''

    cfg = emt.parse.ConfigParser()
    cfg.read('tests/configs/inter_section.emt')

    d = emt.parse.dictify(cfg)
    assert d['two']['one_in_two_name'] == '{one:name}'
    i = emt.parse.interpolate(d)

    got = i['two']['one_in_two_name']
    want = 'one'
    assert got == want, 'got: "%s" want: "%s"' % (got, want)
    got = i['one']['two_in_one_name']
    want = 'two'
    assert got == want, 'got: "%s" want: "%s"' % (got, want)


def test_mutli_line():
    '''
    Test multiple lined configuration items.
    '''
    i = emt.parse.load_files('tests/configs/reqs.emt')
    bt = i['buildtools']
    assert bt, 'no buildtools section'
    reqs = bt['require'].strip().split('\n')
    assert len(reqs) == 3, reqs
