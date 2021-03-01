import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time, os, re, requests, logging
from requests.exceptions import Timeout
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from bs4.element import Comment
from unidecode import unidecode
import unicodedata
import proxy_server
from sort_locations import *
requests.packages.urllib3.disable_warnings()

headers = {
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
    }

# request_headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#                  'Accept-Encoding': 'deflate',
#                  'Accept-Language': 'en-US,en;q=0.8',
#                  'Connection': 'keep-alive',
#                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
#                 }

proxy_hosts = {
            "https":None,
            "http":None
            }


denied_domains = ["twitter.com", "m.facebook.com", "facebook.com", "linkedin.com", "google.com", "plus.google.com"]

def metaData_(startURL, response):

    contactus_inf, contact_inf_link = get_contactus(startURL, response)

    if contactus_inf == '' or contactus_inf == None:
        try:
            if contact_inf_link == '':
                pass

            contactus_inf = get_backup_locations(startURL, contactus_link)
        except:
            pass


    leadership_info = get_leadership_info(startURL, response)
    about_us_info = get_about_us(startURL, response, startURL)

    contactus_info_ = format_information(contactus_inf)
    leadership_info_ = format_information(leadership_info)
    aboutus_info_ = format_information(about_us_info)



    return [contactus_info_,contact_inf_link], leadership_info_, aboutus_info_


def format_information(information):


    if "not found" in information.lower():
        info_ = ''
        return info_

    else:
        info = information.replace(r'\t','').replace(r'\n','')
        info = info.replace(r'\b','').replace(r'\r','')
        info = info.replace('xa2','').replace('\\x80','')
        info = info.replace("\\xe2",'').replace("\\xc2",'')
        info = info.replace("\\xa0",'')
        info = info.replace("\\xa9",'').strip()
        info = info.replace("\\'s","'s")
        info = info.replace("\\x99", "'")
        info = info.replace("\\u003E","")
        info = info.replace("\\u0022","")
        info = info.replace("\\u003C","")
        info = info.replace("\\x9d","")
        info = info.replace("\\x84\\","")
        info = info.replace("\\x9c",'')
        info = info.replace("\\xae",'')
        info = info.replace("\\x93","")
        info = info.replace("\\x8b","")
        info = info.replace("\\xb2","")
        info = info.replace("\\ ","")
        info_ = info.encode('ascii','ignore')
        info_ = info_.decode()
    #print(info_)

        return info_




