import json
import math
import urllib.parse
import urllib.request
import urllib.response


class Octopart:
    def __init__(self, jsonStream):
        self.uid = jsonStream['uid']
        self.mpn = jsonStream['mpn']
        self.brandName = jsonStream['brand']['name']
        self.manufacturer = jsonStream['manufacturer']['name']
        self.octopartUrl = jsonStream['octopart_url']
        self.shortDescription = jsonStream['short_description']
        self.quantity = 0

    def getTechSpecs(self, apiKey, images=False, description=False, datasheets=False):
        # To do: add auto datasheet download and images and description
        url = 'http://octopart.com/api/v3/parts/'
        url += self.uid
        url += '?apikey='
        url += apiKey
        url += '&include[]=specs'
        if images:
            url += '&include[]=imagesets'
        if description:
            url += '&include[]=descriptions'
        if datasheets:
            url += '&include[]=datasheets'

        data = json.loads(urllib.request.urlopen(url).read().decode())
        specJson = data['specs']
        specArray = []
        tempSpec = {}
        for specName in specJson:
            tmpSpec = specJson[specName]
            name = tmpSpec['metadata']['name']
            value = tmpSpec['display_value']
            tempSpec['name'] = name
            tempSpec['value'] = value
            specArray.append(tempSpec)
            tempSpec = {}

        self.specs = specArray

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
    octoList = []
    for item in searchResponse['results']:
        octoList.append(Octopart(item['item']))
    maxPages = math.ceil(searchResponse['hits'] / 10)

    octoList.append(maxPages)
    return octoList
