#!/usr/bin/env python
# coding:utf8

fin = '../github.exercise_generator/词语默写.txt'
fout = '词语抄写.txt'

def loadWords(fname):
    ret=[]
    for l in open(fname,'r').read().decode(encoding='utf8').splitlines():
        l = l.split('#')[0].strip()
        if not l or l == u'\ufeff':
            continue
        for w in list(l.replace(' ','')):
            if not w or w.startswith('~'):
                continue
            if w in ret:  # 去除重复的词语，在打乱顺序模式下有用
                continue
            ret.append(w)
    return ret


def main():
    out = u'\n'.join(loadWords(fin))
    print out
    open(fout, 'w+').write( out.encode(encoding='utf8') )


if __name__ == "__main__":
    main()
    
