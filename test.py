# -*- coding : utf-8 -*-
import re
import os
import urllib
from concurrent.futures.thread import ThreadPoolExecutor
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup


class Ebook():
    """init data"""

    def __int__(self, type, thread):
        self.info = 'Ebook'
        self.type = type
        self.fileDir = 'D:\\EBook'
        self.pool = ThreadPoolExecutor(max_workers=thread)

    '''try url to web page'''

    def get_html(self, url):
        html = requests.get(url)
        html.encoding = 'utf-8'
        return html.text

    '''write data in file'''

    def write_booklist(self, file, booklist):
        pageFile = open(file, 'w')
        pageFile.write(booklist)
        pageFile.close()

    '''find download page in book item page'''

    def analysis_book(self, htmlcode):
        print('Book : ' + htmlcode)
        soup = BeautifulSoup(self.get_html(htmlcode), 'html.parser')
        module = soup.find_all('a', id='read_book')
        for item in module:
            web = item.get('href')
            result = re.match('(/\w+)+.html', web)
            if result:
                return 'http://www.80txt.com' + str(web)
        return None

    '''find download zip file in download page'''

    def analysis_down(self, htmlcode):
        print('start analysis_down')
        soup = BeautifulSoup(self.get_html(htmlcode), 'html.parser')
        down_list = soup.find_all('a', target='_blank')
        for download in down_list:
            if self.type == '1':
                result = re.match('https://\w+.80txt.com(/\w+)+/[^\x00-\xff]+.zip', download.get('href'))
                if result:
                    return download.get('href')
            else:
                result = re.match('https://\w+.80txt.com(/\w+)+/[^\x00-\xff]+.txt', download.get('href'))
                if result:
                    return download.get('href')
        return None

    '''download file in self.fileDir'''

    def download_file(self, filePath):
        fileName = filePath.split('/')[-1]

        if not os.path.exists(self.fileDir):
            os.makedirs(self.fileDir)
        if not os.path.exists(self.fileDir + '\\' + fileName.split('.')[0]):
            os.makedirs(self.fileDir + '\\' + fileName.split('.')[0])
            res = quote(fileName, encoding='utf-8')
            print('加载数据:' + fileName)
            data = urllib.request.urlopen(filePath.replace(fileName, res)).read()
            with open(self.fileDir + '\\' + fileName.split('.')[0] + '\\' + fileName, 'wb') as file:
                file.write(data)
            print('已下载:' + fileName)
        else:
            print('已存在:' + fileName.split('.')[0])

    def thread_bookList(self, book):
        book_down = self.analysis_book(book)
        if book_down:
            book_path = self.analysis_down(book_down)
            if book_path:
                self.download_file(book_path)

    '''search ebook by annunciation'''
    def bookList_annunciation(self, htmlcode):
        print('bookList_annunciation')
        soup = BeautifulSoup(self.get_html(htmlcode), 'html.parser')
        slist = soup.find('div', id='slist')
        if slist is not None:
            bookList_introduction = slist.find_all('a', target='_blank')
            for book_introduction in bookList_introduction:
                self.pool.submit(self.thread_bookList, book_introduction.get('href'))

    '''search ebook by recommend'''
    def bookList_recommend(self, htmlcode):
        print('bookList_recommend')
        soup = BeautifulSoup(self.get_html(htmlcode), 'html.parser')
        div = soup.find('div', id='tuijian')
        if div is not None:
            bookList = div.find_all('a')
            for a in bookList:
                result = re.match('https://\w+.80txt.com(/\w+)+.html', a.get('href'))
                if result:
                    self.pool.submit(self.thread_bookList, a.get('href'))

    def bookList_outOfOrder(self, htmlcode):
        print('bookList_outOfOrder')
        soup = BeautifulSoup(self.get_html(htmlcode), 'html.parser')
        div = soup.find_all('a')
        if div:
            for book in div:
                result = re.match('https://www.80txt.com(/\w+)+.html', book.get('href'))
                if result:
                    self.pool.submit(self.thread_bookList, book.get('href'))
                self.book_chooseAll(book.get('href'))

    def book_chooseAll(self, htmlcode):
        soup = BeautifulSoup(self.get_html(htmlcode), 'html.parser')
        div = soup.find_all('a')
        if div:
            for book in div:
                result = re.match('https://www.80txt.com(/\w+)+.html', book.get('href'))
                if result:
                    self.pool.submit(self.thread_bookList, book.get('href'))

print("欢迎使用小虫下载爬虫：")
book = Ebook()

val = input('请选择下载模式：\n 1:依据榜单下载\n 2:推荐下载\n 3:乱序下载\n')
type = input('请选择下载格式: \n 1.zip\n 2.txt\n')
thread = input('请输入开启线程数: ')
book.__int__(type, int(thread))
if val == '1':
    html = input('请输入榜单首页：\n')
    num = input('请输入爬取页数: \n')
    htmlspit = html[:-6]
    for i in range(1, int(num) + 1):
        s = htmlspit + str(i) + '.html'
        print(s)
        book.bookList_annunciation(htmlspit + str(i) + '.html')
elif val == '2':
    html = 'https://www.80txt.com/'
    book.bookList_recommend(html)
elif val == '3':
    html = 'https://www.80txt.com/'
    book.bookList_outOfOrder(html)


