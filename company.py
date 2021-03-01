from bs4 import BeautifulSoup
import requests
from html_to_etree import parse_html_bytes
from extract_social_media import find_links_tree
import re
import os


def fetch_title(soup):
    title = soup.find('head').find('title').text
    for text in soup.stripped_strings:
        if '©' in text:
            text = re.sub(r'\s+', ' ', text)  # condense any whitespace
            text = text.split("©")[1]
            text = text.strip("©")
            text = text.replace("Copyright","")
            text = text.replace("All Rights Reserved","")
            try:
                year = parse(text, fuzzy=True).year
                if year:
                    text = text.replace(str(year), "")
                    companyName = text
                    companyName = companyName.replace(" - ","")
                    companyName = companyName.replace(" to ","")
            except:
                companyName = text
                companyName = companyName.replace(" - ","")
                companyName = companyName.replace(" to ","")
            return companyName
        else:
            try:
                confirm = True
                while confirm:
                    if "-" in title:
                        title = title.split(" - ")[0].strip()

                    elif "|" in title:
                        title = title.split("|")
                        print(title)
                        title = title[0].strip()

                    elif ".com" in title:
                        title = title.split(".com")
                        print(title)
                        title = title[0].strip()

                    elif "–" in title:
                        title = title.split("–")
                        print(title)
                        title = title[0].strip()
                    elif "\\n            " in title:
                        title = title.split("\\n            ")
                        print(title)
                        title = title[1].strip()
                    else:
                        confirm = False
                        title = title
                return title
            except Exception as error:
                title = 'Invalid Title'



def get_social_media(url):
    media= ['facebook','linkedin','twitter','youtube','github','google plus', 'pinterest','instagram',
            'snapchat','flipboard','flickr','weibo', 'periscope','telegram','soundcloud','feedburner',
            'vimeo','slideshare','vkontakte','xing']
    res = requests.get(url)
    social =dict()
    tree = parse_html_bytes(res.content, res.headers.get('content-type'))
    links = set(find_links_tree(tree))
    for i in range(len(media)):
        for link in links:
            if media[i] in link:
                social[media[i]] = link
    return social
