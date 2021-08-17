import time

#весь файл нужен в качестве промежутка между базой данных основной программой
#он обеспечивает дополнительную безопасность на случай,  если ботапи захочет создать несколько потоков и каждый будет работать с бд
#склайт может работать только с одним потоком так что функции обеспечают это на случай, если к бд будут обращать одновремеи ничего не упадет
#+некоторая дополнительная обработка
#





# not_done_flag=False
# while not_done_flag==False:
#     try:
#         print("stuff done")
#         not_done_flag=True
#     except:
#         print('stuff not done. Waiting')
#         time.sleep(1)


# print()
# print(type())




# not_done_flag=False
# while not_done_flag==False:
#     try:
#         import db
#         not_done_flag=True
#     except:
#         print('importing not done. Waiting')
#         time.sleep(1)







def activateKey(id, first_name,username,k):
    not_done_flag = False
    retry_limit = 3
    while not_done_flag == False:
        try:
            import db
            start = int(time.time())
            bdreply = db.ActivateKey(id, first_name, username, start, k)
            bdreply = bdreply + "\n\nЧто умеет этот бот? www.eda-etoprosto.ru/botabout"
            db.printall()

            print("подписчик добавлен")
            not_done_flag = True
            return bdreply
        except:
            print('ключ подписчика неверный. ещё попытка')
            if retry_limit<0:
                return("ваш ключ не верен")
                break
            retry_limit-=1
            time.sleep(1)





def createKey(daes):
    not_done_flag = False
    while not_done_flag == False:
        try:
            import db
            print("stuff done")
            k = db.CreateKey(daes)
            not_done_flag = True

            return k
        except:
            print('stuff not done. Waiting')
            time.sleep(1)

def get_posts():
    not_done_flag = False
    while not_done_flag == False:
        try:
            import db
            print("stuff done")
            k = db.getAllPosts()
            not_done_flag = True
            return k
        except:
            print('stuff not done. Waiting')
            time.sleep(1)


def createKeys(daes):


    not_done_flag = False
    while not_done_flag == False:
        try:
            import db
            k = db.CreateKeys(daes, 10)
            # print(k)
            # print(len(k))
            name = "Keys{}d- Gen{}={} {}-{}-{}.txt".format(daes, time.localtime().tm_hour, time.localtime().tm_min,
                                                           time.localtime().tm_mday, time.localtime().tm_mon,
                                                           time.localtime().tm_year)
            file = open(name, "w")
            for each in k:
                file.write(str(each))
                file.write('\n')
            file.close()

            print("stuff done")
            not_done_flag = True

            return name
        except:
            print('stuff not done. Waiting')
            time.sleep(1)


# createKeys(10)

def unsubscribeOOONE(id):
    done = False
    try:
        import db
        db.unsubscribeONE(id)
        done = True
    except:
        print("deleting got bad")
    return done



def usubscribeR():

    try:
        import db
        unsubscribed = db.unsubscribeREGULAR(int(time.time()))
        print("удалиение старых подписчиков сделано")

        return unsubscribed
    except:
        print('удалиение старых подписчиков НЕ СДЕЛАНО')
#
# usubscribeR()


def Remind():
    pass

def deler(digit):
    not_done_flag = False
    while not_done_flag == False:
        try:
            import db
            aa = db.del_post(digit-1)
            # print("got post: ")
            not_done_flag = True
            return aa
        except Exception as e:
            print('could not get post from db')
            print(e)
            time.sleep(1)

    pass

# print(deler(1))
def poster():
    not_done_flag = False
    retry_limit = 4
    while not_done_flag == False:
        try:
            import db
            aa = db.DeleteAndGetPost()
            # print("got post: ")
            not_done_flag = True
            return aa
        except:
            print('could not get post from db')
            retry_limit -= 1
            if retry_limit < 0:
                print('Не получилось взять пост из бд. отбой')
                return None
                break
            time.sleep(1)

    pass

def add_post(time_, text_,photos,audio):
    not_done_flag = False
    while not_done_flag == False:
        try:
            import db
            db.addPost(time_, text_, photos, audio)
            print("stuff done")
            not_done_flag = True
        except:
            print('stuff not done. Waiting')
            time.sleep(1)
    pass



def getUsers():
    not_done_flag = False
    while not_done_flag == False:
        try:
            import db
            aaa = db.getAllSubs()

            print("stuff done")
            not_done_flag = True

            return aaa
        except:
            print('stuff not done. Waiting')
            time.sleep(1)

















def waitUsersGet():
    users = None
    not_done_flag = False
    while not_done_flag == False:
        try:
            import db
            users = db.waitUsersGet()
            print("stuff done")
            not_done_flag = True
        except:
            print('stuff not done. Waiting')
            time.sleep(1)



    return users
def waitUsersadd(id):
    not_done_flag = False
    while not_done_flag == False:
        try:
            import db
            db.waitUsersadd(id)
            print("stuff done")
            not_done_flag = True
        except:
            print('stuff not done. Waiting')
            time.sleep(1)

    pass
def waitUsersremove(id):
    not_done_flag = False
    while not_done_flag == False:
        try:
            import db
            db.waitUsersremove(id)
            print("stuff done")
            not_done_flag = True
        except:
            print('stuff not done. Waiting')
            time.sleep(1)

    pass

def waitForPostRead():
    not_done_flag = False
    waiters = None
    while not_done_flag == False:
        try:
            import db
            waiters = db.waitForPostRead()
            print("stuff done")
            not_done_flag = True
        except:
            print('stuff not done. Waiting')
            time.sleep(1)

    return waiters
    pass
def waitForPostChange(booler):
    not_done_flag = False
    while not_done_flag == False:
        try:
            import db
            db.waitForPostChange(booler)
            print("stuff done")
            not_done_flag = True
        except:
            print('stuff not done. Waiting')
            time.sleep(1)

    pass
def replyToSubersRead():
    not_done_flag = False
    waiters = None
    while not_done_flag == False:
        try:
            import db
            waiters = db.replyToSubersRead()
            print("stuff done")
            not_done_flag = True
        except:
            print('stuff not done. Waiting')
            time.sleep(1)

    return waiters
    pass
def replyToSubersChange(booler):
    not_done_flag = False
    while not_done_flag == False:
        try:
            import db
            db.replyToSubersChange(booler)
            print("stuff done")
            not_done_flag = True
        except:
            print('stuff not done. Waiting')
            time.sleep(1)

    pass



def replyToDeadSubersRead():
    not_done_flag = False
    waiters = None
    while not_done_flag == False:
        try:
            import db
            waiters = db.replyToDeadSubersRead()
            print("stuff done")
            not_done_flag = True
        except:
            print('stuff not done. Waiting')
            time.sleep(1)

    return waiters
    pass
def replyToDeadSubersChange(booler):
    not_done_flag = False
    while not_done_flag == False:
        try:
            import db
            db.replyToDeadSubersChange(booler)
            print("stuff done")
            not_done_flag = True
        except:
            print('stuff not done. Waiting')
            time.sleep(1)

    pass


def getDeadUsers():
    not_done_flag = False
    while not_done_flag == False:
        try:
            import db
            aaa = db.getAllDEADSubs()

            print("stuff done")
            not_done_flag = True

            return aaa
        except:
            print('stuff not done. Waiting')
            time.sleep(1)




# listOfSubs = db.getAllSubs()
#
#
# for each in listOfSubs:
#     print(each)