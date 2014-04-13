#!/usr/bin/env python

import common
import emt.parse
import emt.interpret

config_text = '''
[one]
envvar_FOO = set:foo
envvar_BAR = bar
envvar_PREPATH = prepend:/path/to/my/house
envvar_POSTPATH = append:/path/to/your/house
envemit_setup = somescript {shell}
envgenf_setup = somescriptgeneratingafile
envfile_setup = /path/to/some/file
'''

expected_env_sh = '''
FOO=foo ; export FOO
BAR=bar ; export BAR
PREPATH=/path/to/my/house${PREPATH:+:}${PREPATH} ; export PREPATH
POSTPATH=${POSTPATH}${POSTPATH:+:}/path/to/your/house ; export POSTPATH
eval `somescript sh`
source `somescriptgeneratingafile`
source /path/to/some/file
'''.strip()

expected_env_csh = '''
setenv FOO foo
setenv BAR bar
setenv PREPATH /path/to/my/house:${PREPATH}
setenv POSTPATH ${POSTPATH}:/path/to/your/house
eval `somescript csh`
source `somescriptgeneratingafile`
source /path/to/some/file
'''.strip()


def _test_shell(sh, expected):
    params = dict(shell=sh)
    cfg = emt.parse.load_text(config_text, **params)
    script = emt.interpret.env(cfg, ['one'], shell = sh).strip()
    want = expected
    print('---got:\n'+script+'\n---')
    #print('---want:\n'+want+'\n---')
    assert script == want

def test_env_sh():
    '''
    Test emitting sh code.
    '''
    _test_shell('sh', expected_env_sh)

def test_env_csh():
    '''
    Test emitting csh code.
    '''
    _test_shell('csh', expected_env_csh)


def test_reqs():
    '''
    Test turning a config with "require" into shell setup code
    '''
    want = '''
PATH=/path/to/install/gcc/4.8.2${PATH:+:}${PATH} ; export PATH
PATH=/path/to/install/cmake/2.8.12${PATH:+:}${PATH} ; export PATH
    '''.strip()

    params = dict(shell='sh')
    cfgfile = 'tests/configs/reqs.emt'
    cfg = emt.parse.load_files(cfgfile, **params)
    script = emt.interpret.env(cfg, ['buildtools'], shell = 'sh').strip()
    #print (script)
    assert script == want, 'Failed to make setup for %s' % cfgfile
