#!/usr/bin/env python
# encoding=utf-8

import codecs
import requests
import sqlite3
from bs4 import BeautifulSoup
ORIGINAL_URL='https://codeforces.ml'
DOWNLOAD_URL = 'https://codeforces.ml/problemset/status'


def download_page(url):
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }).content


def parse_html(html):
    soup = BeautifulSoup(html)
    movie_list_soup = soup.find('table', attrs={'class': 'status-frame-datatable'})
    submission_url = []
    submission_id  = []
    submission_color=[]
    submission_lang=[]
    submission_verdict=[]
    submission_time=[]
    submission_memory=[]
    submission_problem=[]
    rated=[]
    submission_runtime=[]
    submission_code=[]
    for movie_li in movie_list_soup.find_all('tr')[1:]:
       # print(movie_li)
        detail = movie_li.find('td', attrs={'class': 'id-cell'})
        submission_url.append(detail.a['href'])
        submission_code.append(get_code(ORIGINAL_URL+detail.a['href']))
        #print(get_code(ORIGINAL_URL+detail.a['href']))

        detail = movie_li.find('td', attrs={'class': 'status-small'})
        submission_time.append(detail.span.string)
        #处理一下两个分开的单词
        detail = movie_li.find('td', attrs={'class': 'status-party-cell'})
        rated.append(detail.a['class'][0])
        submission_color.append(detail.a['class'][1])

        detail=detail.find_next_sibling('td')
        submission_problem.append(detail.a['href'])

        detail = detail.find_next_sibling('td')
        #print(detail.string)
        submission_lang.append(detail.string)

        detail = detail.find_next_sibling('td')
        # 待解析！！！！！！！！！！！！！！！！1
        try:
            #print((detail.span.span['class']))
            submission_verdict.append(detail.span.span['class'])
        except TypeError:
            #print(['useless input'])
            submission_verdict.append(['useless input'])
        except  AttributeError:
            #print(['useless input'])
            submission_verdict.append(['useless input'])

        detail = detail.find_next_sibling('td')
        submission_runtime.append(detail.string)
        #print(detail.string)
   # print(soup)
   # next_page = soup.find('div', attrs={'class': 'pagination'})
    next_page=soup.find(lambda tag: tag.name=='a' and tag.get('class')==['arrow'] and tag.string=='→' )
   # next_page=next_page.find('a',attrs={'class','arrow'})
   # print(ORIGINAL_URL + next_page['href'])
    if next_page:
        return submission_url,submission_code,submission_lang,submission_verdict,submission_time,submission_runtime,rated,submission_color,ORIGINAL_URL + next_page['href']
    return submission_url,submission_code,submission_lang,submission_verdict,submission_time,submission_runtime,rated,submission_color,None


def insert_to_database(submission_url,submission_lang,submission_verdict,submission_time,submission_runtime,rated,submission_color):
    db=sqlite3.connect('database.db')

    return

def get_code(url):
    html = download_page(url)
    testsoup = BeautifulSoup(html)
    testsoup=testsoup.find('pre',attrs={'id':'program-source-text'})
    return testsoup.string
def test_db():
    #db = sqlite3.connect('database.db')
    #db.execute('''select datetime('now')''')
    return

def main():
    url = DOWNLOAD_URL
    while url:
        print(url)
        html = download_page(url)
        submission_url,submission_code,submission_lang,submission_verdict,submission_time,submission_runtime,rated,submission_color,url=parse_html(html)
        #insert_to_database( submission_url,submission_lang,submission_verdict,submission_time,submission_runtime,rated,submission_color)

if __name__ == '__main__':
    main()
