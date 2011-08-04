"""
Implements a cache to be used by httplib2.

Caches must define get, set, delete methods

Each stored key is gzipped
"""
import os
from httplib2 import FileCache
import gzip

#TODO: Replace these with a proper db?
#      caching could be more organized and aggressive, ie., caching actual
#      indicators in a db and not the specific page views
#NOTE: support for with statement in gzip only >= 2.7
def save_cached_key(path, value):
    f = gzip.open(path, 'wb')
    f.write(value)
    f.close()

def load_cached_key(key):
    f = gzip.open(key)
    retval = f.read()
    f.close()
    return retval

class ZipCache(FileCache):
    def __init__(self, cache='.cache'): #TODO: allow user configurable
        super(ZipCache, self).__init__(cache)

    def get(self, key):
        cacheFullPath = os.path.join(self.cache, self.safe(key))
        retval = None
        try:
            retval = load_cached_key(cacheFullPath)
        except IOError:
            pass
        return retval

    def set(self, key, value):
        retval = None
        cacheFullPath = os.path.join(self.cache, self.safe(key))
        save_cached_key(cacheFullPath, value)
