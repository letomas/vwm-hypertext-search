from urllib.request import urlopen
from urllib.error import URLError
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from collections import deque
import html2text
import json
import sys

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HypertextSearch.settings")

from hypertext_search.models import WebPage


def crawlAndCreateMatrix(start_url, number_to_scrape):
    try:
        isInt = int(number_to_scrape)
    except:
        exit(1)

    d = deque()
    d.append(start_url)

    crawled_links = []
    matrix_links = []
    data = {}
    unallowed_words = ["mailto:", "tel:", ".pdf"]

    headers = {
        'User-Agent':'Mozilla/5.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

    html2textObj = html2text.HTML2Text()
    html2textObj.ignore_links = True

    # crawler for the data to setup H_matrix and strings

    crawled_link_counter = 0

    while True:
        crawl_url = d[0]

        try:
            html = urlopen(crawl_url)
            bsObj = BeautifulSoup(html.read(), 'html.parser')
        except URLError as e:
            print(e, "could not scrape this url", crawl_url)

        if crawl_url not in matrix_links:
            matrix_links.append(crawl_url)

        data[crawl_url] = { 'links' :[], 'outlinksCount' : 0}

        crawl_url_content = html2textObj.handle(str(bsObj.find('body')))

        for link in bsObj.find_all('a'):
            reduced_link = link.get('href')

            if reduced_link is None:
                continue

            flag = False
            for unallowed_word in unallowed_words:
                if unallowed_word in reduced_link:
                    flag = True
                    break

            if flag:
                continue

            if "http" not in reduced_link:
                reduced_link=urljoin(crawl_url, reduced_link)

            if reduced_link in data[crawl_url]['links']:
                continue
            if crawl_url == reduced_link:
                continue

            if crawled_link_counter < number_to_scrape:
                if reduced_link not in crawled_links:
                    crawled_link_counter += 1
                    d.append(reduced_link)
                    crawled_links.append(reduced_link)
            data[crawl_url]['links'].append(reduced_link)

            if reduced_link not in matrix_links:
                matrix_links.append(reduced_link)

        data[crawl_url]['outlinksCount'] = len(data[crawl_url]['links'])
        data[crawl_url]['content'] = crawl_url_content

        d.popleft()

        if not d:
            break

    # setting up the H_matrix for page rank
    existing_keys = data.keys()
    count_of_matrix_links = len(matrix_links)
    H_matrix = [[0 for x in range(count_of_matrix_links)] for y in range(count_of_matrix_links)] 

    for i in range(count_of_matrix_links):
        current_row_link = matrix_links[i]

        if current_row_link in existing_keys:
            for j in range(count_of_matrix_links):
                current_column_link = matrix_links[j]
                if current_column_link in data[current_row_link]['links']:
                    H_matrix[i][j] = 1/data[current_row_link]['outlinksCount']
                else:
                    H_matrix[i][j] = 0
        else:
            for j in range(count_of_matrix_links):
                H_matrix[i][j] = 0

    for data_url in matrix_links:
        new_webpage = WebPage()
        new_webpage.url = data_url
        new_webpage.content = ''

        if data_url in data:
            if 'content' in data[data_url]:
                new_webpage.content = data[data_url]['content']

        new_webpage.save()

    return (matrix_links, H_matrix)
