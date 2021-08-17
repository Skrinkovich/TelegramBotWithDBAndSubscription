import sqlite3
import random
import time



def waitUsersGet():
    con = sqlite3.connect('teleBot.db')
    myCursor = con.cursor()
    users = []
    for each in myCursor.execute(f"SELECT * FROM KeyWaitUsers"):
        # print(each[0])
        # print(each)
        users.append(each)
    # print("losts",lostS)
    myCursor.close()
    con.close()
    return users
def waitUsersadd(id):
    print("waitUsersadd",id)
    con = sqlite3.connect('teleBot.db')
    myCursor = con.cursor()
    myCursor.execute(f"SELECT id_ FROM KeyWaitUsers WHERE id_ ='{id}'")
    if myCursor.fetchone() is None:
        myCursor.execute(f"INSERT INTO KeyWaitUsers VALUES (?)", (id,))
        con.commit()
    else:
        print("уже в списке ожидающих")
        # for each in myCursor.execute("SELECT * FROM subscribers"):
        #     print(each)
    myCursor.close()
    con.close()
    pass
def waitUsersremove(id):
    print("waitUsersremove",id)
    con = sqlite3.connect('teleBot.db')
    myCursor = con.cursor()
    myCursor.execute(f"DELETE FROM KeyWaitUsers WHERE id_ ='{id}' ")
    con.commit()
    myCursor.close()
    con.close()
    pass
def waitForPostRead():
    con = sqlite3.connect('teleBot.db')
    myCursor = con.cursor()
    myCursor.execute("""SELECT booler FROM waitForPost Where  id_ = 0 """)
    waiters = myCursor.fetchone()
    myCursor.close()
    con.close()
    return waiters[0]
    pass
def waitForPostChange(booler):
    con = sqlite3.connect('teleBot.db')
    myCursor = con.cursor()
    myCursor.execute(f"UPDATE waitForPost SET booler ='{booler}' WHERE id_ =0 ")
    con.commit()
    myCursor.close()
    con.close()
    pass
def replyToSubersRead():
    con = sqlite3.connect('teleBot.db')
    myCursor = con.cursor()
    myCursor.execute("""SELECT booler FROM replyToSubers Where  id_ = 0 """)
    waiters = myCursor.fetchone()
    myCursor.close()
    con.close()
    return waiters[0]
    pass
def replyToSubersChange(booler):
    con = sqlite3.connect('teleBot.db')
    myCursor = con.cursor()
    myCursor.execute(f"UPDATE replyToSubers SET booler ='{booler}' WHERE id_ =0 ")
    con.commit()
    myCursor.close()
    con.close()
    pass



def replyToDeadSubersRead():
    con = sqlite3.connect('teleBot.db')
    myCursor = con.cursor()
    myCursor.execute("""SELECT booler FROM replyToDeadSubers Where  id_ = 0 """)
    waiters = myCursor.fetchone()
    myCursor.close()
    con.close()
    return waiters[0]
    pass

def replyToDeadSubersChange(booler):
    con = sqlite3.connect('teleBot.db')
    myCursor = con.cursor()
    myCursor.execute(f"UPDATE replyToDeadSubers SET booler ='{booler}' WHERE id_ =0 ")
    con.commit()
    myCursor.close()
    con.close()
    pass





def add_sub(id, first_name,username,start,end,relevance):
    con = sqlite3.connect('teleBot.db')
    myCursor = con.cursor()

    myCursor.execute(f"SELECT id FROM subscribers WHERE id ='{id}'")
    if myCursor.fetchone() is None:
        myCursor.execute(f"INSERT INTO subscribers VALUES(?,?,?,?,?,?)", (id, first_name, username, start, end, relevance))
        print("подписчик ", first_name, " ", username, " добавлен в список подписчиков")
        myCursor.execute(f"DELETE FROM dead_subscribers WHERE id ='{id}' ")
        con.commit()

    else:
        print("подписка ещё активна")
        # for each in myCursor.execute("SELECT * FROM subscribers"):
        #     print(each)


    myCursor.close()
    con.close()



