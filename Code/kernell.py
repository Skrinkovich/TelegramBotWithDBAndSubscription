import asyncio
import re
import time
import telebot
import time
import ast
import os
import constants

# import functions
import telebot
import constants
import time
from multiprocessing import Process
import subprocess
import os
import asyncio





if __name__ =='__main__':
    prev_time = 21

    while True:
        prev_time = time.localtime().tm_hour
        process = subprocess.Popen("python timer.py")
        time.sleep(25)
        process.terminate()
        print("рассылка окончена. возвращаемся к работе бота. ")


        process2 = subprocess.Popen("python mainer.py")
        while prev_time == time.localtime().tm_hour:
            time.sleep(1000)
        process2.terminate()
        prev_time = time.localtime().tm_hour
        print("работа обычного бота приостановлена для рассылки")




#===========================================================
    # os.system('python timer.py')
    # time.sleep(6)
    # print(os.popen('tasklist').readlines())
    # os.system("taskkill /f /im python3 timer.py")


    # process_creator(aa)
    # process_creator(mainn)





# async def foo():
#     while True:
#         print('Running in foo')
#         await asyncio.sleep(0)
#         print('Explicit context switch to foo again')
#
#
# async def bar():
#     while True:
#         print('Explicit context to bar')
#         await asyncio.sleep(0)
#         print('Implicit context switch back to bar')
#
#
# ioloop = asyncio.get_event_loop()
# tasks = [ioloop.create_task(foo()), ioloop.create_task(bar())]
# while True:
#     wait_tasks = asyncio.wait(tasks)
#     ioloop.run_until_complete(wait_tasks)
# # ioloop.close()

#
# def start():
#     import functions
#     listOfSubs = functions.getUsers()
#     return listOfSubs
#
#
# owner = constants.owner
# token = constants.token
# waitForPost = False
# replyToSubers = False
# KeyWaitUsers=[]
# listOfSubs = start()
#
#
# def bot(waitForPost,replyToSubers, KeyWaitUsers,listOfSubs, token, owner):
#     waitForPost, replyToSubers, KeyWaitUsers = mainer.runnn(waitForPost,replyToSubers, KeyWaitUsers,listOfSubs, token, owner)
#     return waitForPost, replyToSubers, KeyWaitUsers
#
#
#
#
# def regular():
#     while True:
#         print('Explicit context to bar')
#
#
#
# while True:
#     waitForPost, replyToSubers, KeyWaitUsers = bot(waitForPost,replyToSubers, KeyWaitUsers,listOfSubs, token, owner)
#     print("loop")
#     time.sleep(10)

#=============================================================



# import asyncio
#
# async def foo():
#     while True:
#         print('Running in foo')
#         await asyncio.sleep(0)
#         print('Explicit context switch to foo again')
#
#
# async def bar():
#     while True:
#         print('Explicit context to bar')
#         await asyncio.sleep(0)
#         print('Implicit context switch back to bar')
#
#
# ioloop = asyncio.get_event_loop()
# tasks = [ioloop.create_task(foo()), ioloop.create_task(bar())]
# while True:
#     wait_tasks = asyncio.wait(tasks)
#     ioloop.run_until_complete(wait_tasks)
# # ioloop.close()