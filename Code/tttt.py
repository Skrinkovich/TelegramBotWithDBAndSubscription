''''
пост про регулярки
https://habr.com/ru/post/349860/
тестер регулярок
https://regex101.com/r/
документация бс
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
'''




# пример использования флажка
# import time
# done_flag=False
# while done_flag==False:
#     try:
#         print("stuff done")
#         done_flag=True
#     except:
#         print('stuff not done. Waiting')
#         time.sleep(1)






#autorun
#C:\Users\wital\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup



import urllib.request
import urllib.request
from bs4 import BeautifulSoup
import re
import os
import time
#from threading import Thread
from multiprocessing import Process
import ast

vitalaChat = 345373872
nasyaChat = '377477531'
# url_link = 'http://mspvolga.ru/zakupki/'

#для тестов
#nasyaChat = 345373872
#url_link = "HTML_страница.html"


#универсальная функция для открытия страниц в интернете или на локальной машине в зависимости от названия.
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



def msp_volg_parser(url):

    html = get_html(url)
    soup = BeautifulSoup(html, features="html.parser")
    # print(soup.prettify())
    table1 = soup.find('div', class_="grid gap-md margin-top-md")
    offers = table1
    list = []
    pattern =  r'$'
    pattern1 =  r'\n'
    table1 = offers.find_all('h4')
    for each in table1:
        # print(each)
        link = each.find('a').get('href')#
        text = each.find('a').get_text()
        link =re.sub(pattern,' ', link, count=0)
        text =re.sub(pattern,' ', text, count=0)
        text =re.sub(pattern1,' ', text, count=0)
        list.append(text+'\n'+"http://mspvolga.ru"+link)
    return list




def cppvlg_parse(url):
    html = get_html(url)
    soup = BeautifulSoup(html, features="html.parser")
    # print(soup.prettify())
    table1 = soup.find(class_="items row")
    table2 = table1.find_all("div", class_="title")
    table3 = []
    for each in table2:
        link = each.find('a').get('href')
        text = each.find('a').get_text()
        # print(link)
        # print(text)
        table3.append(str(text+'\n'+"http://cppvlg.ru"+link))
    return table3

def ciss_parse(url):
    html = get_html(url)
    soup = BeautifulSoup(html, features="html.parser")
    # print(soup.prettify())
    table1 = soup.find_all("div", class_="col-lg-6 col-xl-4" )
    table3 = []
    # print(table1)
    for each in table1:
        link = each.find('a').get('href')
        # table3.append(link)
        head = each.find('h6', class_="header").get_text()
        # table3.append(head)
        text = each.find('div', class_="desc").get_text()
        table3.append(str(head)+"\n"+str(link)+"\n"+str(text))
    pattern2 = r'  +'
    pattern3 = r'\n'
    for each in table3:
        v1= re.sub(pattern3,r" ", each)
        table3[table3.index(each)] = re.sub(pattern2,r" ", v1)
    table4 =[]
    pattern4 = r'сбор'
    pattern5 = r'коммерч'
    pattern6 = r'предл'

    for each in table3:
        if re.search(pattern4, each, flags=re.IGNORECASE) or re.search(pattern5, each, flags=re.IGNORECASE) or re.search(pattern6, each, flags=re.IGNORECASE):
            table4.append(each)

    return table4




#проверка на то, прощло ли необходимое количество времени с момента прошлой отправки обновлений
def is_it_time():
    upd_period = 25000
    if os.path.exists("time_file.txt")==False:
        file = open("time_file.txt", "w")
        file.write(str(time.time()))
        file.close()
        print("created new time file")
        return True, upd_period
    else:
        file = open("time_file.txt", "r")
        last = float(file.read())
        now = time.time()
        file.close()
        if now-last>upd_period:
            file = open("time_file.txt", "w")
            file.write(str(now))
            file.close()
            print('it is time to get updates')
            return True, upd_period-(now-last)
        else:
            return False, upd_period-(now-last)


def get_prev_list(name):
    if os.path.exists(name)==False:
        file = open(name, "w")
        file.write(' ')
        file.close()
        print("created new offers file")
        return [' ']
    else:
        file = open(name, "r")
        LList = file.read()
        file.close()
        LList = ast.literal_eval(LList)#штука переводящая строку формата листа в лист
        return LList


def upd_last_offers(LList,which):
    file = open(which, "w")
    t = str(LList)
    file.write(t)
    file.close()