def unsubscribeONE(id):
    con = sqlite3.connect('teleBot.db')
    myCursor = con.cursor()



    user = None
    for each in myCursor.execute(f"SELECT * FROM subscribers WHERE id ='{id}'"):
        user=each
    myCursor.execute(f"SELECT id FROM dead_subscribers WHERE id ='{id}'")
    if myCursor.fetchone() is None:
        myCursor.execute(f"INSERT INTO dead_subscribers VALUES(?,?,?,?,?,?)", (user))
    myCursor.execute(f"DELETE FROM subscribers WHERE id ='{id}' ")
    con.commit()
    myCursor.close()
    con.close()
unsubscribeONE(1006130578)

def unsubscribeREGULAR(now):
    con = sqlite3.connect('teleBot.db')
    myCursor = con.cursor()


    lostS = []
    for each in myCursor.execute(f"SELECT * FROM subscribers WHERE end <='{now}'"):
        # print(each[0])
        # print(each)
        lostS.append(each)
    for rrr in lostS:
        myCursor.execute(f"INSERT INTO dead_subscribers VALUES(?,?,?,?,?,?)", (rrr))
        myCursor.execute(f"DELETE FROM subscribers WHERE id ='{rrr[0]}' ")
        con.commit()
    # print("losts",lostS)
    con.commit()
    myCursor.close()
    con.close()
    return lostS



def CreateKey(days):
    con = sqlite3.connect('teleBot.db')
    myCursor = con.cursor()


    # with sql.connect("database.db") as con:
    #     myCursor = con.cursor()
    def get_random_key():
        def r():
            return random.randint(42, 4242)
        return r() * r() + r()
    new_key = get_random_key()
    myCursor.execute(f"SELECT * FROM keys WHERE key ='{new_key}'")
    if myCursor.fetchone() is None:
        myCursor.execute(f"INSERT INTO keys VALUES(?,?)", (new_key, days*24*60*60))#2678400 = 1 month
        con.commit()
        # print("ключ",new_key," добавлен")
        pass
    else:
        print("такой ключ уже есть")

    # myCursor.close()
    # con.close()

    myCursor.close()
    con.close()
    return new_key
    pass




def CreateKeys(days,howMany):
    con = sqlite3.connect('teleBot.db')
    myCursor = con.cursor()
    keyList = []

    def get_random_key():
        return random.randint(42, 4242424242) + random.randint(42, 4242424242)

    for each in range(howMany):
        new_key = get_random_key()
        myCursor.execute(f"SELECT * FROM keys WHERE key ='{new_key}'")
        if myCursor.fetchone() is None:
            myCursor.execute(f"INSERT INTO keys VALUES(?,?)", (new_key, days*24*60*60))#2678400 = 1 month
            keyList.append(new_key)
            # print("ключ",new_key," добавлен")
            pass
        else:
            print("такой ключ уже есть")

    con.commit()
    myCursor.close()
    con.close()
    return keyList
    pass


def ActivateKey(id, first_name,username,start, key):#этот модуль надо будет жестко тестить
    con = sqlite3.connect('teleBot.db')
    myCursor = con.cursor()
    myCursor.execute(f"SELECT time FROM keys WHERE key ='{key}'")
    tt = myCursor.fetchone()[0]
    print("tt",tt)
    end = start+tt
    his_time = tt/60/60/24
    print(end)
    relevance = True
    myCursor.execute(f"SELECT * FROM subscribers WHERE id ='{id}'")
    if myCursor.fetchone() is None:
        myCursor.execute(f"DELETE FROM keys WHERE key ='{key}' ")


        myCursor.execute(f"SELECT id FROM subscribers WHERE id ='{id}'")
        if myCursor.fetchone() is None:
            myCursor.execute(f"INSERT INTO subscribers VALUES(?,?,?,?,?,?)",
                             (id, first_name, username, start, end, relevance))
            print("подписчик ", first_name, " ", username, " добавлен в список подписчиков")
            myCursor.execute(f"DELETE FROM dead_subscribers WHERE id ='{id}' ")
            con.commit()

        else:

            print("подписка ещё активна")



        con.commit()
    else:
        print("____________________else")
        myCursor.execute(f"SELECT end FROM subscribers WHERE id ='{id}'")
        user_end = myCursor.fetchone()[0]

        print("user_end",user_end)

        # print("key time ", tt)
        new_end = int(user_end)+int(tt)
        his_time = (new_end - start)/60/60/24
        print("new_end", new_end)
        myCursor.execute(f"UPDATE subscribers SET end ='{new_end}' WHERE     id ='{id}'")

        myCursor.execute(f"DELETE FROM keys WHERE key ='{key}' ")
        con.commit()
    ss = 'Спасибо, ваш ключ активирован, подписка закончится через '+ str(his_time)+" день"
    print(ss)
    myCursor.close()
    con.close()
    return ss
    pass





