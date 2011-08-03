"""
Connect to World Bank Indicators API
"""
import urlparse
import httplib # delete after debug?
httplib.HTTPConnection.debuglevel = 1
import urllib
import urllib2
import json
#from client import *

from handlers import DefaultErrorHandler, RedirectHandler

BASE_URL = "http://api.worldbank.org"
SOURCE_URL = urlparse.urljoin(BASE_URL, "sources")

class Connection(object):
    def __init__(self, base_url, user_agent):
        self.base_url = base_url
        self.user_agent = user_agent
        self._cache = {} #make sqlite instance persistant dbase
        self._opener = urllib2.build_opener(DefaultErrorHandler, 
                               RedirectHandler)

class WBConnection(Connection):
    def __init__(self, default_fmt='json'):
        base_url = "http://api.worldbank.org"
        user_agent = 'wbquery/0.1-dbg +http://github.com/jseabold'
        super(WBConnection, self).__init__(base_url, user_agent)

        formats = {
                    'json'  : {'format' : 'json'},
                    'xml'   : {'format' : 'xml'},
                    'jsonp' : {'format' : 'jsonp', 
                               'prefix' : 'Getdata'}
                    }
        self.formats = formats
#        self.default_fmt = urllib.urlencode(formats['json'])
        self.default_fmt = 'json'

    def _get_fmt(self, fmt=None):
        if not fmt:
            return self.default_fmt
        return urllib.urlencode(self.formats[fmt])

    def _load_stream(self, stream, fmt):
        if fmt == 'json':
            return json.load(stream)
        else:
            raise NotImplementedError("Format not supported yet")

    def search(self):
        pass

    def categories(self):
        pass

    def fetch(self, ext_url, fmt=None):

        return_fmt = fmt or self.default_fmt
        fmt = self._get_fmt(fmt)
        stream = self.open_url(ext_url, return_fmt)
        #TODO: unzip, handle formats better
        return self._load_stream(stream, return_fmt)


    #TODO: this stuff might be able to go up a level
    def open_url(self, ext_url, fmt=None):
        fmt = self._get_fmt(fmt)
        url = urlparse.urljoin(self.base_url, ext_url) +'?' + fmt
        request = urllib2.Request(url)
        request.add_header('User-agent', self.user_agent)
        request.add_header('Accept-encoding', 'gzip')
        opener = self._opener
        stream = opener.open(request)
        #TODO deal with return status
        return stream


    def _get_sources(self, fmt=None):
        source_url = 'sources'
        return self.fetch(source_url, fmt)

        
        


#TODO: it doesn't look like it sends an Etag or Last-Modified
#count. Maybe it does for the data?
#datafmt = urllib.urlencode(formats['json'])
#request = urllib2.Request(SOURCE_URL + '?' + datafmt)
#request.add_header('User-Agent',
#                    'wbquery/0.1-dbg +http://github.com/jseabold')
#request.add_header('Accept-encoding', 'gzip')
#opener = urllib2.build_opener(DefaultErrorHandler, 
#                               RedirectHandle)
#stream = opener.open(request)

#200, 301, 302, 404
#check stream.status for redirects or ok and handle accordingly
