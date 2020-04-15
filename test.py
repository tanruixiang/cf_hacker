#!/usr/bin/env python
# encoding=utf-8

"""
爬取豆瓣电影TOP250 - 完整示例代码
"""

import codecs

import requests
from bs4 import BeautifulSoup

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
    movie_name_list=[]
    for movie_li in movie_list_soup.find_all('tr')[1:]:
       # print(movie_li)
        detail = movie_li.find('td', attrs={'class': 'id-cell'})
        submission_url.append(detail.a['href'])

        detail = movie_li.find('td', attrs={'class': 'status-small'})
        submission_time.append(detail.span.string)
        #处理一下两个分开的单词
        detail = movie_li.find('td', attrs={'class': 'status-party-cell'})
        submission_url.append(detail.a['class'])

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
    next_page=soup.find(lambda tag: tag.name=='div' and tag.get('class')==['pagination'])
    next_page=next_page.find('a',attrs={'class','arrow'})
    if next_page:
        return movie_name_list, DOWNLOAD_URL + next_page['href']
    return movie_name_list, None


def main():
    url = DOWNLOAD_URL

    with codecs.open('movies', 'wb', encoding='utf-8') as fp:
        while url:
            html = download_page(url)
            data, url = parse_html(html)
            fp.write(u'{movies}\n'.format(movies='\n'.join(movies)))


if __name__ == '__main__':
    main()
