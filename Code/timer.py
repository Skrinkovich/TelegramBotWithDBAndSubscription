import time
import ast
import os


def updator(lisst):
    file = open("raspisanie_otpravok.txt", "w")
    file.write(str(lisst))
    file.close()


# процесс с ботом телеги. тут осуществляется проверка на наличие ошибки соединения, так как она ловится только тут. в main она за ошибку не считается.
def sender():  # в этой функции мы непосредственно коннектимся к тг и бд. делаем попытку отправить пост, пока не удастся

    import telebot
    import constants
    import time
    import functions
    thePost = None

    listOfSubs1 = functions.getUsers()
    bot = telebot.TeleBot(constants.token)

    for each in listOfSubs1:
        try:
            if each[4] - each[3] < 259200:
                bot.send_message(each[0], "ваша подписка закончится в течении трех дней")
            else:
                # print("ok")
                pass
        except:
            print("проблема с отправкой уведомления о заканчивающейся подписке юзеру")
            pass

    done_flag = False
    while done_flag == False:
        try:
            thePost = functions.poster()
            done_flag = True
        except:
            time.sleep(1)

    def sendddd(each, thePost):
        retry_limit = 2
        done_flag2 = False

        if thePost[2] != None or thePost[2] != "None":  # отправка текстового поста
            while done_flag2 == False:
                try:
                    bot.send_message(each[0], thePost[1])
                    done_flag2 = True
                    print("отпралено сообщение пользователю ", each[0], each[1])
                except Exception as e:
                    # print("each",each)
                    retry_limit-=1
                    if retry_limit < 0:
                        print('отправка сообщеня пользователю', each[0], each[1], 'не удалась.')
                        return True
                        break
                    print('проблема с отправкой сообщения ', each, "\n", e)
                    time.sleep(1)
            return True
        else:
            while done_flag2 == False:
                try:
                    print(thePost[2])
                    print(type(thePost[2]))
                    print(thePost[3])
                    bot.send_photo(each[0], thePost[2], thePost[1])
                    done_flag2 = True
                except Exception as e:
                    # print("each",each)
                    retry_limit -= 1
                    if retry_limit < 0:
                        print('отправка сообщеня пользователю', each[0], each[1], 'не удалась.')
                        return True
                        break
                    print('проблема с отправкой сообщения ', each, "\n", e)
                    time.sleep(1)
            return True

    if thePost == None:
        print("no post to post")
        bot.send_message(constants.owner, "нет поста на этот час для отправки подписчикам")
        pass
    else:
        for each in listOfSubs1:
            # print("______")
            # print(type(each))
            # print(each)
            try:
                sendddd(each, thePost)
            except Exception as e:
                print("sending file exception  ")
                print(each)
                print(e)
        bot.send_message(constants.owner, "пост из очереди был отправлен подписчикам")


# жутко намудрил, но он точно проверяет время отправки и наличие файла с часами отправки дополнительно
def process_creator(next_post, lisst):  # в этой функции мы делаем проверку на то, сейчас время или не время делать пост
    from time import sleep
    global listOfSubs
    lisst = lisst  # может это не правильно, но для надежности закрепил наличие переменных
    next_post = next_post
    start_time = time.time()

    file = open("vrema_rassylky.txt", "r")
    hh = file.readline()
    hh2 = int(file.readline())
    file.close()
    file = open("vrema_rassylky.txt", "w")
    file.write(str("False" + "\n" + str(int(hh2))))
    file.close()

    def timer(next_time1, lisst):
        raspis = None  # время постов. дублирует лисст, если он есть
        booler = False  # пора делать пост, или нет
        tim = time.localtime()
        hour = tim.tm_hour  # сейчас час
        next_hour = None  # следующий час из списка
        rer = False

        if os.path.exists("raspisanie_otpravok.txt") == False:
            tt = [9, 14, 20]
            file = open("raspisanie_otpravok.txt", "w")
            file.write(str(tt))
            file.close()
            raspis = tt
            rer = True
        if os.path.exists("raspisanie_otpravok.txt") == True:
            file = open("raspisanie_otpravok.txt", "r")
            LList = ast.literal_eval(file.read())
            print("расписание отправок: ",LList)
            raspis = LList
            rer = True

        if rer == False:
            raspis = lisst

        for index in range(len(raspis)):
            print(index, raspis[index])
            raspis[index] = int(raspis[index])

        def next_time(raspis, hour):
            if hour in raspis:
                next_hour = raspis.index(hour)
                try:
                    return raspis[next_hour + 1]
                except:
                    return raspis[0]
            for each in range(24):
                if each < hour:
                    continue
                if each in raspis:
                    return each
                if each == 23:
                    return raspis[0]
                if each == 24:
                    return raspis[0]

        next_hour = next_time(raspis, hour)
        print(raspis[0])
        print(type(raspis[0]))

        if hour in raspis:
            booler = True
            pass
        print("функция таймер вернула ",raspis, booler, next_hour, hour)
        return raspis, booler, next_hour, hour

    while True:

        raspis1, booler1, next_hour1, now = timer(next_post, lisst)
        lisst = raspis1
        if booler1 == True:  # если сейчас время для поста
            if next_post == now or next_post == None:  # если в этот час ещё не было поста или постов не было вообще
                # post = functions.poster()#вытащили пост
                # BOT! DO POST
                sender()

                # pr = Process(target=sender, args=())
                # pr.start()
                # pr.join()
                # pr.terminate()



                # time.sleep(35)
                import functions
                functions.usubscribeR()
                print("_________post made")

                #
                # print(start_time)
                end_time=int(time.time())

                # print(end_time)
                end_time = end_time - start_time
                # print(end_time)

                file = open("vrema_rassylky.txt", "r")
                hh = file.readline()
                hh2 = int(file.readline())
                print("hhhhhhhh in timer",hh,hh2)
                file.close()
                if end_time>int(hh2):
                    file = open("vrema_rassylky.txt", "w")
                    file.write(str("True" + "\n" + str(int(end_time) +2)))
                    file.close()
                else:
                    file = open("vrema_rassylky.txt", "w")
                    file.write(str("True" + "\n" + str(int(hh2))))
                    file.close()
                    pass



            else:
                print("time for post, but no")
        print("now", now)
        print("next_post", next_post)
        next_post = next_hour1  # переключили флажок
        sleep(3)


def runn():
    next_post = None
    lisst = [9, 15, 20]  # None
    process_creator(next_post, lisst)


if __name__ == '__main__':
    while True:
        try:
            runn()
        except:
            print('Main file exception')
            time.sleep(42)

