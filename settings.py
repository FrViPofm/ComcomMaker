# -*- coding: utf-8  -*-
"""comcommaker@frvipofm.net"""

__version__ = '0.0.4'
created_by = "comcommaker@frvipofm.net"

## connexion
## to osm2psql database
## local ##
db_name= 'gis'
db_user= 'postgres'
db_host= 'localhost'
db_password= 'NNN'             #TODO: MASQUER
db_table= 'france_polygon'  # table
db_geometry= 'way'      # geometry field
db_srid= '4326'
db_debug= False

db_where= "boundary='administrative' AND admin_level='8'" #default

## api
api_server= "www.openstreetmap.org"
api_path = "/api/0.6/"


from time import gmtime, mktime
# cache
cache_dir= "cache/"
cache_deadline = int(mktime(gmtime())) - (60*60*24) # cache 24 h

#debugging
debug=True