def getAllSubs():
    con = sqlite3.connect('teleBot.db')
    myCursor = con.cursor()

    myCursor.execute("""SELECT * from subscribers""")
    items = myCursor.fetchall()
    myCursor.close()
    con.close()
    return items
    pass

def getAllDEADSubs():
    con = sqlite3.connect('teleBot.db')
    myCursor = con.cursor()

    myCursor.execute("""SELECT * from dead_subscribers""")
    items = myCursor.fetchall()

    myCursor.close()
    con.close()
    return items
    pass



def printall():
    con = sqlite3.connect('teleBot.db')
    myCursor = con.cursor()

    print("keys")
    for each in myCursor.execute("SELECT * FROM keys"):
        print(each)
    print("subscribers")
    for each in myCursor.execute("SELECT * FROM subscribers"):
        print(each)
    print("dead_subscribers")
    for each in myCursor.execute("SELECT * FROM dead_subscribers"):
        print(each)
    print("post_que")
    for each in myCursor.execute("SELECT * FROM post_que"):
        print(each)
    print(waitUsersGet())
    print("replyToSubersRead", replyToSubersRead())
    print("waitForPostRead", waitForPostRead())
    print("replyToDeadSubers", replyToDeadSubersRead())

    myCursor.close()
    con.close()


def getAllPosts():
    con = sqlite3.connect('teleBot.db')
    myCursor = con.cursor()
    myCursor.execute("""SELECT * from post_que ORDER BY time""")
    posts = myCursor.fetchall()
    myCursor.close()
    con.close()
    # print(posts)
    return posts

def addPost(time_, text_,photos,audio):
    time_ = int(time_)
    con = sqlite3.connect('teleBot.db')
    myCursor = con.cursor()
    myCursor.execute(f"SELECT * FROM post_que WHERE time ='{time_}'")
    if myCursor.fetchone() is None:
        print("myCursor.fetchone()---------------------",myCursor.fetchone())
        myCursor.execute(f"INSERT INTO post_que VALUES(?,?,?,?)", (time_, text_,photos,audio,))
        con.commit()
        print("пост добавлен\n")
        pass
    else:
        print("такой пост уже есть")
        # for each in myCursor.execute("SELECT * FROM post_que"):
        #     print(each)
    myCursor.close()
    con.close()




#
# def DeleteAndGetPost():
#     con = sqlite3.connect('teleBot.db')
#     myCursor = con.cursor()
#
#     myCursor.execute("""SELECT * FROM post_que WHERE time = '1602247166.8811533'""")#'1602247166.8811533'""")
#     post = myCursor.fetchall()
#
#     print("post!!!!!!!!!!!!",post)
#     # print(post[0])
#     # print(type(post[0]))
#     print(type(post))
#     post = post
#     # post = post[0]
#
#     # post = 1602247166.8811533
#     myCursor.execute(f"""SELECT time,text_,photos,audio FROM post_que WHERE time LIKE MIN(time)""")
#
#     post1 = post#myCursor.fetchall()
#
#     print("post1-------------------",post1)
#     # myCursor.execute(f"DELETE FROM post_que WHERE time ='{post}' ")
#     # con.commit()
#     myCursor.close()
#     con.close()
#     print(post1)
#     return post1


