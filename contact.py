from requests import exceptions
import requests
import re


def get_phone(soup):
    numbers =  []
    text = soup.get_text()
    pattern = re.compile('\(\d{3}\)-\d{3}-\d{4}|\d{3}-\d{3}-\d{4}|\(\d{3}\) ?\d{3}-\d{4}|\d{3}.\d{3}.\d{4}')
    for number in pattern.findall(text):
        if number is None or number == '':
            continue
        if number not in numbers: numbers.append(number)
    return numbers

def get_email(soup):
    emails = []
    text = soup.get_text()
    pattern = re.compile('''(
                    [a-zA-Z0-9._%+-]+
                    @
                    [a-zA-Z0-9.-]+
                    \.[a-zA-Z]{2,4}
                    )''', re.VERBOSE)
    for email in pattern.findall(text):
        if email is None or email == '':
            continue
        if email not in emails: emails.append(email)
    return emails
