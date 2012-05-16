#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
comcomMaker version %(VERSION)s %(DATE)s
Command-line or http tool for computing boundaries

Liste de relations sous la forme
   "ID,ID,..."
ou "rID,rID,..."(josm)
ou "-ID,-ID,..."(osm2pg)
"""
import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)

import settings

VERSION=settings.__version__
DATE='  2011-11-14'
MY_ENV={}
defaults={
  'tags': "type=boundary,boundary=administrative",
  'cache_dir':"cache/"
}
debug ={}
MODE_CONSOLE='console'
MODE_HTTP='http'

from modules import OsmApi
api = OsmApi.OsmApi()


class Status(object):

    def __init__(self, code, msg):
        self.code=code
        self.msg=msg


def get_relation(rid):
    rel = api.RelationGet(rid)
    return rel


def get_relations(RelationIdList):
    rels = api.RelationsGet(RelationIdList)
    return rels


def xor_list(a, b):
    """ return n if not n in a and n in b """
    return [i for i in a if i not in b] + [j for j in b if not j in a]


def list_rids(rids):
    # strip starting 'r' or '-'
    rids = rids.replace('r', '').replace('-', '')
    # strip trailing ','
#    if MY_ENV['mode']==MODE_CONSOLE:
#        print rids
    if(rids[-1] == ','):
        rids = rids[:-1]
    return rids


def dict_tags(teq, sep='\n'):
    # python 2.7
#    tagDict = {t.split('=')[0]:t.split('=')[1] for t in teq.split(sep)}
    
    # python 2.6
    splited = teq.split(sep)
    tagDict = {}
    for t in splited:
        k,v = t.split('=')
        tagDict[k]=v

#    if MY_ENV['mode']==MODE_CONSOLE:
#        print "tagDict", str(tagDict)
    return tagDict


def build_relation(members=[], tagDict={}):
    s="""<?xml version='1.0' encoding='UTF-8'?>
<osm version='0.6' generator='comcomMaker'>
  <relation id='-1' visible='true' action='modify' >
    %s
    %s
  </relation>
</osm>"""
    t="""<tag k='%s' v='%s' />"""
    m="""<member type='way' ref='%s' role='outer' />"""
    memberString="\n    ".join([m % i for i in members])
    tagString="\n    ".join([t % (i, tagDict[i]) for i in tagDict])
#    if MY_ENV['mode']==MODE_CONSOLE:
#        print "tagString", str(tagString)
    return s % (memberString, tagString)

def save(data, path=False):
    import os.path
    from time import gmtime, mktime
    from modules.ccm import save
    a = gmtime()
    if path:
        real_path = os.path.realpath(path)
    else:
        path = settings.cache_dir + str(int(mktime(gmtime())))+'-'+str(os.getpid())+'.osm'
        realpath = os.path.realpath(path)
    f = open(realpath, 'w')
    f.write(data)
    f.close()
#    debug['__file__']=__file__
#    debug['settings.cache_dir']=settings.cache_dir
#    debug['realpath']=realpath
    if MY_ENV['mode']==MODE_CONSOLE:
        return os.path.realpath(path)
    if MY_ENV['mode']==MODE_HTTP:
        return path

def main(RelationIdList, TagDict):
    # get relations from osm
    import os.path
    rels = get_relations(RelationIdList)
    data=''
#    debug["tagDict"]=TagDict
#    if MY_ENV['mode']==MODE_CONSOLE:
#        print str(rels)
    masterWayList = []
    for rid in rels:
        relWayList = [w['ref'] for w in rels[rid]['member'] if w['type']==u'way']
        masterWayList = xor_list(masterWayList, relWayList)
#        if MY_ENV['mode']==MODE_CONSOLE:
#            print str(relWayList)
#            print str(relWayList)
#    if MY_ENV['mode']==MODE_CONSOLE:
#        print 'm : ', ','.join(['w'+str(i) for i in masterWayList])
    dotOsm = build_relation(masterWayList, TagDict)
#    debug['osm']=dotOsm
    path = save(dotOsm)
#    debug['path'] = path
#    debug['real_path'] = os.path.realpath(path)
    if MY_ENV['mode']==MODE_CONSOLE:
        print "Your file have been saved at %s" % path
    elif MY_ENV['mode']==MODE_HTTP:
        status = Status(200, "OK.")
        data += '{"url":"%s"}' % path
        return status, data


def index(req):
    """ http request handler """
    import json
    MY_ENV['mode']=MODE_HTTP
    data=''
    req.content_type = "application/json;charset:utf-8"
    #relation
    if 'relations' not in req.form:
        status = Status(400, "no relation given.")
        data += '[]'
        req.status = status.code
        return '{"status":[%i,"%s"],"data":%s}' % (status.code, status.msg, data)
    rids = req.form['relations']
    RelationIdList = list_rids(rids).split(',')
    #tags
    teq = defaults['tags']
    if 'tags' in req.form:
        teq = req.form['tags']
    TagDict = dict_tags(teq, ',')

    status, data=main(RelationIdList, TagDict)

    req.status = status.code
    nested = '{"status":[%i,"%s", "%s"],"data":%s, "debug":%s}' % (status.code, status.msg, req.content_type, data, json.dumps(debug))
    return nested

if __name__ == "__main__":
    """ command line handler """
    MY_ENV['mode']=MODE_CONSOLE
    import argparse, textwrap
    msg = textwrap.dedent(__doc__) % {
        'VERSION': VERSION,
        'DATE': DATE}
    parser = argparse.ArgumentParser(
        description=msg,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        usage='%(prog)s [-h] rID[,rID...] [-t k=v[,k2=v,...]]]')
    parser.add_argument(
            'rids',
            help='Liste de relations',
            metavar='rID[,rID]',
            )
    parser.add_argument(
            '-t',
            '--teq',
            help='Liste de tags à appliquer : k=v[,k2=v,...]',
            dest='teq',
            metavar='k=v',
            default=defaults['tags'])
    kwargs = vars(parser.parse_args(sys.argv[1:]))
    RelationIdList = list_rids(kwargs['rids']).split(',')
    TagDict = dict_tags(kwargs['teq'], ',')

    main(RelationIdList, TagDict)