def get_leadership_info(startURL, response):
    print('LEADERSHIP >>>>> ',startURL)

    bs_inst_ = response

    patterns = [r'(.|\n)*(EXECUTIVE|MANAGEMENT)(.)?(TEAM|OFFICERS|COMMITTEE|BIOS)(\.)?(HTML|HTM|PHP|ASPX)?$', r'(.|\n)*(EXECUTIVE)(.)?(MANAGEMENT|TEAM|OFFICERS|COMMITTEE)(\.)?(HTML|HTM)?$',
                r'(.|\n)*(LEADERSHIP|TEAM|LEADERS)$',r'(.|\n)*(LEADERSHIP|TEAM|LEADERS|MANAGEMENT)(.)?(ASPX|PHP)$',r'(.|\n)*(LEADERSHIP|TEAM|LEADERS)(.)?(PROFILES)(.?)(HTML|ASPX)$',r'(.|\n)*(OFFICERS|BOARDS|BOARD)(.)?(.|\n)*(DIRECTORS)(.|\n)*',
                r'(.|\n)*(ORGANIZATION)(.)?(.|\n)*(EXECUTIVES)(.|\n)*']

    leadership_link, leadership_text = '', ''
    match_status = False
    for patt in patterns:
        for item in bs_inst_.find_all('a', href=True):
            #print(c_url)
            c_url = item['href'].upper().rstrip('/')
            #print(c_url)
            #print(c_url,re.search(patt, c_url))
            if re.search(patt, c_url) and not 'PORTFOLIO' in c_url:
                match_status = True
                leadership_link = item['href'].rstrip('/')
                print('Label Match (LEADERSHIP)', leadership_link, patt)
                break


    if match_status:

        leadership_link = absolute_url(startURL,leadership_link)

        print("Leadership_link ",leadership_link)

        try:
            html_response = requests.get(leadership_link.lower(), headers = headers,  proxies = proxy_hosts,  verify=False, timeout=30)
        except:
            return {'error':'(409) page request forbidden'}

        code = html_response.status_code

        if str(code) == '200':

            print("status_code: ", html_response)

            leadership_text,txt_ = text_from_html(html_response, "leadership")

        else:

            print("status_code: ",html_response)

            leadership_text,txt_, = "", ""

        print('FOUND LEADERSHIP: ', leadership_link)
        print('-' * 100)


    if leadership_link == '' or leadership_text == None:
        try:
            leadership_link = startURL+"/executive-management"
            try:
                response = requests.get(leadership_link.lower(), headers = headers, proxies = proxy_hosts, verify=False, timeout=30)
            except :
                return {'error':'(409) page request forbidden'}

            code = response.status_code

            if str(code) == '200':

                print("status_code: ", response)

                leadership_text,txt_ = text_from_html(response, "leadership")

            else:

                print("status_code: ",html_response)

                leadership_text,txt_, = "", ""

        except:
            leadership_text,txt_, = "", ""

    leadership_text = leadership_text.replace(r'\t','').replace(r'\n','')
    leadership_text = leadership_text.replace(r'\b','').replace(r'\r','')
    leadership_text = leadership_text.replace('xa2','').replace('\\x80','')
    leadership_text = leadership_text.replace("\\xe2",'').replace("\\xc2",'')
    leadership_text = leadership_text.replace("\\xa0",'')
    leadership_text = leadership_text.replace("\\xa9",'').strip()
    leadership_text = leadership_text.replace("\\'s","'s")
    leadership_text = leadership_text.replace("\\x99", "'")
    leadership_text = leadership_text.replace("\\u003E","")
    leadership_text = leadership_text.replace("\\u0022","")
    leadership_text = leadership_text.replace("\\u003C","")
    leadership_text = leadership_text.replace("\\x9d","")
    leadership_text = leadership_text.replace("\\x84\\","")
    leadership_text = leadership_text.replace("\\x9c",'')
    leadership_text = leadership_text.replace("\\xae",'')
    leadership_text = leadership_text.replace("\\x93","")
    leadership_text = leadership_text.replace("\\x8b","")
    leadership_text = leadership_text.replace("\\xb2","")
    leadership_text = leadership_text.replace("\\ ","")
    return leadership_text



def absolute_url(startURL, link):
    if 'HTTP' not in link.upper():
        link = '/'.join([s_i for s_i in link.split('/') if s_i.lower() not in startURL.lower().split('/')])
        link = startURL.rstrip('/') + '/' + link.lstrip('/')
    if 'HTTP' not in link.upper():
        link = 'http://' + link
    return link



def get_contactus(startURL,response):
    print("CONTACT US >>>>> ",startURL)
    bs_inst_ = response
    patterns = [r'(.|\n)*(CONTACT)(.)?(US|ME|INFORMATION)?(\.)?(HTML|HTM|ASPX)?$', '(.|\n)*(CONTACTS|CONTACT)$',
                r'(.|\n)*(CONNECT)(.)?(US|ME|INFORMATION)?(\.)?(HTML|HTM)?$']

    match_status,contactus_info = False, ''


    for patt in patterns:
        for item in bs_inst_.find_all('a', href=True):
            #print("Item here: ", item)
            c_url = item['href'].upper().rstrip('/')
            # print(c_url)
            if re.search(patt, c_url) and not re.search('(.|\n)*(FACILITIES)(.|\n)*',c_url):
                match_status = True
                contactus_link = item['href'].rstrip('/')
                break


    if not match_status:
        for item in bs_inst_.find_all('a', href=True):
            # ContactUS Extraction
            c_url = item['href'].rstrip('/')
            a_text = item.text.upper().rstrip('/').rstrip().replace(',','')
            #print(a_text)
            for patt in patterns:
                if re.search(patt, a_text):
                    match_status = True
                    contactus_link = c_url
                    print('Label Match (CONTACT US)', contactus_link, patt)
                    if item.has_attr('data-toggle') and c_url == '#':
                        match_status = False
                    else:
                        break
            if match_status: break


    if match_status:

        contactus_link = absolute_url(startURL, contactus_link)

        print("Contactus_link",contactus_link)

        try:
            html_response = requests.get(contactus_link.lower(), headers = headers, proxies = proxy_hosts,  verify=False, timeout=30)  # MetaData.
        except:
            return {'error':'(409) page request forbidden'}

        code = html_response.status_code

        if str(code) == '200':

            print("status_code: ", html_response)

            contactus_info, page_text = text_from_html(html_response, 'contactus')  # MetaData.

        else:
            print("status_code: ",html_response)
            contactus_info, page_text= "",""


        print('FOUND CONTACT US: ', contactus_link)
        print(contactus_info)
        print('-' * 100)


    if contactus_info == '' or contactus_info == ' ':
        for item in bs_inst_.find_all('a', href=True):

            c_url = item['href'].lower().rstrip('/')
            if "location" in c_url:
                contactus_info = get_backup_locations(startURL, c_url)


    return contactus_info, contactus_link


