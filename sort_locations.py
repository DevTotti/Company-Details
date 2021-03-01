import time, os, re, requests, logging
from requests.exceptions import Timeout
from bs4 import BeautifulSoup as bs
from bs4.element import Comment
from unidecode import unidecode
import unicodedata
import proxy_server
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

def get_backup_locations(startURL, contactus_link):
    contactus_link = absolute_url(startURL, contactus_link)

    print("Contactus_link",contactus_link)

    try:
        html_response = requests.get(contactus_link.lower(), headers = headers, proxies = proxy_hosts,  verify=False, timeout=30)  # MetaData.
    except :
        return {'error':'(409) page request forbidden'}

    code = html_response.status_code

    if str(code) == '200':

        print("status_code: ", html_response)

        contactus_info, page_text = text_from_html(html_response, 'contactus')  # MetaData.

    else:
        print("status_code: ",html_response)
        contactus_info, page_text= "",""


    print('FOUND LOCATIONS: ', contactus_link)
    print('-' * 100)

    return contactus_info




def absolute_url(startURL, link):
    if 'HTTP' not in link.upper():
        link = '/'.join([s_i for s_i in link.split('/') if s_i.lower() not in startURL.lower().split('/')])
        link = startURL.rstrip('/') + '/' + link.lstrip('/')
    if 'HTTP' not in link.upper():
        link = 'http://' + link
    return link


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



def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'header', 'title', 'meta', '[document]', 'footer', 'nav', 'x-topbar']:
        return False
    if isinstance(element, Comment):
        return False

    return True
