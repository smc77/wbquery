#Not to sure I can a Decoder subclass more efficient than just parsing the
#dicts from JSON objects since WB doesn't follow the JSON Spec...

#fp = StringIO(content)
import json

class CountryDecoder(json.JSONDecoder):
    def decode(self, json_string):
        head, body = json.loads(json_string, object_hook=custom_decode)
#        for row in body
        return (head, body)

def country_decode(thread):
    headers = None
    if 'page' in thread:
        return thread
    else:
        if headers is None:
            headers = thread.keys()
        return thread

#json.loads(content, cls=CountryDecoder, object_hook=custom_decode)

#Notes from bank site on countries
#http://data.worldbank.org/node/18
#3 letter Code differences: Andorra, Congo, Dem. Rep., Isle of Man, Romania,
#                           Timor-Leste, West Bank and Gaza
#2 letter Code differences: Congo, Dem. Rep., Serbia, Timor-Leste, Yemen, Rep.,
#                           West Bank and Gaza
#Countries not yet represented using ISO codes: Channel Islands (JG), Kosovo
#Added to list by SS, Curacau (CW), Kosovo (KV), Sint Maaretn (Dutch Part) (SX)
#

def _is_region(code):
    """
    """
    #TODO: xc is euro zone, probably not a region outright
    return code in ["EAP","EAS","ECA","ECS","LAC","LCN",
                    "MNA","MEA","NAC","SAS","SSA","SSF",
                    "1A", '1W', '4E', '7E', '8S', 'ZF',
                    'XC', 'EU''XJ', 'XL','XQ','XU','OE',
                    '8S', 'ZF','1W']

def _is_not_country(code):
    return code in ["XC", "E"]

def _is_income_level(code):
    """
    """
    return code in ["NOC","OEC","HIC","HPC","LIC","LMC","LMY","MIC","UMC",
                    "Z4","Z7","XD","ZJ","XM","XN","XO","ZQ","XP","XR",
                    "XS","ZG","XT", "XE"]

def _is_country(code):
    """
    """
    if _is_region(code):
        return False
    if _is_income_level(code):
        return False
    import iso3166 #dbg
    try:
        iso3166.countries.get(code.lower())
    except:
        if not in 'JG'
        print '%s not in iso!?!' % code
    return True

def _country_conversion_map(*args):
    key, value = args
    if key in ['latitude','longitude']:
        return float(value)
    if key == 'id':
        return int(id)
    elif key in ['name', 'region', 'adminregion', 'iso2code', 'capitalCity',
            'incomeLevel', 'lendingType']:
        return value
    else:
        raise ValueError("key %s not handled" % key)

def _filter_countries(data, map=False):
    """
    Accepts a list of dicts, returns a list of lists

    If map is True, returns the value mapped to a type according to
    _country_conversion_map
    """
    #headers = data[0].keys()
    headers = ['name', 'region', 'adminregion', 'iso2Code', 'capitalCity', u'longitude',
               'latitude', 'incomeLevel', 'id', 'lendingType']
    results = [headers]
    for row in data:
        if not _is_country(row['iso2Code']):
            #TODO: remove them from the cache
            continue
        if map:
            results.append([_country_conversion_map(i, row[i]) for i in headers])
        else:
            results.append([row[i] for i in headers])
    return results



