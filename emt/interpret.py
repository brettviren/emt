#!/usr/bin/env

def dependencies(sec, cfg):
    'Return an ordered list of package section names on which the given <sec> depends on'

    depexps = cfg[sec].get('require',"").strip().split('\n')
    
    if not depexps:
        return list()
    
    ret = list()
    for depexp in depexps:
        depexp = depexp.strip()
        if not depexp:
            continue
        for osec, odat in cfg.items():
            if osec == sec: continue # skip self
            if osec in ret: continue # skip already seen
            try:
                hit = eval(depexp, None, odat)
            except NameError:
                continue
            except SyntaxError:
                print (depexp)
                raise
            if not hit:
                continue
            ret.append(osec)
    return ret