# def DeleteLastPost():
#     con = sqlite3.connect('teleBot.db')
#     myCursor = con.cursor()
#
#     myCursor.execute("""SELECT MAX(time) from post_que""")
#     post = myCursor.fetchone()
#     # print(type(post[0]))
#     myCursor.execute(f"SELECT * FROM post_que WHERE time ='{post[0]}'")
#     post1 = myCursor.fetchone()
#     myCursor.execute(f"DELETE FROM post_que WHERE time ='{post[-1]}' ")
#
#     con.commit()
#     myCursor.close()
#     con.close()
#     return "последний пост удален"


#
# def DeleteAndGetPost():
#     con = sqlite3.connect('teleBot.db')
#     myCursor = con.cursor()
#     myCursor.execute("""SELECT MIN(time) from post_que""")
#     post = myCursor.fetchone()
#     # print(type(post[0]))
#     myCursor.execute(f"SELECT * FROM post_que WHERE time ='{post[0]}'")
#     post1 = myCursor.fetchone()
#     myCursor.execute(f"DELETE FROM post_que WHERE time ='{post[0]}' ")
#     con.commit()
#     myCursor.close()
#     con.close()
#     return post1

def del_post (number):
    try:
        number = int(number)
        con = sqlite3.connect('teleBot.db')
        myCursor = con.cursor()
        myCursor.execute("""SELECT * FROM post_que ORDER BY time""")
        post = myCursor.fetchall()
        print(post)
        print("-----")
        number = int(post[number][0])
        print(number)
        myCursor.execute(f"SELECT * FROM post_que WHERE time ='{number}'")
        post1 = myCursor.fetchone()
        myCursor.execute(f"DELETE FROM post_que WHERE time ='{number}' ")
        con.commit()
        myCursor.close()
        con.close()
        return post1
    except:
        return "не смог удалить пост. возможно вы указали номер поста, которого нет. Либо список постов пуст"



def DeleteAndGetPost():
        con = sqlite3.connect('teleBot.db')
        myCursor = con.cursor()
        myCursor.execute("""SELECT MIN(time) from post_que""")
        post = int(myCursor.fetchone()[0])
        # print(type(post[0]))
        myCursor.execute(f"SELECT * FROM post_que WHERE time ='{post}'")
        post1 = myCursor.fetchone()
        myCursor.execute(f"DELETE FROM post_que WHERE time ='{post}' ")
        con.commit()
        myCursor.close()
        con.close()
        return post1


