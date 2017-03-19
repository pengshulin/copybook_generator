#!/usr/bin/env python
# coding:utf8

fin = '../github.exercise_generator/词语默写.txt'
fout = '词语抄写.txt'

single_mode = False

def loadWords(fname):
    ret=[]
    for l in open(fname,'r').read().decode(encoding='utf8').splitlines():
        l = l.split('#')[0].strip()
        if not l or l == u'\ufeff':
            continue
        if single_mode:
            for w in list(l.replace(' ','')):
                if not w or w.startswith('~'):
                    continue
                if w in ret:
                    continue
                ret.append(w)
        else:
            for w in l.split(' '):
                if not w or w.startswith('~'):
                    continue
                while len(w) < 12:
                    w += '_'
                if w in ret:
                    continue
                ret.append(w)
    return ret


def main():
    out = u'\n'.join(loadWords(fin))
    print out
    open(fout, 'w+').write( out.encode(encoding='utf8') )


if __name__ == "__main__":
    main()
    
