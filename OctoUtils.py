import json
import math
import urllib.parse
import urllib.request
import urllib.response


def getTechSpecs(apiKey, uid):
    url = 'http://octopart.com/api/v3/parts/'
    url += uid
    url += '?apikey='
    url += apiKey
    url += '&include[]=specs'
    data = urllib.request.urlopen(url).read().decode()
    techResponse = json.loads(data)
    return techResponse


def octoSearch(apiKey, startItem, searchQuery):
    url = "http://octopart.com/api/v3/parts/search"
    url += "?apikey="
    url += apiKey

    args = [
        ('q', searchQuery),
        ('include', 'short_description'),
        ('start', startItem),
        ('limit', 10)
    ]

    url += '&' + urllib.parse.urlencode(args)
    data = urllib.request.urlopen(url).read().decode()
    searchResponse = json.loads(data)

    return searchResponse


def getHits(jsonDict):
    hits = jsonDict['hits']
    return hits


def getMaxPages(hits):
    maxPages = math.ceil(hits / 10)
    return maxPages
