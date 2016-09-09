import json
import math
import urllib.parse
import urllib.request
import urllib.response
import os

class Octopart:
    """
    Class to contain the Octopart data without saving a Json string
    """
    def __init__(self, jsonStream):
        """
        Octopart init. Takes a dict representing a single Octopart item and converts it to an Octopart()
        :param jsonStream: Dict returned from an Octosearch
        :type jsonStream: dict
        """
        self.uid = jsonStream['uid']
        self.mpn = jsonStream['mpn']
        self.brandName = jsonStream['brand']['name']
        self.manufacturer = jsonStream['manufacturer']['name']
        self.octopartUrl = jsonStream['octopart_url']
        self.shortDescription = jsonStream['short_description']
        self.quantity = 0

    def getTechSpecs(self, apiKey, images=False, description=False, datasheets=False):
        """
        Performs a part-match with Octopart and includes the tech specs. Adds the tech specs to the Octopart
        :param apiKey: API key from config file
        :type apiKey: str
        :param images: Boolean on whether or not to include images
        :type images: bool
        :param description: Boolean on whether or not to include long descriptions
        :type description: bool
        :param datasheets: Boolean on whether or not to include datasheet downloads
        :type datasheets: bool
        """
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
        if data['datasheets']:
            if len(data['datasheets']) > 1:
                urlString = data['datasheets'][1]['url']
                urlArray = urlString.rpartition('/')
                fileName = urlArray[len(urlArray) - 1]
                fileName = os.path.join('datasheets/', fileName)
                self.dataFile = fileName
                self.dataURL = urlString

        specJson = data['specs']
        specArray = []
        for specName in specJson:
            tmpSpec = specJson[specName]
            name = tmpSpec['metadata']['name']
            value = tmpSpec['display_value']
            specArray.append([name, value])

        descArray = []
        if data['descriptions']:
            for i in range(0, len(data['descriptions'])):
                descArray.append(data['descriptions'][i]['value'])

        self.specs = specArray
        self.descriptions = descArray


def getOctoList(octoArray):
    """
    Converts an array of Octoparts in a list that can be added to a multilistbox
    :param octoArray: Array of Octoparts
    :type octoArray: list
    :return: List that can be added to multilistbox
    :rtype: list
    """
    tmpList = []
    for i in range(0, len(octoArray)):
        tmpList.append([octoArray[i].mpn, octoArray[i].manufacturer, octoArray[i].shortDescription])

    return tmpList

def octoSearch(apiKey, startItem, searchQuery):
    """
    Searches the Octopart database for the text in searchQuery, starting the results at startItem

    :param apiKey: API key from config file
    :type apiKey: str
    :param startItem: Result item to begin at
    :type startItem: int
    :param searchQuery: Search text to search Octopart with
    :type searchQuery: str
    :return: Array of Octoparts
    :rtype: list
    """
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
