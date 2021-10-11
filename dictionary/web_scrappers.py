from typing import Optional, List

import requests
from bs4 import BeautifulSoup


def to_ascii(word: str) -> str:
    res = ''
    for letter in word:
        i = 'öäüÖÄÜß'.find(letter)
        if i == -1:
            res += letter
        else:
            res += 'oe ae ue Oe Ae Ue sz'.split()[i]
    return res


def duden_definitions(word: str) -> Optional[List]:
    base_url = 'https://www.duden.de/rechtschreibung/'
    url = base_url + to_ascii(word)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    if soup is None:
        return []
    all_bed_soup = soup.find(attrs={'id': 'bedeutungen'})
    if all_bed_soup is None:
        all_bed_soup = soup
    res = []
    for bed_soup in all_bed_soup.find_all(id=lambda x: x and 'bedeutung' in x.lower()):
        tag = bed_soup.find(attrs={'class': 'enumeration__text'})
        if tag is None:
            tag = bed_soup.find('p')
        if tag is not None:
            res.append(tag.text)
    return res

