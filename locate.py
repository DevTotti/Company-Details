import usaddress as US
from ez_address_parser import AddressParser
import pyap
import requests
from requests import exceptions
from  bs4 import BeautifulSoup
import re

def get_page(url):
    try:
        html = requests.get(url).text
        soup = BeautifulSoup(html,'html.parser')
        raw_text = soup.get_text()
        page = re.sub('[^a-zA-Z0-9\.]', ' ', raw_text)
    except exceptions.MissingSchema:
        print('Empty URL')
    return page

def extract_pobox(page):
    pat = re.compile('(PO Box ?\n?.+ ?\n?.+ ?\n?,? ?[A-Z]{2} \d{5})')
    pat2 =re.compile('(PO Box ?\n?.+ ?\n?.+ [A-Z]{2} ?[A-Z]\d[A-Z] ?\d[A-Z]\d)')
    po_box= ' '.join(pat.findall(page))
    if po_box == ' ':
        po_box= ' '.join(pat2.findall(page))

    par = US.parse(po_box)
    po_box = [box[0] for box in par if box[1] == 'USPSBoxID']
    return po_box

def parse(page):
    country = ['US','CA']
    is_US =True
    locations =[]
    parsed= []
    address = pyap.parse(page, country=country[0])
    if address == []:
        is_US =False
        address = pyap.parse(page, country=country[1])

    for a in address:
        if a in parsed:
            continue
        else:
            parsed.append(a)
    for setter in parsed:
        if is_US:
            parsed = US.parse(str(setter))
        else:
            parsed = AddressParser().parse(str(setter))
        locations.append(parsed)
    return locations

class AddressSplit():
    def __init__(self,locations):
        self.locations = locations
    def street(self):
        tags = ['BuildingName','StreetNamePreDirectional','IntersectionSeperator',
        'AddressNumber','StreetName','StreetNamePostType','OccupancyType','OccupancyIdentifier',
        'StreetDirection','StreetType','StreetNumber']
        streets = []
        for loc in self.locations:
            streetname =''
            for pair in loc:
                if pair[1] in tags: streetname += pair[0] + ' ';
            
            if streetname not in streets: streets.append(streetname)
        return streets
        
    def zipcode(self):
        tag =['ZipCode','PostalCode']
        zips = []
        for loc in self.locations:
            for pair in loc:
                zipcode = ''
                if pair[1] in tag:
                    zipcode += pair[0]
                if zipcode != '':
                    if zipcode not in zips: zips.append(zipcode.replace(']',''));
        return zips

    def city(self):
        cities = []
        tag = ['PlaceName','Municipality']
        for loc in self.locations:
            for pair in loc:
                city = ''
                if pair[1] in tag:
                    city += pair[0]
                    if city in cities:
                        pass
                    elif city.upper() in cities:
                        pass
                    else:
                        cities.append(city)
        return cities

    def state(self):
        states = []
        tag = ['StateName','Province']
        for loc in self.locations:
            for pair in loc:
                state =''
                if pair[1] in tag:
                    state += pair[0]
                    if state not in states: states.append(state)
        return states