def contains_office_hrs(node_text):

    p_us_hour_range1 = r"(.|\n)*(?:(?:SUN|MON|TUE|WED|THU|FRI|SAT|SUNDAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY)\s*(-\s*(?:SUN|MON|TUE|WED|THU|FRI|SAT|SUNDAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY)?)?:?)?\s*[01]?\d(?::[012345]\d)?\s*[AP]\.?M\.?\s*-\s*[01]?\d(?::[012345]\d)?\s*[AP]\.?M\.?|[01]?\d(?::[012345]\d)?\s*[AP]\.?M\.?(.|\n)*"
    p_us_hour_range2 = r"\b(?:[01]?\d:[012345]\d\s*[AP]M\s*-\s*[01]?\d:[012345]\d\s*[AP]M|[01]?\d:[012345]\d\s*[AP]M)$"
    p_us_hour_range3 = r'(.|\n)*(\b(SUN|MON|TUE|WED|THU|FRI|SAT|SUNDAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY)\b)(.|n)*' #r'(.|\n)*(?:(?:SUN\b|MON\b|TUE\b|WED\b|THU\b|FRI\b|SAT\b|SUNDAY\b|MONDAY\b|TUESDAY\b|WEDNESDAY\b|THURSDAY\b|FRIDAY\b|SATURDAY\b)\s*(-\s*(?:SUN\b|MON\b|TUE\b|WED\b|THU\b|FRI\b|SAT\b|SUNDAY\b|MONDAY\b|TUESDAY\b|WEDNESDAY\b|THURSDAY\b|FRIDAY\b|SATURDAY\b)?)?:?)(.|\n)*'

    for patt in [p_us_hour_range1,p_us_hour_range2,  p_us_hour_range3]:
        if re.search(patt, node_text.upper()):
            break
            return True

    return False


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'header', 'title', 'meta', '[document]', 'footer', 'nav', 'x-topbar']:
        return False
    if isinstance(element, Comment):
        return False

    return True

def text_from_html(body,page):
    soup = bs(str(body.content), 'html.parser')
    #print("soupy")
    #print(soup)
    if page == 'leadership':
        for div in soup.find_all("div", {'class': 'x-topbar'}): div.decompose()
        for div in soup.find_all("section", {'id': 'nav'}): div.decompose()
        for div in soup.find_all("div", {'class': 'footer'}): div.decompose()
        for part in soup.find_all('', class_="copyright"): part.decompose()
        for part in soup.find_all('', class_="nav"): part.decompose()

    texts = soup.findAll(text=True)
    #print(texts)
    visible_texts = filter(tag_visible,texts)
    ttt = [t.strip() for t in visible_texts]
    return " ".join(ttt), ttt


