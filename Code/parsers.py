''''
пост про регулярки
https://habr.com/ru/post/349860/
тестер регулярок
https://regex101.com/r/aGn8QC/2
документация бс
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
'''




import urllib.request
import re

def get_html(url):
    if bool(re.search('[а-яА-Я]', url)):
        response = open(url, encoding='utf-8').read()
        print("local_open")
        return response
    else:
        #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
        response = urllib.request.urlopen(url)#, headers)
        print("INTERNET_OPEN!")
        return response.read()