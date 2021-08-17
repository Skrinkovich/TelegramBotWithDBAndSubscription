import sqlite3
import random
import time

#
# def unsubscribeONE(id):
#     con = sqlite3.connect('teleBot.db')
#     myCursor = con.cursor()
#     # myCursor.execute(f"DELETE FROM subscribers WHERE id ='{id}' ")
#     # myCursor.execute(f"DELETE * FROM subscribers WHERE id ='{id}' ")
#     # myCursor.execute("SELECT * FROM subscribers")
#     print("subscribers")
#     for each in myCursor.execute("SELECT * FROM subscribers"):
#         print(each)
#     print("dead_subscribers")
#     for each in myCursor.execute("SELECT * FROM dead_subscribers"):
#         print(each)
#     # if myCursor.fetchone() is None:
#     print(myCursor.fetchall())
#         # myCursor.execute(f"DELETE FROM keys WHERE key ='{key}' ")
#
#     con.commit()
#     myCursor.close()
#     con.close()
#
# def unsubscribeREGULAR(now):
#     con = sqlite3.connect('teleBot.db')
#     myCursor = con.cursor()
#     print("f")
#     # myCursor.execute(f"DELETE FROM subscribers WHERE end < '{now}' ")
#     lostS = []
#     for each in myCursor.execute(f"SELECT * FROM subscribers  WHERE end <='{int(now)}' "):
#         print(each[0])
#         print(each)
#         lostS.append(each)
#     for rrr in lostS:
#         myCursor.execute(f"INSERT INTO dead_subscribers VALUES(?,?,?,?,?,?)", (rrr))
#         myCursor.execute(f"DELETE FROM subscribers WHERE id ='{rrr[0]}' ")
#         con.commit()
#     print("losts",lostS)
#     con.commit()
#     myCursor.close()
#     con.close()


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




if __name__ == '__main__':






    # id = 345373872
    id = 1006130578
    # first_name = "User_"
    # username = "User_779"
    # start = 1600178518
    # end = 1701478518
    # relevance = True
    # time = 1601478519  # 1601478519

    # unsubscribeREGULAR(6801478518)
    print(time.time())
    unsubscribeONE(1006130578)