def homepage_aboutus(startURL, response, companyName):
    aboutus_text = ''
    soup = bs(response.text, 'html.parser')
    for s in soup(['script', 'style']):
        s.decompose()
    if 'about us' in response.text.lower():
        # print('here!!!!')
        for div in soup.find_all("div"):
            if div.text not in aboutus_text and 'about' in div.text and companyName.lower() in div.text.lower():
                aboutus_text += div.text + '\n'
                break
            if div.text not in aboutus_text and div.has_attr('id') and (div['id'] in {'summary'}):
                aboutus_text += div.text + '\n'
            if div.text not in aboutus_text and div.has_attr('class'):
                if div.text not in aboutus_text and 'about' in ' '.join(div['class']) if isinstance(div['class'],list) else div['class']:
                    aboutus_text += div.text + '\n'


    if 'welcome to' in response.text.lower() and (remove_non_ascii(companyName.lower().replace('–','').strip()) in soup.text.lower() or 'our website' in response.text.lower() ):
        for div in soup.find_all("div"):
            if div.text not in aboutus_text and len(div.text) > 50 :
                aboutus_text += div.text + '\n'
        if aboutus_text == '':
            aboutus_text = filter(tag_visible, soup.find_all(text=True))
            aboutus_text = '\n'.join([t.strip() for t in aboutus_text])
    aboutus_text = aboutus_text.replace('\n\n','\n')
    return aboutus_text


def homepage_contactus(startURL, response):


    bs_inst_ = response.find("div", {"id": "contact-info"})
    if bs_inst_:
        contactus_text = bs_inst_.text

        return contactus_text
    else:
        contactus_text_ = ''
        bs_inst_ = response.find_all("address", {"class":"qhkvMe"})
        if bs_inst_:
            for data in bs_inst_:
                cp = data.find_all("div")
                for item in cp:

                    contactus_text = item.text
                    contactus_text_ = contactus_text_ + contactus_text + ' '

            return contactus_text_

        else:
            contactus_text_ = ''
            bs_inst_ = response.find_all("div", {"id":"comp-ikno7w01"})
            if bs_inst_:
                #print(bs_inst_)
                for data in bs_inst_:
                    cp = data.find_all("p")
                    for item in cp:
                        contactus_text = item.text
                        contactus_text_ = contactus_text_ + contactus_text + ' '

                return contactus_text_

            else:
                return ''



def remove_non_ascii(text):
    return unidecode(str(text))



def aboutus_helper(html_response):
    aboutus_bs_inst_ = bs(html_response.text, 'html.parser')

    aboutus_text = ''
    try:
        aboutus_bs_inst_.footer.decompose()
    except:
        pass
    for div in aboutus_bs_inst_.find_all("div", {'class': 'footer'}): div.decompose()
    for part in aboutus_bs_inst_.find_all('', class_="copyright"): part.decompose()
    #print('*'*100)
    #print(aboutus_bs_inst_)
    # for aboutus_bs_inst_ in aboutus_page_.find_all('div'):
    for content in aboutus_bs_inst_.find_all('p'):

        if ('"FOOTER"' in str(content.parent).upper() or 'Copyright' in content.text) and aboutus_text == ''  and '<!DOCTYPE html>' not in content.parent: continue
        if ('"FOOTER"' in str(content.parent).upper() or 'Copyright' in content.text) and aboutus_text != ''  and '<!DOCTYPE html>' not in content.parent:
            #print(content.text, content.parent)
            break
        # print(content.parent, content.text)
        # print('*!@' * 50)
        if len(content.text) > 50 and content.text not in aboutus_text:
            aboutus_text += content.text + '\n'
    if aboutus_text == '':
        for content in aboutus_bs_inst_.find_all('span'):
            if ('"FOOTER"' in str(content.parent).upper() or 'Copyright' in content.text) and aboutus_text == '' and '<!DOCTYPE html>' not in content.parent: continue
            if ('"FOOTER"' in str(content.parent).upper() or 'Copyright' in content.text) and aboutus_text != '' and '<!DOCTYPE html>' not in content.parent:
                break
            if len(content.text) > 50 and content.text not in aboutus_text:
                aboutus_text += content.text + '\n'
    if aboutus_text == '':
        for content in aboutus_bs_inst_.find_all('h2|h4'):
            if ('"FOOTER"' in str(content.parent).upper() or 'Copyright' in content.text) and aboutus_text == '' and '<!DOCTYPE html>' not in content.parent:continue
            if ('"FOOTER"' in str(content.parent).upper() or 'Copyright' in content.text) and aboutus_text != '' and '<!DOCTYPE html>' not in content.parent:
                break
            if len(content.text) > 50 and content.text not in aboutus_text:
                aboutus_text += content.text + '\n'
    if aboutus_text == '':
        for content in aboutus_bs_inst_.find_all("div"):
            if ('"FOOTER"' in str(content.parent).upper() or 'Copyright' in content.text) and aboutus_text == '' and '<!DOCTYPE html>' not in content.parent: continue
            if ('"FOOTER"' in str(content.parent).upper() or 'Copyright' in content.text) and aboutus_text != '' and '<!DOCTYPE html>' not in content.parent:
                break
            if len(content.text) > 50 and content.text not in aboutus_text:
                aboutus_text += content.text + '\n'

    return aboutus_text