if __name__ == '__main__':



    # https://www.conite.org/datatype3.html

    # import sqlite3

    # def getSubscribers():
    #     subscribers = {'user': {"id": 345373872, "first_name": "Vitaly", "username": "honoto"},
    #                    "subscription": {"start": 1600178518, "end": 1601478518, 'relevance': True}}
    #     return subscribers


    # # id = 345373872
    # id = 345374242342
    # first_name = "Vitaly"
    # username = "honoto"
    # start = 1600178518
    # end = 1701478518
    # relevance = True
    # time = 1601478519  # 1601478519


    # id = 345373872
    id = 1006130578
    first_name = "User_"
    username = "User_779"
    start = 1600178518
    end = 1701478518
    relevance = True
    time = 1601478519  # 1601478519



    post1 = "Hi There"
    post2 = "post2"


    print("База данных импортирована")
    con = sqlite3.connect('teleBot.db')  # connect us to the database and will let us execute the SQL statements
    myCursor = con.cursor()  # cursor is a method of the connection object

    # con = sqlite3.connect('teleBot.db')
    # myCursor = con.cursor()
    # con.commit()

    # myCursor.close()
    # con.close()

    myCursor.execute("""CREATE TABLE IF NOT EXISTS subscribers (
    id INTEGER,
    first_name TEXT,
    username TEXT,
    start INTEGER,
    end INTEGER,
    relevance INTEGER
    )""")
    myCursor.execute("""CREATE TABLE IF NOT EXISTS dead_subscribers (
    id INTEGER,
    first_name TEXT,
    username TEXT,
    start INTEGER,
    end INTEGER,
    relevance INTEGER
    )""")
    myCursor.execute("""CREATE TABLE IF NOT EXISTS post_que (
    time INTEGER,
    text_ TEXT,
    photos TEXT,
    audio TEXT
    )""")
    myCursor.execute("""CREATE TABLE IF NOT EXISTS keys (
    key INTEGER,
    time INTEGER
    )""")

    myCursor.execute("""CREATE TABLE IF NOT EXISTS KeyWaitUsers (
    id_ INTEGER
    )""")

    myCursor.execute("""CREATE TABLE IF NOT EXISTS waitForPost (
    id_ INTEGER,
    booler INTEGER
    )""")

    myCursor.execute("""CREATE TABLE IF NOT EXISTS replyToSubers (
    id_ INTEGER,
    booler INTEGER
    )""")

    myCursor.execute("""CREATE TABLE IF NOT EXISTS replyToDeadSubers (
    id_ INTEGER,
    booler INTEGER
    )""")

    # ЭТОТ КОД ЗАПУСТИТЬ ТОЛЬКО ПРИ СОЗДАНИИ БАЗЫ ДАННЫХ!!!!!!

    # myCursor.execute(f"INSERT INTO waitForPost VALUES (?,?)", (0,0))
    # myCursor.execute(f"INSERT INTO replyToSubers VALUES (?,?)", (0,0))
    # myCursor.execute(f"INSERT INTO replyToDeadSubers VALUES (?,?)", (0,0))


    con.commit()
    myCursor.close()
    con.close()








    #--------------------------------

    # add_sub(id, first_name, username, start, end, relevance)
    #
    #
    # printall()
    # print("======================")
    # time_, text_, photos, audio = 1602326103.9595494, 'postpostpostpostpostpost', 'AgACAgIAAxkBAAIHwV-BjlnanL2uENes69cxyJ-gB7p4AAJTsDEblN0AAUgHs-2OWpwZFDVbFZUuAAMBAAMCAAN5AANFBwUAARsE', None
    # time_, text_, photos, audio =  1602247166.8811533, 'ffffffffddddddddddddd', 'AgACAgIAAxkBAAIHp1-AWf3ZS33WcIw3D_2vi1fQMePeAAJRsDEblN0AAUjkeSDoDA6hmV3VE5UuAAMBAAMCAAN5AAMMDwUAARsE', None
    # addPost(time_, text_, photos, audio,)
    # print("======================")
    # printall()
    # print("======================")
    # # print('post!!!!!!!!!!!!!!!!!!!!!', DeleteAndGetPost())
    # print("======================")


    # printall()





    # for i in range(4):
    # add_sub(id, first_name,username,start,end,relevance)


    # addPost(int(time.time()),post1,"photos","audio" )
    # printall()



    # print(getAllPosts())

    # unsubscribeONE(id)
    # unsubscribeONE(1006130578)

    # h = DeleteAndGetPost()
    # print(h)

    #CreateKey(31)


    # ti = 1601478518
    # gg = unsubscribeREGULAR(ti)

    # printall()

    #_________________________


    # printall()
    # print("-1-")
    # k = CreateKey(31)
    # printall()
    # print("-2-")
    # activateKey(id, first_name,username,start,end,relevance, k)
    # printall()
    # print("-3-")
    # ti = 1601478518
    # gg = unsubscribeREGULAR(ti)
    # printall()
    # print("-4-")
    # k = CreateKey()
    # printall()
    # print("-5-")
    # activateKey(id, first_name,username,start,end,relevance, k)
    # printall()
    # print("-6-")




    # printall()
    # print("-1-")
    # k = CreateKey(31)
    # printall()
    # print("-2-")
    # activateKey(id, first_name,username,start, k)









    # replyToSubersChange(True)
    # print("replyToSubersRead",replyToSubersRead())


    # waitForPostChange(0)
    # print("waitForPostRead",waitForPostRead())

    # waitUsersadd("1233211111")
    # waitUsersremove("1233211111")

    # print(waitUsersGet())
# import time
# unsubscribeREGULAR(time.time())
# print(time.time())
printall()
