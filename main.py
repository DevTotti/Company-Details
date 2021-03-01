from locate import AddressSplit, get_page, parse, extract_pobox
from contact import get_email, get_phone
from url import get_urls, form_soup
from meta_data import get_about_us, get_leadership_info
from company import get_social_media, fetch_title
import json
from geotext import GeoText
from commonregex import CommonRegex as cmg
# Company name, email, phone, social media, about us, leadership_info, address


next_to = {}

def run(url):
    result = []
    links = get_urls(url)
    # soups for links 1 and 2
    mini = 0
    for i in range(0,len(links)):
        if len(links[i])< len(links[mini]):
            mini = i
    ssh = form_soup(links[mini])
    ssc = form_soup(links[1])
    next_to['Company_Name'] = fetch_title(ssh)
    next_to['Email']= get_email(ssc)
    next_to['Phone']= get_phone(ssc)
    next_to['Social_media']= get_social_media(links[1])
    next_to['About_US']= get_about_us(links[0],ssh,next_to.get('Company_name'))
    next_to['Leadership']= get_leadership_info(links[0],ssh)
    next_to["PostalAddress"]= extract_pobox(get_page(links[1]))

    obj= parse(get_page(links[1]))
    
    ads = AddressSplit(obj)
    sortLocation(obj)


    if (next_to.get('Street_Name') == [] and
        next_to.get('City')==[] and
        next_to.get('State')==[] and
        next_to.get('PostalCode')==[]):
        # code here
        obj= parse(get_page(links[0]))

        ads = AddressSplit(obj)
        sortLocation(obj)


    if next_to.get('Email') ==[]: next_to['Email']= get_email(ssh)
    if next_to.get('Phone') ==[]: next_to['Phone']= get_phone(ssh)
    if next_to.get('Social_media') =={}: next_to['Social_media']= get_social_media(links[0])
    if next_to.get('PostalAddress') == '': next_to['PostalAddress'] =extract_pobox(get_page(links[0]))

    if len(next_to.get('PostalCode')) == 1 and len(next_to.get('City')) > 1:
         next_to['City'] = GeoText(' '.join(ads.city())).cities

    next_to['Street_Name'] = removePhone(next_to['Street_Name'])
    final_result = sort_Result(next_to)
    return final_result


def sortLocation(obj):

    ads = AddressSplit(obj)
    next_to['Street_Name'] = ads.street()
    next_to['City'] = ads.city()
    next_to['State'] = ads.state()
    next_to['PostalCode'] = ads.zipcode()




def removePhone(street_address):
    street_address_ = []
    for address in street_address:
        res = cmg(address)
        fpone = res.phones
        if fpone:
            for ii in fpone:
                address = address.replace(ii, "")
                street_address_.append(address)
        else:
            street_address_.append(address)

    
    return street_address_


def sort_Result(data):
    final_result = []

    streetName = data['Street_Name']
    if len(streetName) >= 1:

        for street in streetName:
            inds = streetName.index(street)

            extract = {}
            extract['Company_Name'] = data['Company_Name']
            extract['Email'] = data['Email']
            extract['Phone'] = data['Phone']
            extract['Social_media'] = data['Social_media']
            extract['About_US'] = data['About_US']
            extract['Phone'] = data['Phone']
            extract['Social_media'] = data['Social_media']
            extract['About_US'] = data["About_US"]
            extract['Leadership'] = data['Leadership']
            extract['PostalAddress'] = data['PostalAddress']
            extract['Street_Name'] = street
            try: extract['City'] = data['City'][inds]
            except: extract['City'] = ''
            try: extract['State'] = data['State'][inds]
            except: extract['State'] = ''
            try: extract['PostalCode'] = data['PostalCode'][inds] 
            except: extract['PostalCode'] = ''

            final_result.append(extract)



        return final_result

    else:
        return data