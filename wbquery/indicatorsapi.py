"""
Connect to World Bank Indicators API

We grab supersets from the bank, but cache aggressively. That is, we would
grab all countries if a subset are requested, but then filter on the results.
This means that the cache is more efficient, since it leaves little scope for
the RESTful url to be different given different user options.
"""
import urlparse
import httplib # delete after debug?
import httplib2
httplib.HTTPConnection.debuglevel = 1
httplib.debuglevel = 1
import urllib
import urllib2
import json
from cStringIO import StringIO
#from client import *

#Ours
from handlers import DefaultErrorHandler, RedirectHandler
from caching import ZipCache

BASE_URL = "http://api.worldbank.org"
SOURCE_URL = urlparse.urljoin(BASE_URL, "sources")


def _check_params(params):
    for key in params:
        if key not in ['date','','']:
            pass

class RecursionWarning(Warning):
    pass

class Connection(object):
    def __init__(self, base_url, user_agent):
        self._base_url = base_url
        self.user_agent = user_agent
        #TODO: make cache directory configurable
        self.cache_control = 'max-age='+str(7 * 24 * 60 * 60)
                                        #TODO: make configurable
        self.connection = httplib2.Http(ZipCache())
        self._opener = urllib2.build_opener(DefaultErrorHandler,
                               RedirectHandler)

class WBIndicatorsConnection(Connection):
    def __init__(self):
        base_url = "http://api.worldbank.org"
        user_agent = 'wbquery/0.1-dbg +http://github.com/jseabold'
        super(WBIndicatorsConnection, self).__init__(base_url, user_agent)

        #this receives json. end of story?
        #self._format = urllib.urlencode({'format' : 'json'})
        self._params = {'format' : 'json',
                        'per_page' : '1000'}
        self._language = 'en'

    def _load_stream(self, stream):
        #        try:
        #            return json.load(stream)
        #        except:
        #            return json.load(StringIO(stream))
        return json.loads(stream)
#        raise ValueError("Could not load stream")

    def build_query(self, params):
        params = urlparse.urlencode(params)
        return params

    def set_language(self, lang):
        """
        Set the default

        Parameters
        ----------
        lang : str {'en','es','fr','ar'}
            English, Spanish, French, or Arabic
        """
        self._language = lang

    @property
    def base_url(self):
        """
        Propert representing the base url. It appands the language set in the class.
        """
        return urlparse.urljoin(self._base_url, self._language)

#    def get_regions(self):
#        #shouldn't need to update this very much?
#        year = str(365*24*60*60)
#        return self.fetch('regions', cache_control='max-age='+year)

    def get_countries(self, region=None):
        #shouldn't need to update this very much, one a year
        year = str(365*24*60*60)

        return self.fetch('countries', cache_control='max-age='+year)

#    def get_catalogue(self):
#        return self.fetch('sources')

#    def get_topics(self):
#        return self.fetch('topics')

#    def get_indicators(self):
#        return self.fetch('indicators')

    def get_data(self, country=None, indicator=None, topic=None):
        if not country and not indicator and not topic:
            raise( ValueError("Must select type of data") )
        #_make_query()

    def fetch(self, ext_url, params = {}, cache_control=None):
        """
        """

        # actually get the http stream, uses cached if available
        stream = self.open_url(ext_url, params, cache_control)

        #split the data stream up
        #TODO: might be able to change this when i write a custom json decoder
        head, body = self._load_stream(stream)

        # see if we need to grab more pages
        i = 1
        while head['page'] < head['pages'] and i <= 10:
            #and head['per_page'] < head['total'] #?
            page = head['page'] + 1
            params.update({'page' : page})
            stream = self.open_url(ext_url, params, cache_control)
            head, body2 = self._load_stream(stream)
            body.extend(body2)
            i += 1
            if i == 10 and head['page'] < head['pages']:
                msg = "Reached paged response recursion limit of 10. Data "
                msg += "may not be complete."
                raise RecursionWarning(msg)
        return body

    #TODO: this stuff might be able to go up a level
    def open_url(self, ext_url, params, cache_control=None):
        if not cache_control:
            cache_control = self.cache_control

        dft_params = self._params
        params.update(dft_params)
        params = urllib.urlencode(params)

        url = urlparse.urljoin(self.base_url, ext_url) +'?' + params
        connection = self.connection
        resp, content = connection.request(url, headers={
                    'user-agenet' : self.user_agent,
                    'accept-encoding' : 'gzip',
                    'cache-control' : cache_control})
        if resp.fromcache:
            print "Using from cache" #dbg
        #TODO deal with return status and encoding
        #_check_return_status(resp.status)
        return content

class QueryCountries(WBIndicatorsConnection):

    def build_url(self):
        pass

    def query(self, code):
        """
        code : str
            A country or region id.
        Allow querying for the full list of countries or detail about a single
        country.
        """
        url = self.base_url


#opener = urllib2.build_opener(DefaultErrorHandler,
#request.add_header('Accept-encoding', 'gzip')
#                               RedirectHandle)
#stream = opener.open(request)

#200, 301, 302, 404
#check stream.status for redirects or ok and handle accordingly

"""
datafmt = urllib.urlencode(formats['json'])
url = 'http://api.worldbank.org/countries/chn;bra/indicators/DPANUSIFS?date=2000Q1:2010Q3'
request = urllib2.Request(url + '&' + datafmt)
request.add_header('User-Agent',
                    'wbquery/0.1-dbg +http://github.com/jseabold')
request.add_header('Accept-encoding', 'gzip')
opener = urllib2.build_opener()
stream = opener.open(request)

# or use httlib2
connection = httplib2.Http('.cache')
url = urlparse.urljoin(wb.base_url, 'topics') + '?' + 'format=json'
"""

if __name__ == "__main__":
    wb = WBIndicatorsConnection()
#    catalogue = wb.get_catalogue()
#    topics = wb.get_topics()
#    indicators = wb.get_indicators()
#    regions = wb.get_regions()
    countries = wb.get_countries()
