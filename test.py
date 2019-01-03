# -*- coding : utf-8 -*-
import urllib.request
import re
from bs4 import BeautifulSoup


class Ebook():

    def __int__(self, type):
        self.info = 'Ebook'
        self.type = type

    def get_html(self, url):
        page = urllib.request.urlopen(url)
        return page.read().decode('utf-8', errors='replace')

    def write_booklist(self, file, booklist):
        pageFile = open(file, 'w')
        pageFile.write(booklist)
        pageFile.close()

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
        return html_book_list

    def analysis_book(self, htmlcode):
        print('start analysis_book')
        soup = BeautifulSoup(htmlcode, 'html.parser')
        module = soup.find_all('a', id='read_book')
        html_book_downs = []
        for item in module:
            web = item.get('href')
            result = re.match('(/\w+)+.html', web)
            if result:
                html_book_downs.append(web)
        return html_book_downs

    def analysis_down(self, htmlcode):
        print('start analysis_down')
        soup = BeautifulSoup(htmlcode, 'html.parser')
        downlist = soup.find_all('div', class_='pan_url')
        print(str(downlist))
        list = []
        for download in downlist:
            down_item = BeautifulSoup(str(download), 'html.parser')
            down_path = down_item.find('a').get('href')
            print(str(down_path))
            if self.type == 0:
                print(down_path[0])
                list.append(down_path[0])
            else:
                list.append(down_path[1])
        return list


eBook = Ebook()
eBook.__int__(0)
html = eBook.get_html('https://www.80txt.com/sort/89.html')
book_list = eBook.analysis_booklist(html)
print('book_list size ' + str(book_list.__sizeof__()))
download_htmlList = []
for book in book_list:
    print(str(book))
    book_web = eBook.get_html(book)
    download_list = eBook.analysis_book(book_web)
    for download in download_list:
        download_htmlList.append('http://www.80txt.com/' + str(download))
print(str(download_htmlList))

