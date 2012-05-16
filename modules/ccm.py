# -*- coding: utf-8  -*-

def tidy(path, deadline):
    import os
    fullpath = lambda f: os.path.join(path, f)
    isfile = lambda f: os.path.isfile(fullpath(f))
    isdead = lambda f: int(os.path.getmtime(fullpath(f))) < deadline
    for fi in [fullpath(f) for f in os.listdir(path) if isfile(f) and isdead(f)]:
        os.remove(fi)

def normalize(id):
    if id < 0:
        return 'r'+str(abs(id))
    return 'w' + str(id)

def save(data, path=False):
    f = open(path, 'w')
    f.write(data)
    f.close()
    return len(f.read())


