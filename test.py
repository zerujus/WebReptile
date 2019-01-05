# -*- coding : utf-8 -*-
import urllib.request
import re
import os
from concurrent.futures.thread import ThreadPoolExecutor
from urllib.parse import quote

from bs4 import BeautifulSoup


class Ebook():
    """init data"""

    def __int__(self, type, thread):
        self.info = 'Ebook'
        self.type = type
        self.book_list = []
        self.fileDir = 'D:\\EBook'
        self.max_thread = thread

    '''try url to web page'''

    def get_html(self, url):
        page = urllib.request.urlopen(url)
        return page.read().decode('utf-8', errors='replace')

    '''write data in file'''

    def write_booklist(self, file, booklist):
        pageFile = open(file, 'w')
        pageFile.write(booklist)
        pageFile.close()

    '''find book list in web page'''

    def analysis_booklist(self, htmlcode):
        print('start analysis_booklist')
        soup = BeautifulSoup(htmlcode, 'html.parser')
        book_target = soup.find_all('a', target='_blank')
        html_book_list = []
        for item in book_target:
            book_item = BeautifulSoup(str(item), 'html.parser')
            book_href = book_item.find('a').get('href')
            result = re.match('https://www.80txt.com(/\w+)+.html', book_href)
            if result:
                html_book_list.append(book_href)
        if html_book_list.__sizeof__() == 0:
            return None
        else:
            return html_book_list

    '''find download page in book item page'''

    def analysis_book(self, htmlcode):
        print('start analysis_book')
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
            if self.type == 0:
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
        print(str(book))
        book_down = self.analysis_book(book)
        if book_down:
            book_path = self.analysis_down(book_down)
            if book_path:
                self.download_file(book_path)

    '''search ebook by annunciation'''
    def bookList_annunciation(self, htmlcode):
        print('bookList_annunciation')
        pool = ThreadPoolExecutor(max_workers=self.max_thread)
        soup = BeautifulSoup(self.get_html(htmlcode), 'html.parser')
        slist = soup.find('div', id='slist')
        if slist is not None:
            bookList_introduction = slist.find_all('a', target='_blank')
            for book_introduction in bookList_introduction:
                pool.submit(self.thread_bookList, book_introduction.get('href'))


'''eBook = Ebook()
eBook.__int__(0)
pool = ThreadPoolExecutor(max_workers=7)
for i in range(0, 10):
    html = eBook.get_html('https://www.80txt.com/sort/' + str(i) + '.html')
    book_list = eBook.analysis_booklist(html)
    if not book_list is None:
        for book in book_list:
            pool.submit(eBook.thread_bookList, book)'''

Ebook = Ebook()
Ebook.__int__(0, 7)
Ebook.bookList_annunciation('https://www.80txt.com/sort/23.html')
