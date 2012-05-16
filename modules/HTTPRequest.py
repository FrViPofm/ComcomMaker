#!/usr/bin/python
# -*- coding: UTF-8 -*-

__version__ = '0.0.1'

import httplib, base64, re, xml.dom.minidom, time, sys, bz2, gzip, tempfile

class ApiError(Exception):
    	
    def __init__(self, status, reason, debug = True):
        self.status = status
        self.reason = reason
        self._debug = debug
    
    def __str__(self):
        return "Request failed: " + str(self.status) + " - " + self.reason

class httpRequest:

    def __init__(self, 
        server, 
        port=80, 
        api=u"www.openstreetmap.org",
        debug = False,
        created_by = "PythonTraceChecker/"+__version__,
        ):
        
        # debug
        self._debug = debug
        self._created_by = created_by
        
        self._conn = httplib.HTTPConnection(server, port)
        self._api = api

    def _http_request(self, cmd, path, auth, send):
        self.path = path
        filename = ""
        if self._debug:
            path2 = path
            if len(path2) > 50:
                path2 = path2[:50]+"[...]"
            print >>sys.stderr, "%s %s %s"%(time.strftime("%Y-%m-%d %H:%M:%S"),cmd,path2)
        self._conn.putrequest(cmd, path)
        self._conn.putheader('User-Agent', self._created_by)
        if auth:
            self._conn.putheader('Authorization', 'Basic ' + base64.encodestring(self._username + ':' + self._password).strip())
        if send:
            self._conn.putheader('Content-Length', len(send))
        self._conn.endheaders()
        if send:
            self._conn.send(send)
        response = self._conn.getresponse()
        if response.status <> 200:
            response.read()
            if response.status == 410:
                return None
            raise ApiError(response.status, response.reason)
        if self._debug:
            print >>sys.stderr, "%s %s %s done"%(time.strftime("%Y-%m-%d %H:%M:%S"),cmd,path2)
#        print response.status
#        print repr(response.getheader('Content-Type'))
#        print repr(response.getheader('Content-disposition'))
        mime = response.getheader('Content-Type').split('/')
        if response.getheader('content-disposition') :
            filename = re.search('"(.+)"',response.getheader('content-disposition')).group(1)
#        filename = 
        if mime[1] == "x-gzip" or filename.endswith(".gz"):
            path = './cache/'+ filename
            tmp = open(path, "w")
            tmp.write(response.read())
            tmp.close()
            return gzip.open(path).read()
        return response.read()
       

    def _http(self, cmd, path, auth, send):
        i = 0
        while True:
            i += 1
            try:
                return self._http_request(cmd, path, auth, send)
            except ApiError, e:
                if e.status >= 500:
                    if i == 5: raise
                    if i <> 1: time.sleep(5)
                    self._conn = httplib.HTTPConnection(self._api, 80)
                else: raise
            except Exception:
                if i == 5: raise
                if i <> 1: time.sleep(5)
                self._conn = httplib.HTTPConnection(self._api, 80)
    
    def get(self, path):
        return self._http('GET', path, False, None)

    def put(self, path, data):
        return self._http('PUT', path, True, data)
    
    def delete(self, path, data):
        return self._http('DELETE', path, True, data)