def get_about_us(startURL, response, companyName):

    ignore_about_us = ['Please accept our apologies for the inconvenience', 'URL was not found on this server','You are being redirected',
                       'please contact the site owner','page you are looking for is not found',"Some pages you just can't reach",'The requested URL /about was not found on this server']
    about_us_patterns = [r'(.|\n)*(ABOUT)(.)?(US|ME)?(\.)(HTML)?$', r'(.|\n)*(ABOUT|ABOUTUS|ABOUTME|OURSTORY)$',
                         r'(.|\n)*(ABOUT)(.)?(US|ME)$', r'(.|\n)*((ABOUT)(.)(US|ME))(.)?(HTML)$',r'(.|\n)*((ABOUT)(.)(US|ME))(.)?(DEFAULT)(.)?(ASPX)$',
                         r'(.|\n)*((OUR)(.)?(STORY|WORK))$', r'(.|\n)*((COMPANY)(.)?(OVERVIEW|INFO))$', r'(.|\n)*((THE)(.)?(COMPANY|INFO))$',
                         r'(.|\n)*(ABOUT)(.)?(US|ME)(.)*(MISSION)*(VISION)(.|\n)*',
                         r'(.|\n)*(WHO)(.)?(WE)(.)?(ARE)(.|\n)*', r'(.|\n)*(WHAT)(.)?(WE)(.)?(DO)(.|\n)*']
    bs_inst_ = response
    about_us_link, aboutus_text = '', ''
    match_status = False
    for patt in about_us_patterns:
        for item in bs_inst_.find_all('a', href=True):
            c_url = item['href'].upper().rstrip('/')
            # print(c_url,item)
            flag = False
            for ii in denied_domains:
                if ii in c_url.lower(): flag = True
            if flag: continue
            if re.search(patt, c_url):
                match_status = True
                about_us_link = item['href'].rstrip('/')
                print(about_us_link, patt)
                break

        if match_status: break

    if not match_status:
        for item in bs_inst_.find_all('a', href=True):
            c_url = item['href'].upper().rstrip('/')
            flag = False
            for ii in denied_domains:
                if ii in c_url.lower(): flag = True
            if flag: continue
            try:
                for cn in companyName.split():
                    if cn in {'*','.'}:continue
                    patt = r'(.|\n)*(ABOUT|ABOUTUS|ABOUTME|OURSTORY)(.)?' + cn.upper() + '$'
                    #print(c_url,patt,companyName)
                    try:
                        if re.search(patt, c_url):
                            match_status = True
                            about_us_link = c_url
                            print(about_us_link, patt)
                            break
                    except:continue
            except:pass

    if not match_status:
        for item in bs_inst_.find_all('a', href=True):
            # LOB Extraction
            c_url = item['href'].rstrip('/')
            a_text = item.text.upper().rstrip('/').rstrip().replace(',','')
            #print(a_text)
            for patt in about_us_patterns:
                if re.search(patt, a_text):
                    match_status = True
                    about_us_link = c_url
                    print('Label Match (ABOUT US)', about_us_link, patt)
                    if item.has_attr('data-toggle') and c_url == '#':
                        match_status = False
                    else:
                        break
            if match_status: break
            try:
                for cn in companyName.split():
                    patt = r'(.|\n)*(ABOUT|ABOUTUS|ABOUTME|OURSTORY)(.)?' + cn.upper()
                    if re.search(patt, a_text):
                        match_status = True
                        about_us_link = c_url
                        print(about_us_link, patt)
                        break
            except:pass
    # print(match_status)
    if match_status:
        about_us_link1 = absolute_url(startURL, about_us_link)
        #print(about_us_link1)
        """Make sure you change/sort out the line below"""
        try:
            html_response = requests.get(about_us_link1.lower(), headers = headers, proxies = proxy_hosts,  verify=False, timeout=30)  # MetaData.
        except:
            return {'error':'(409) page request forbidden'}

        # print(html_response.text)
        aboutus_text = aboutus_helper(html_response)  # MetaData.

        for ignr in ignore_about_us:
            if ignr.lower() in aboutus_text.lower(): aboutus_text = ''

        if aboutus_text == '' :
            about_us_link = absolute_url(startURL, about_us_link)

            try:
                html_response = requests.get(about_us_link.lower(), headers = headers, proxies = proxy_hosts,  verify=False, timeout=30)
            except:
                return {'error':'(409) page request forbidden'}

            aboutus_text = aboutus_helper(html_response)

        print('FOUND ABOUT US: ', about_us_link)
        print('-' * 100)


    for ignr in ignore_about_us:
        if ignr.lower() in aboutus_text.lower():
            match_status = False
            aboutus_text = ''
    # print('aboutus_text>>>',aboutus_text)
    if str(aboutus_text) in {'','None'}:
        aboutus_text = homepage_aboutus(startURL, response, startURL)

    # print(startURL, match_status)
    if not match_status and aboutus_text == '':
        if 'HTTP' not in startURL.upper():
            about_us_link = 'http://' + startURL.lower() + '/about'
        else:
            about_us_link = startURL + '/about'
        # print(about_us_link.lower())
        try:
            html_response = requests.get(about_us_link.lower(), headers = headers, proxies = proxy_hosts,  verify=False, timeout=30)  # MetaData.
        except:
            return {'error':'(409) page request forbidden'}

        # print(html_response.text)
        if html_response.status_code == 200:
            print('Found ABOUT US: ', about_us_link)
            print('-' * 100)
            aboutus_text = aboutus_helper(html_response)  # MetaData.
            match_status = True


    if aboutus_text == '' :
        try:
            about_us_link = startURL + '/who-we-are'
            try:
                html_response = requests.get(about_us_link, headers = headers, proxies = proxy_hosts,  verify=False, timeout=30)
            except:
                return {'error':'(409) page request forbidden'}

            if html_response.status_code == 200:
                print('Found ABOUT US: ', about_us_link)
                print('-' * 100)
                aboutus_text = aboutus_helper(html_response)  # MetaData.
                match_status = True

        except:
            aboutus_text = ''
    aboutus_text = aboutus_text.replace(r'\t','').replace(r'\n','')
    aboutus_text = aboutus_text.replace(r'\b','').replace(r'\r','')
    aboutus_text = aboutus_text.replace('xa2','').replace('\\x80','')
    aboutus_text = aboutus_text.replace("\\xe2",'').replace("\\xc2",'')
    aboutus_text = aboutus_text.replace("\\xa0",'')
    aboutus_text = aboutus_text.replace("\\xa9",'').strip()
    aboutus_text = aboutus_text.replace("\\'s","'s")
    aboutus_text = aboutus_text.replace("\\x99", "'")
    aboutus_text = aboutus_text.replace("\\u003E","")
    aboutus_text = aboutus_text.replace("\\u0022","")
    aboutus_text = aboutus_text.replace("\\u003C","")
    aboutus_text = aboutus_text.replace("\\x9d","")
    aboutus_text = aboutus_text.replace("\\x84\\","")
    aboutus_text = aboutus_text.replace("\\x9c",'')
    aboutus_text = aboutus_text.replace("\\xae",'')
    aboutus_text = aboutus_text.replace("\\x93","")
    aboutus_text = aboutus_text.replace("\\x8b","")
    aboutus_text = aboutus_text.replace("\\xb2","")
    aboutus_text = aboutus_text.replace("\\ ","")
    return aboutus_text
