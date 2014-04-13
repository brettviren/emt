#!/usr/bin/env

def dependencies(sec, cfg):
    '''Return an ordered list of package section names on which the given
    <sec> depends on, but not <sec> itself
    '''

    # "parse" the "require dsl"
    depexp = ' '.join([l.strip() for l in cfg[sec].get('require',"").split('\n')])
    
    if not depexp:
        return list()
    
    defaults = dict()
    for osec,odat in cfg.items():
        for k in odat: 
            defaults[k] = ""
        
    ret = list()
    for osec, odat in cfg.items():
        if osec == sec: continue # skip self
        if osec in ret: continue # skip already seen
        try:
            hit = eval(depexp, defaults, odat)
        except NameError:
            continue
        except SyntaxError:
            print (depexp)
            raise
        if not hit:
            continue
        ret.append(osec)
    return ret


def sh_envvar(var, cmd):
    '''
    Return Bourne shell commands for an environment variable setting
    '''
    val = cmd
    if cmd.startswith('prepend'):
        delim = cmd[len('prepend')]
        val = cmd[len('prepend')+1:]
        return "%(var)s=%(val)s${%(var)s:+%(delim)s}${%(var)s} ; export %(var)s" % locals()
    if cmd.startswith('append'):
        delim = cmd[len('append')]
        val = cmd[len('append')+1:]
        return "%(var)s=${%(var)s}${%(var)s:+%(delim)s}%(val)s ; export %(var)s" % locals()
    # everything else is a assumed to be a direct setting
    if cmd.startswith('set'):
        val = cmd[4:]
    return "%(var)s=%(val)s ; export %(var)s" % locals()



def csh_envvar(var, cmd):
    '''
    Return C-shell commands for an environment variable setting
    '''
    val = cmd
    if cmd.startswith('prepend'):
        delim = cmd[len('prepend')]
        val = cmd[len('prepend')+1:]
        return "setenv %(var)s %(val)s%(delim)s${%(var)s}" % locals()
    if cmd.startswith('append'):
        delim = cmd[len('append')]
        val = cmd[len('append')+1:]
        return "setenv %(var)s ${%(var)s}%(delim)s%(val)s" % locals()
    # everything else is a assumed to be a direct setting
    if cmd.startswith('set'):
        val = cmd[4:]
    return "setenv %(var)s %(val)s" % locals()
    

    return ""


def env_emit(label, args):
    '''
    Run command <args> which emits shell code to stdout for eventual evaluation.  
    '''
    return 'eval `%s`' % args

def evn_genf(label, args):
    return 'source `%s`' % args

def env_file(label, args):
    return 'source %s' % args

from collections import namedtuple
ShellFuncs = namedtuple('ShellFuncs','var emit genf file')
env_funcs = dict(
    sh   = ShellFuncs( sh_envvar, env_emit, evn_genf, env_file),
    bash = ShellFuncs( sh_envvar, env_emit, evn_genf, env_file),
    csh  = ShellFuncs(csh_envvar, env_emit, evn_genf, env_file),
    tcsh = ShellFuncs(csh_envvar, env_emit, evn_genf, env_file),
)

def env(cfg, pkgs = None, shell = 'sh'):
    '''
    Return text making up a shell-specific script for sourcing based on
    configuration object <cfg>.  If <shell> is not specified divine it
    from the calling environment.
    '''
    funcs = env_funcs[shell]

    if not pkgs:
        pkgs = cfg.keys()

    allpkgs = list()
    for p in pkgs:
        deps = dependencies(p, cfg) + [p]
        for d in deps:
            if d in allpkgs:
                continue
            allpkgs.append(d)

    ret = list()
    for pkg in allpkgs:
        pdat = cfg[pkg]
        for k, v in pdat.items():
            for ind,typ in enumerate(ShellFuncs._fields):
                pre = 'env%s_' % typ
                siz = len(pre)
                if k.startswith(pre):
                    ret.append(funcs[ind](k[siz:], v))
                    continue
    return '\n'.join(ret)