# процесс с ботом телеги. тут осуществляется проверка на наличие ошибки соединения, так как она ловится только тут. в main она за ошибку не считается.
def sender(id, text_list,waiting_time):
    import telebot
    sent = False#флажок

    def aa(id, text_list,waiting_time):
            try:
                for each in text_list:
                    bot = telebot.TeleBot("1349683616:AAGOPlMak-DrzUzrtUo_Szt1CBLecRhmuxM")
                    print(each)
                    bot.send_message(id, each)
                return True
            except:
                print("telegram bot connection  EXCEPTION. Waiting", "\n", ' ')
                time.sleep(waiting_time)
                print('retry')
                return False
    while sent==False:
        sent = aa(id, text_list,waiting_time)#так как интерпретатор питона сука умный, то он не поменяет переменную, ведь она не используется потом
        print("success of retry?: ",sent)#поэтому нужна эта строка
    print("terminated process", os.getpid())
    sent = False

# функция нужна, чтоб  создавать соедининение  с ботом отдельно от остальной программы и предотвращать нечаянное трогание телеграма. посколько тут процесс, то
# его в отличие от потока можно закрыть. даже импорт библиотеки происходит изолированно. без этого была ошибка
def process_creator(id,text,waiting_time):
    pr = Process(target=sender, args=(id,text,waiting_time))
    pr.start()
    pr.join()
    pr.terminate()


if __name__=='__main__':
    waiting_time = 300
    toSend_list = []

    print("program started")
    while True:
        t, tt = is_it_time()
        if t == True:



            def _work(waiting_time, site, file):
                retry_limit = 5
                not_done_flag=False
                send_list = []
                toSend_list = []
                while not_done_flag==False:
                    try:
                        list_offers = []
                        if file =="cppvlg.txt":
                            list_offers = cppvlg_parse(site)
                        if file == "mspvolga.txt":
                            list_offers = msp_volg_parser(site)
                        if file == 'ciss34.txt':
                            list_offers = ciss_parse(site)

                        old_list = get_prev_list(file)
                        send_list = list(set(list_offers) - set(old_list))
                        upd_last_offers(list_offers, file)
                        not_done_flag = True


                    except Exception as e:
                        print("site parsing exception: ", e, "\n" 'Retry in ', waiting_time / 60, " minutes")
                        time.sleep(waiting_time)
                        retry_limit-=1
                        if retry_limit<1:
                            not_done_flag = True

                if send_list == []:
                    print("notheing new at ", site)
                    pass
                else:
                    process_creator(nasyaChat, toSend_list, waiting_time)
                    process_creator(vitalaChat, send_list, waiting_time)
                    print(send_list)
                    print(site, ' sent')




            # def cppvlg_work(waiting_time):
            #     try:
            #         list_offers = cppvlg_parse('http://cppvlg.ru/news-and-events/news/')
            #         old_list = get_prev_list('cppvlg.txt')
            #         toSend_list = list(set(list_offers) - set(old_list))
            #         upd_last_offers(list_offers, "cppvlg.txt")
            #         return True, toSend_list
            #     except Exception as e:
            #         print("site parsing exception: ", e, "\n" 'Retry in ', waiting_time / 60, " minutes")
            #         time.sleep(waiting_time)
            #         return False, []
            #
            #
            # def mspvolga_work(waiting_time):
            #     try:
            #         list_offers = msp_volg_parser('http://mspvolga.ru/zakupki/')
            #         old_list = get_prev_list('mspvolga.txt')
            #         toSend_list=list(set(list_offers) - set(old_list))
            #         upd_last_offers(list_offers,"mspvolga.txt")
            #         return True, toSend_list
            #     except Exception as e:
            #         print("site parsing exception: ", e,"\n" 'Retry in ',waiting_time/60, " minutes" )
            #         time.sleep(waiting_time)
            #         return False, []

            # send_list = mspvolga_work(waiting_time)
            _work(waiting_time, 'http://cppvlg.ru/news-and-events/news/', 'cppvlg.txt')
            _work(waiting_time, 'http://mspvolga.ru/zakupki/', 'mspvolga.txt')
            _work(waiting_time, 'http://ciss34.ru/news', 'ciss34.txt')


        ttt = float('{:.1f}'.format(tt))
        print('main waiting ' + str(int(tt / 60)) + " minutes or ~ " + str( int(ttt / 60/ 60)) +  " hours untill update")
        time.sleep(waiting_time*6)

