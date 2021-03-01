from bs4 import BeautifulSoup
import requests
import re
from requests import exceptions
import os


def get_urls(url):
    internal_urls = set()
    internal_urls.add(url)
    page = requests.get(url)
    try:
        soup = BeautifulSoup(page.text,'html.parser')
        for link in soup.find_all("a",text=re.compile('Contact',re.IGNORECASE)):
            new_url = link.get('href')
            if new_url.startswith('http'):
                internal_urls.add(new_url)
            else:
                new_url = url + new_url
                internal_urls.add(new_url)
    except(exceptions.MissingSchema,exceptions.InvalidSchema,TypeError):
        pass
    new = list(internal_urls)
    if len(new) == 1:
        new.append(url)
    return new

def form_soup(url):
    page =requests.get(url).text
    return BeautifulSoup(page,'html.parser')
