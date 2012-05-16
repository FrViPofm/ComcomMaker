import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)

import settings


class Status(object):

    def __init__(self, code, msg):
        self.code=code
        self.msg=msg


def get_relation(rid):
    # downloads relation from osm.org and stores in cache
    from modules import HTTPRequest
    req = HTTPRequest.httpRequest(
        server=settings.api_server,
        api= settings.api_path,
        created_by= settings.created_by
    )
    rel = req.get(settings.api_path+'relation/'+str(abs(rid))+'/full')
    return rel


def get_entity(params):

    import psycopg2, psycopg2.extras
    rows = [{'osm_id':-1,
            'name':'debuging SQL',
            'wkt':'POINT (%(lon)s, %(lat)s)' % {'lat': params['lat'],'lon': params['lon']}
            }] # dummy result for debugging
    conn = psycopg2.connect("dbname='%(dbname)s' user='%(user)s' host='%(host)s' password='%(password)s'"% {
                                'dbname':settings.db_name,
                                'user':settings.db_user,
                                'host':settings.db_host,
                                'password':settings.db_password
                            })
    curs = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    q = """
SELECT out.osm_id AS osm_id,
    out.name AS name,
    ST_AsText(ST_Collect(ST_Transform(out.%(geometry)s,4326))) AS wkt
FROM %(table)s out
    JOIN %(table)s ref
        ON ref.osm_id=out.osm_id
WHERE
    %(where)s
    AND ST_WITHIN(ST_Transform(ST_SetSRID(ST_POINT(%(lon)s, %(lat)s),4326), %(srid)s), ref.%(geometry)s)
GROUP BY out.osm_id, out.name;
    """ % {
        'lat': params['lat'],
        'lon': params['lon'],
        'table': settings.db_table,
        'geometry': settings.db_geometry,
        'where': params['where'],
        'srid': settings.db_srid
    }
    if not settings.db_debug:
        curs.execute(q) # comment this line for sql debugging
        rows = curs.fetchall() # comment this line for sql debugging
    return rows, q


def main(req):

    from modules.ccm import save, normalize, tidy
    tidy(settings.cache_dir, settings.cache_deadline)
    data=''
    sql=''
    form = req.form
    try:
        settings.db_debug = form['db_debug']
    except:
        pass
    req.content_type = "application/json;charset:utf-8"
    if "lat" not in form or "lon" not in form:
        status = Status(400, "Lat and lon were not given.")
        data+= "[]"
        return status, data, sql
    params = {
        'where': settings.db_where,
        'lat': form['lat'].value,
        'lon': form['lon'].value,
        }
    if "where" in form:
        where = form['where'].value.split('\n')
        w = ['ref."'+t.split('=')[0]+"\"='"+t.split('=')[1]+"'" for t in where]
        params['where'] = " AND ".join(w)
    rows, sql = get_entity(params)
    if len(rows) == 0:
        status = Status(204, "Nothing found.")
        data = "{}"
    if len(rows) == 1:
        status = Status(200, "OK.")
        data = '{"id":"%(osm_id)s","name":"%(name)s","wkt":"%(wkt)s"}' % rows[0]
#        rid = rows[0]['osm_id']
#        osm=get_relation(rid)
#        save(osm,settings.cache_dir+normalize(rid)+'.osm')
        
    if len(rows) > 1:
        status = Status(206, "Several result, first sent.")
        data = '{"id":"%(osm_id)s","name":"%(name)s"}' % rows[0]
#        rid = str(abs(rows[0]['osm_id']))
#        osm=get_relation(rid)
    return status, data, sql


def index(req):
    status, data, sql = main(req)
    req.status = status.code
    sql = sql.replace('"', '\\"').replace('\n', '\\n')
    nested = '{"status":[%i,"%s"],"data":%s, "sql":"%s"}' % (status.code, status.msg, data, sql)
    return nested
