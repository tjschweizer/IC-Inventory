import json
import math
import urllib.parse
import urllib.request
import urllib.response
from tkinter import *


def techSpecs(self):
    selectedUID = self.partList[self.resultsList.row][3]
    url = 'http://octopart.com/api/v3/parts/'
    url += selectedUID
    url += '?apikey=1ef54ac1'
    url += '&include[]=specs'
    data = urllib.request.urlopen(url).read().decode()
    response = json.loads(data)
    partSpecs = [('', '')]
    for spec in response['specs']:
        partSpecs.append((response['specs'][spec]['metadata']['name'], response['specs'][spec]['display_value']))
    del partSpecs[0]
    partSpecs.insert(0, ('Manufacturer', response['brand']['name']))
    partSpecs.insert(0, ('Part Number', response['mpn']))
    self.techSpecsList.lists[0].configure(state=NORMAL)
    self.techSpecsList.lists[1].configure(state=NORMAL)
    self.techSpecsList.addTechSpec(partSpecs)


def octoSearch(master):
    url = "http://octopart.com/api/v3/parts/search"

    # NOTE: Use your API key here (https://octopart.com/api/register)
    url += "?apikey=1ef54ac1"
    searchString = master.searchQuery.get()
    startItem = 10 * (master.currentPage - 1)
    args = [
        ('q', searchString),
        ('include', 'short_description'),
        ('start', startItem),
        ('limit', 10)
    ]

    url += '&' + urllib.parse.urlencode(args)
    data = urllib.request.urlopen(url).read().decode()
    search_response = json.loads(data)
    if master.currentPage == 1:
        master.prevPageButton['state'] = DISABLED
        master.nextPageButton['state'] = NORMAL
    elif master.currentPage == master.maxPages:
        master.nextPageButton['state'] = DISABLED
        master.prevPageButton['state'] = NORMAL
    master.maxPages = math.ceil(search_response['hits'] / 10)
    master.pageNavigationLabel['text'] = 'Page {0} of {1}'.format(master.currentPage, master.maxPages)

    i = 0
    master.partList = [(' ', ' ')]
    # print results
    for result in search_response['results']:
        part = result['item']
        brandName = part['brand']['name']
        mpn = part['mpn']
        shortDescription = part['short_description']
        uid = part['uid']
        master.partList.append((mpn, brandName, shortDescription, uid))
        i = i + 1

    del master.partList[0]
    master.resultsList.addItem(master.partList)
