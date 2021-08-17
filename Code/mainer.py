def runnn():
    import time
    import re
    bot = telebot.TeleBot(constants.token)
    listOfSubs = functions.getUsers()
    listOfDeadSubs = functions.getDeadUsers()
    KeyWaitUsers1= functions.waitUsersGet()
    KeyWaitUsers =[]
    waitForPost = functions.waitForPostRead()
    replyToSubers = functions.replyToSubersRead()
    replyToDeadSubers = functions.replyToDeadSubersRead()

    for each in KeyWaitUsers1:# это просто перевод значений из строк базы данных внужные
        KeyWaitUsers.append(each[0])
    if waitForPost == "True":
        waitForPost = True
    else:
        waitForPost = False
    if replyToSubers == "True":
        replyToSubers = True
    else:
        replyToSubers = False
    if replyToDeadSubers == "True":
        replyToDeadSubers = True
    else:
        replyToDeadSubers = False

    # print(KeyWaitUsers)
    # print(type(KeyWaitUsers))
    # print(waitForPost)
    # print(type(waitForPost))


    def MakeValue(what, value):
        nonlocal waitForPost
        nonlocal replyToSubers
        nonlocal replyToDeadSubers
        if what == "waitForPost":
            waitForPost = value
        if what == "replyToSubers":
            replyToSubers = value
        if what == "replyToDeadSubers":
            replyToDeadSubers = value



    def globaler():# функция, которая решает проблему с недоступностью к переменных снаруж функции
        return waitForPost, replyToSubers, listOfSubs, replyToDeadSubers, listOfDeadSubs


    def updator(lisst):
        file = open("raspisanie_otpravok.txt", "w")
        file.write(str(lisst))
        file.close()

    def log(message, answer):
        from datetime import datetime
        print(datetime.now())
        print("сообщение от {0}{1}.id = {2}\n Текст= {3}".format(message.from_user.first_name,
                                                                 message.from_user.last_name, str(message.from_user.id),
                                                                 message.text))
        print(answer)

    @bot.message_handler(commands=['start'])
    def handle_start(message):
        if int(message.chat.id) == int(constants.owner):
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row("Добавить пост в очередь", "Написать подписчикам")
            user_markup.row("Получить ключи на 31 день", "Получить ключи на 93 дня")
            user_markup.row("просмотреть запланированные посты", "написать отписанным")
            user_markup.row("Статистика", "отменить действие", "/start", "/help")
            bot.send_message(message.from_user.id, "Добро пожаловать", reply_markup=user_markup)
            pass
        else:
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row("Оформить подписку", "Ввести ключ подписки", "Моя подписка", "/help")
            bot.send_message(message.from_user.id, "Добро пожаловать", reply_markup=user_markup)

    @bot.message_handler(commands=['stop'])
    def handle_stop(message):
        hide_markup = telebot.types.ReplyKeyboardRemove
        bot.send_message(message.chat.id, "Удачи!")

    @bot.message_handler(commands=['help'])
    def handle_help(message):

        if int(message.chat.id) != int(constants.owner):
            bot.send_message(message.chat.id, """Что умеет этот бот? www.eda-etoprosto.ru/botabout""")
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row("Оформить подписку", "Ввести ключ подписки", "Моя подписка", "/help")
            bot.send_message(message.from_user.id, "Добро пожаловать", reply_markup=user_markup)
        elif int(message.chat.id) == int(constants.owner):
            tt = "основные команды реализованы с помощью клавиатуры. если у вас нет клавиатуры, можете отправить /start\n" \
            "дополнительные команды - \n\n " \
            " 'Время' - Если вы захотите поменять расписание запланированных постов. отправьте 'Время' и нужные часы через запятую. Например 'Время 10,14,19' \n \n " \
            "'Удалить' - если вам нужно удалить пост из очереди. Отправьте  'Удалить 1', если хотите удалить пост который идет в очереди первым. \n" \
            "'Удалить 0', если вы хотите удалить последний пост. 'Удалить -1'-предпоследний и.т.д.\n" \
            "для удалиения пользователя отправьте 'Бан 1006130578', где цифры это его айди. их можно найти в сообщении между плками | |\n"
            bot.send_message(message.from_user.id, tt)

    @bot.message_handler(content_types=["text"])
    def messages(message):
        # если шлет владелец бота
        if int(message.chat.id) == int(constants.owner):
            waitForPost, replyToSubers, listOfSubs, replyToDeadSubers,listOfDeadSubs = globaler()
            def zatuchka (a, b):
                MakeValue(a, b)
                print("made", a, b)

            if message.reply_to_message != None:  # reply
                def no_repeat(message, gg):
                    pattern2 = r'(?<=\|)(\d+)(\|)'
                    idd = re.search(pattern2, gg)[0][0:-1]
                    bot.send_message(idd, message.text)
                #блоки трай нужны чтоб выбрать человека которому слать сообщение
                #функция ноу рипит непосредственно отправляет текст пользователю. она одна здесь, поскольку мы точно знаем, что пользователь слал текст
                try:
                    gg = (r'{}'.format(message.reply_to_message.text))#если ответ админа на текстовое сообщение
                    no_repeat(message,gg)
                except Exception as e:
                    print(e)
                try:
                    gg = (r'{}'.format(message.reply_to_message.caption))#если ответ админа на фото
                    no_repeat(message,gg)
                except Exception as e:
                    print(e)
            if message.reply_to_message == None:  # not reply
                if message.text == "отменить действие":
                    functions.waitForPostChange(False)
                    zatuchka("waitForPost", False)
                    functions.replyToSubersChange(False)
                    zatuchka("replyToSubers", False)
                    functions.replyToDeadSubersChange(False)
                    zatuchka("replyToDeadSubers", False)
                    bot.send_message(constants.owner, "отменено")
                    pass
                elif waitForPost == True:
                    time_ = time.time()
                    text = message.text
                    photos = None
                    audio = None
                    functions.add_post(time_, text, photos, audio)
                    functions.waitForPostChange(False)
                    zatuchka("waitForPost", False)
                    bot.send_message(constants.owner, "пост добавлен в очередь")

                elif replyToSubers == True:
                    listOfSubs = functions.getUsers()
                    for each in listOfSubs:
                        try:
                            bot.send_message(each[0], message.text)
                            print(each[0])
                        except:
                            continue
                    functions.replyToSubersChange(False)
                    zatuchka("replyToSubers", False)
                    bot.send_message(constants.owner, "Пост подписчикам отправлен")

                elif replyToDeadSubers == True:
                    listOfDeadSubs = functions.getDeadUsers()
                    for each in listOfDeadSubs:
                        try:
                            bot.send_message(each[0], message.text)
                            print(each[0])
                        except:
                            continue
                    functions.replyToDeadSubersChange(False)
                    zatuchka("replyToDeadSubers", False)
                    bot.send_message(constants.owner, "Пост отписчикам отправлен")

                elif message.text == "Статистика":

                    ls ="У вас подписчиков на сегодня: "+str(len(listOfSubs))+"\n"
                    ls = ls + "Подписчики в прошлом: " + str(len(listOfDeadSubs)) + "\n" + "\n"
                    for each in listOfSubs:
                        t1 = str(each[1])
                        t2 = str(each[2])

                        t4 = int(each[4])-time.time()
                        t5 = str(t4/60/60/24)
                        ls=ls+"Подписчик "+t1+" "+t2+" ещё "+t5+"дней  \n"
                        pass
                    bot.send_message(constants.owner, ls)
                    pass

                elif message.text.startswith("Удалить"):
                    try:
                        indexes = []
                        pattern = r"\d+"
                        indexes = re.findall(pattern, message.text)
                        ok = True
                        for each in indexes:
                            functions.deler(int(each))
                        if ok == True:
                            bot.send_message(constants.owner, "готово")
                    except:
                        bot.send_message(constants.owner, "не получилось удалить пост")

                elif message.text.startswith("Бан"):

                    pattern = r"\d+"
                    aidi = re.search(pattern, message.text)
                    print(aidi)
                    print(type(aidi))
                    try:
                        resul = functions.unsubscribeOOONE(int(aidi[0]))
                        if resul == True:
                            bot.send_message(constants.owner, "отписан")
                        else:

                            bot.send_message(constants.owner, "не получилось его удалить")
                    except:
                        print("smth got wrong with deling")
                        bot.send_message(constants.owner, "не получилось его удалить")




                elif message.text.startswith("Время"):
                    try:
                        times = []
                        pattern = r"\d+"
                        times = re.findall(pattern, message.text)
                        ok = True
                        for each in times:
                            if int(each) < 0 or int(each) > 23:
                                print("значение " + str(each) + ' не подходит')
                                bot.send_message(constants.owner, "значение " + str(each) + ' не подходит')
                                ok = False
                        if ok == True:
                            updator(times)
                            print("Новое время ", times)
                            bot.send_message(constants.owner, "Время отправки сообщений обновлено: " + str(times))
                    except:
                        bot.send_message(constants.owner, "не получилось обновить часы")


                elif message.text == "просмотреть запланированные посты":
                    # bot.send_message(constants.owner, "Напишите одним сообщением ваш пост")

                    posts = functions.get_posts()

                    for each in posts:

                        # try:
                        #     bot.send_photo(constants.owner, each[2], each[1])
                        # except Exception as e:
                        #     bot.send_message(constants.owner, "Exception" + str(e))
                        # try:
                        #     bot.send_message(constants.owner, each[1])
                        # except Exception as e:
                        #     bot.send_message(constants.owner, "Exception" + str(e))
                        if each[2]!=None:#для фото
                            # try:
                            bot.send_photo(constants.owner,each[2], each[1])
                            # except Exception as e:
                            #     bot.send_message(constants.owner, "Exception"+str(e))
                        elif each[2]==None:#для текст :
                            # try:
                            bot.send_message(constants.owner, each[1])
                            # except Exception as e:
                            #     bot.send_message(constants.owner, "Exception"+str(e))
                        else:
                            bot.send_message(constants.owner, "что-то не получилось ")
                    pass
                elif message.text == "Добавить пост в очередь":
                    bot.send_message(constants.owner, "Напишите одним сообщением ваш пост")
                    functions.waitForPostChange(True)
                    zatuchka("waitForPost", True)
                    pass
                elif message.text == "Написать подписчикам":
                    bot.send_message(constants.owner, "ожидаю письмо для подписчиков")
                    functions.replyToSubersChange(True)
                    zatuchka("replyToSubers", True)


                elif message.text == "написать отписанным":
                    bot.send_message(constants.owner, "ожидаю письмо для отписчиков")
                    functions.replyToDeadSubersChange(True)
                    zatuchka("replyToDeadSubers", True)

                elif message.text == "Получить ключи на 31 день":
                    file = functions.createKeys(31)
                    openFile = open(file, "rb")
                    bot.send_document(constants.owner, openFile)
                    openFile.close()
                    pass

                elif message.text == "Получить ключи на 93 дня":
                    file = functions.createKeys(93)
                    openFile = open(file, "rb")
                    bot.send_document(constants.owner, openFile)
                    openFile.close()
                    pass
                elif message.text == "Статистика":
                    bot.send_message(constants.owner, "пока не работает")
                    pass
                else:
                    bot.send_message(constants.owner, "Не понял вашу команду")
        #если шлет обычный юзер
        else:
            if message.text == "Оформить подписку":
                bot.send_message(message.chat.id,
                                 'Отлично! Страница, на которой вы сможете оформить подписку \nwww.eda-etoprosto.ru/bot')
            elif message.text == "Ввести ключ подписки":
                functions.waitUsersadd(message.chat.id)
                KeyWaitUsers.append(message.chat.id)
                # KeyWaitUsers = True
                print('user appended')
                bot.send_message(message.chat.id, 'Ожидаю от вас ключ. Если вы передумаете слать ключ, напишите "нет"')

            elif "нет" in message.text:
                try:
                    functions.waitUsersremove(message.chat.id)
                    KeyWaitUsers.pop(KeyWaitUsers.index(message.chat.id))
                except:
                    pass


            elif message.text == "Моя подписка":


                listOfSubs = functions.getUsers()
                actualnali = False
                for each in listOfSubs:
                    if message.chat.id == each[0]:
                        # print(each[4])
                        # print(time.time())
                        # print(each[4]-time.time())

                        t4 = int(each[4])-int(time.time())
                        t5 = str(t4 / 60 / 60 / 24)
                        # print(t5)
                        bot.send_message(message.chat.id,'Ваша подписка актуальна ещё '+ t5+" дней")
                        actualnali = True
                    else:
                        bot.send_message(message.chat.id, 'Ваша подписка не актуальна, однако вы можете её продлить. отправьте заново /start')
                        pass
                if actualnali== False:
                    bot.send_message(message.chat.id,'Ваша подписка не актуальна, однако вы можете её продлить. отправьте заново /start')

                # functions.waitUsersadd(message.chat.id)
                # KeyWaitUsers.append(message.chat.id)
                # # KeyWaitUsers = True
                # print('user appended')
                # bot.send_message(message.chat.id, 'Ожидаю от вас ключ. Если вы передумаете слать ключ, напишите "нет"')

            elif message.chat.id in KeyWaitUsers:
                try:
                    k = "ваш ключ не верен"
                    try:
                        hisKey = (r'{}'.format(message.text))
                        pattern2 = r'\d+'
                        k = re.search(pattern2, hisKey)[0]
                        repl = functions.activateKey(message.chat.id, message.chat.first_name, message.chat.username, k)
                        functions.waitUsersremove(message.chat.id)
                        bot.send_message(message.chat.id, repl)

                    except:
                        print("человек ввел в качестве ключа ",message.text)
                        KeyWaitUsers.pop(KeyWaitUsers.index(message.chat.id))
                        bot.send_message(message.chat.id, k)
                    pass
                except:
                    pass
                    # bot.send_message(message.chat.id, 'что-то не так. отправьте ключ ещё раз или "нет", если вы передумали')
                pass

            else:


                bot.send_message(constants.owner, str(message.chat.first_name) + ' |' + str(message.chat.id) + '| ' + ': \n' + message.text)

                # waitForPost, replyToSubers, listOfSubs, replyToDeadSubers, listOfDeadSubs = globaler()
                # print(listOfSubs)
                # for each in listOfSubs:
                #     if message.chat.id == each[0]:
                #         bot.send_message(constants.owner, str(message.chat.first_name) + ' |' + str(message.chat.id) + '| ' + ': \n' + message.text)
                #         print("sent to admin")
                #     else:
                #         user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                #         user_markup.row("Оформить подписку", "Ввести ключ подписки", "Моя подписка", "/help")
                #         bot.send_message(message.chat.id, """К сожалению у вас неактивна подписка. активировать её можно на странице \n www.eda-etoprosto.ru/botabout""", reply_markup=user_markup)

    @bot.message_handler(content_types=["photo"])
    def photo(message):
        # если шлет владелец бота
        if int(message.chat.id) == int(constants.owner):
            waitForPost, replyToSubers, listOfSubs, replyToDeadSubers,listOfDeadSubs = globaler()
            def zatuchka (a, b):
                MakeValue(a, b)
            if message.reply_to_message != None:  # reply
                def no_repeat(message, gg):
                    pattern2 = r'(?<=\|)(\d+)(\|)'
                    idd = re.search(pattern2, gg)[0][0:-1]
                    bot.send_photo(idd, message.photo[-1].file_id, message.caption)
                #блоки трай нужны чтоб выбрать человека которому слать сообщение
                #функция ноу рипит непосредственно отправляет текст пользователю. она одна здесь, поскольку мы точно знаем, что пользователь слал текст
                try:
                    gg = (r'{}'.format(message.reply_to_message.text))#если ответ админа на текстовое сообщение
                    no_repeat(message,gg)
                except Exception as e:
                    print(e)
                try:
                    gg = (r'{}'.format(message.reply_to_message.caption))#если ответ админа на фото
                    no_repeat(message,gg)
                except Exception as e:
                    print(e)

            if message.reply_to_message == None:  # not reply
                if waitForPost == True:
                    time_ = time.time()
                    text = message.caption
                    photos = message.photo[-1].file_id
                    audio = None
                    functions.add_post(time_, text, photos, audio)
                    functions.waitForPostChange(False)
                    zatuchka("waitForPost", False)
                    bot.send_message(constants.owner, "пост добавлен в очередь")

                elif replyToSubers == True:
                    listOfSubs = functions.getUsers()
                    for each in listOfSubs:
                        try:
                            bot.send_photo(each[0], message.photo[-1].file_id, message.caption)
                            print(each[0])
                        except:
                            continue
                    functions.replyToSubersChange(False)
                    zatuchka("replyToSubers", False)
                    bot.send_message(constants.owner, "Пост подписчикам отправлен")

                elif replyToDeadSubers == True:
                    listOfDeadSubs = functions.getDeadUsers()
                    for each in listOfDeadSubs:
                        try:
                            bot.send_photo(each[0], message.photo[-1].file_id, message.caption)
                            print(each[0])
                        except:
                            continue
                    functions.replyToDeadSubersChange(False)
                    zatuchka("replyToDeadSubers", False)
                    bot.send_message(constants.owner, "Пост отписчикам отправлен")


                else:
                    bot.send_message(constants.owner, "Не понял вашу команду")



        #если шлет обычный юзер
        else:
            if message.chat.id in KeyWaitUsers:
                try:
                    k = "я ожидаю от вас ключ"
                    print("человек отправил фото вместо ключа")
                    KeyWaitUsers.pop(KeyWaitUsers.index(message.chat.id))
                    bot.send_message(message.chat.id, k)
                    pass
                except:
                    pass
                    # bot.send_message(message.chat.id, 'что-то не так. отправьте ключ ещё раз или "нет", если вы передумали')
                pass

            else:
                bot.send_photo(constants.owner, message.photo[-1].file_id, str(message.chat.first_name) + ' |' + str(message.chat.id) + '| ' + ': \n' + str(message.caption))








    # Handles all sent documents and audio files
    @bot.message_handler(content_types=['voice'])
    def handle_docs_audio(message):
        # если шлет владелец бота
        if int(message.chat.id) == int(constants.owner):
            waitForPost, replyToSubers, listOfSubs, replyToDeadSubers, listOfDeadSubs = globaler()

            def zatuchka(a, b):
                MakeValue(a, b)

            if message.reply_to_message != None:  # reply
                def no_repeat(message, gg):
                    pattern2 = r'(?<=\|)(\d+)(\|)'
                    idd = re.search(pattern2, gg)[0][0:-1]
                    bot.send_voice(idd, message.voice.file_id, message.caption)

                # блоки трай нужны чтоб выбрать человека которому слать сообщение
                # функция ноу рипит непосредственно отправляет текст пользователю. она одна здесь, поскольку мы точно знаем, что пользователь слал текст
                try:
                    gg = (r'{}'.format(message.reply_to_message.text))  # если ответ админа на текстовое сообщение
                    no_repeat(message, gg)
                except Exception as e:
                    print(e)
                try:
                    gg = (r'{}'.format(message.reply_to_message.caption))  # если ответ админа на фото
                    no_repeat(message, gg)
                except Exception as e:
                    print(e)

            if message.reply_to_message == None:  # not reply
                if waitForPost == True:
                    bot.send_message(constants.owner, "отложенная отправка голосовых не поддерживается")
                elif replyToSubers == True:
                    listOfSubs = functions.getUsers()
                    for each in listOfSubs:
                        try:
                            bot.send_photo(each[0], message.voice.file_id, message.caption)
                            print(each[0])
                        except:
                            continue
                    functions.replyToSubersChange(False)
                    zatuchka("replyToSubers", False)
                    bot.send_message(constants.owner, "Пост подписчикам отправлен")

                elif replyToDeadSubers == True:
                    listOfDeadSubs = functions.getDeadUsers()
                    for each in listOfDeadSubs:
                        try:
                            bot.send_photo(each[0], message.voice.file_id, message.caption)
                            print(each[0])
                        except:
                            continue
                    functions.replyToDeadSubersChange(False)
                    zatuchka("replyToDeadSubers", False)
                    bot.send_message(constants.owner, "Пост отписчикам отправлен")
                else:
                    bot.send_message(constants.owner, "Не понял вашу команду")
        # если шлет обычный юзер
        else:
            if message.chat.id in KeyWaitUsers:
                try:
                    k = "я ожидаю от вас ключ"
                    print("человек отправил фото вместо ключа")
                    KeyWaitUsers.pop(KeyWaitUsers.index(message.chat.id))
                    bot.send_message(message.chat.id, k)
                    pass
                except:
                    pass
                pass

            else:

                bot.send_voice(constants.owner, message.voice.file_id, str(message.chat.first_name) + ' |' + str(message.chat.id) + '| ' )
        pass



    @bot.message_handler(content_types=['document'])
    def handle_text_doc(message):
        # print(message)
        # print(message.document)
        # print(message.caption)
        # print(message)
        # print(message)
        # если шлет владелец бота
        if int(message.chat.id) == int(constants.owner):
            waitForPost, replyToSubers, listOfSubs, replyToDeadSubers, listOfDeadSubs = globaler()
            def zatuchka(a, b):
                MakeValue(a, b)
            if message.reply_to_message != None:  # reply
                def no_repeat(message, gg):
                    pattern2 = r'(?<=\|)(\d+)(\|)'
                    idd = re.search(pattern2, gg)[0][0:-1]
                    bot.send_document(idd, message.document.file_id, message.caption)
                # блоки трай нужны чтоб выбрать человека которому слать сообщение
                # функция ноу рипит непосредственно отправляет текст пользователю. она одна здесь, поскольку мы точно знаем, что пользователь слал текст
                try:
                    gg = (r'{}'.format(message.reply_to_message.text))  # если ответ админа на текстовое сообщение
                    no_repeat(message, gg)
                except Exception as e:
                    print(e)
                try:
                    gg = (r'{}'.format(message.reply_to_message.caption))  # если ответ админа на фото
                    no_repeat(message, gg)
                except Exception as e:
                    print(e)

            if message.reply_to_message == None:  # not reply
                if waitForPost == True:
                    bot.send_message(constants.owner, "отложенная отправка документов сейчас не поддерживается")
                elif replyToSubers == True:
                    listOfSubs = functions.getUsers()
                    for each in listOfSubs:
                        try:
                            bot.send_document(each[0], message.document.file_id,None, message.caption)
                            print(each[0])
                        except:
                            continue
                    functions.replyToSubersChange(False)
                    zatuchka("replyToSubers", False)
                    bot.send_message(constants.owner, "Пост подписчикам отправлен")

                elif replyToDeadSubers == True:
                    listOfDeadSubs = functions.getDeadUsers()
                    for each in listOfDeadSubs:
                        try:
                            bot.send_document(each[0], message.document.file_id,None, message.caption)
                            print(each[0])
                        except:
                            continue
                    functions.replyToDeadSubersChange(False)
                    zatuchka("replyToDeadSubers", False)
                    bot.send_message(constants.owner, "Пост отписчикам отправлен")
                else:
                    bot.send_message(constants.owner, "Не понял вашу команду")
        # если шлет обычный юзер
        else:
            if message.chat.id in KeyWaitUsers:
                try:
                    k = "я ожидаю от вас ключ"
                    print("человек отправил фото вместо ключа")
                    KeyWaitUsers.pop(KeyWaitUsers.index(message.chat.id))
                    bot.send_message(message.chat.id, k)
                    pass
                except:
                    pass
                pass
            else:
                bot.send_document(constants.owner, message.document.file_id,None, str(message.chat.first_name) + ' |' + str(message.chat.id) + '| ' + ': \n' + str(message.caption))

        pass







    @bot.message_handler(content_types=['sticker'])
    def handle_text_doc(message):


        # если шлет владелец бота

        if int(message.chat.id) == int(constants.owner):
            waitForPost, replyToSubers, listOfSubs, replyToDeadSubers, listOfDeadSubs = globaler()
            def zatuchka(a, b):
                MakeValue(a, b)
            if message.reply_to_message != None:  # reply
                def no_repeat(message, gg):
                    pattern2 = r'(?<=\|)(\d+)(\|)'
                    idd = re.search(pattern2, gg)[0][0:-1]
                    bot.send_sticker(idd, message.sticker.file_id, message.caption)
                # блоки трай нужны чтоб выбрать человека которому слать сообщение
                # функция ноу рипит непосредственно отправляет текст пользователю. она одна здесь, поскольку мы точно знаем, что пользователь слал текст
                try:
                    gg = (r'{}'.format(message.reply_to_message.text))  # если ответ админа на текстовое сообщение
                    no_repeat(message, gg)
                except Exception as e:
                    print(e)
                try:
                    gg = (r'{}'.format(message.reply_to_message.caption))  # если ответ админа на фото
                    no_repeat(message, gg)
                except Exception as e:
                    print(e)

            if message.reply_to_message == None:  # not reply
                if waitForPost == True:
                    bot.send_message(constants.owner, "отложенная отправка стикеров сейчас не поддерживается")
                elif replyToSubers == True:
                    listOfSubs = functions.getUsers()
                    for each in listOfSubs:
                        try:
                            bot.send_sticker(each[0], message.sticker.file_id,None, message.caption)
                            print(each[0])
                        except:
                            continue
                    functions.replyToSubersChange(False)
                    zatuchka("replyToSubers", False)
                    bot.send_message(constants.owner, "Пост подписчикам отправлен")

                elif replyToDeadSubers == True:
                    listOfDeadSubs = functions.getDeadUsers()
                    for each in listOfDeadSubs:
                        try:
                            bot.send_sticker(each[0], message.sticker.file_id,None, message.caption)
                            print(each[0])
                        except:
                            continue
                    functions.replyToDeadSubersChange(False)
                    zatuchka("replyToDeadSubers", False)
                    bot.send_message(constants.owner, "Пост отписчикам отправлен")
                else:
                    bot.send_message(constants.owner, "Не понял вашу команду")



        # если шлет обычный юзер
        else:
            if message.chat.id in KeyWaitUsers:
                try:
                    k = "я ожидаю от вас ключ"
                    print("человек отправил фото вместо ключа")
                    KeyWaitUsers.pop(KeyWaitUsers.index(message.chat.id))
                    bot.send_message(message.chat.id, k)
                    pass
                except:
                    pass
                pass
            else:
                bot.send_sticker(constants.owner,message.sticker.file_id, str(message.chat.first_name) + ' |' + str(message.chat.id) + '| ' + ': \n' + str(message.caption))

        pass




    @bot.message_handler(content_types=['audio'])
    def handle_text_doc(message):
        # try:
        #     print(message)
        # except:
        #     pass
        # try:
        #     print(message.audio)
        # except:
        #     pass
        # try:
        #     print(message.caption)
        # except:
        #     pass
        # try:
        #     print(message.audio.file_id)
        # except:
        #     pass
        # try:
        #     print(message.chat.id)
        # except:
        #     pass

        # если шлет владелец бота

        if int(message.chat.id) == int(constants.owner):
            waitForPost, replyToSubers, listOfSubs, replyToDeadSubers, listOfDeadSubs = globaler()
            def zatuchka(a, b):
                MakeValue(a, b)
            if message.reply_to_message != None:  # reply
                def no_repeat(message, gg):
                    pattern2 = r'(?<=\|)(\d+)(\|)'
                    idd = re.search(pattern2, gg)[0][0:-1]
                    bot.send_audio(idd, message.audio.file_id, message.caption)
                # блоки трай нужны чтоб выбрать человека которому слать сообщение
                # функция ноу рипит непосредственно отправляет текст пользователю. она одна здесь, поскольку мы точно знаем, что пользователь слал текст
                try:
                    gg = (r'{}'.format(message.reply_to_message.text))  # если ответ админа на текстовое сообщение
                    no_repeat(message, gg)
                except Exception as e:
                    print(e)
                try:
                    gg = (r'{}'.format(message.reply_to_message.caption))  # если ответ админа на фото
                    no_repeat(message, gg)
                except Exception as e:
                    print(e)

            if message.reply_to_message == None:  # not reply
                if waitForPost == True:
                    bot.send_message(constants.owner, "отложенная отправка стикеров сейчас не поддерживается")
                elif replyToSubers == True:
                    listOfSubs = functions.getUsers()
                    for each in listOfSubs:
                        try:
                            bot.send_audio(each[0], message.audio.file_id,None, message.caption)
                            print(each[0])
                        except:
                            continue
                    functions.replyToSubersChange(False)
                    zatuchka("replyToSubers", False)
                    bot.send_message(constants.owner, "Пост подписчикам отправлен")

                elif replyToDeadSubers == True:
                    listOfDeadSubs = functions.getDeadUsers()
                    for each in listOfDeadSubs:
                        try:
                            bot.send_audio(each[0], message.audio.file_id,None, message.caption)
                            print(each[0])
                        except:
                            continue
                    functions.replyToDeadSubersChange(False)
                    zatuchka("replyToDeadSubers", False)
                    bot.send_message(constants.owner, "Пост отписчикам отправлен")
                else:
                    bot.send_message(constants.owner, "Не понял вашу команду")



        # если шлет обычный юзер
        else:
            if message.chat.id in KeyWaitUsers:
                try:
                    k = "я ожидаю от вас ключ"
                    print("человек отправил фото вместо ключа")
                    KeyWaitUsers.pop(KeyWaitUsers.index(message.chat.id))
                    bot.send_message(message.chat.id, k)
                    pass
                except:
                    pass
                pass
            else:
                bot.send_audio(constants.owner,message.audio.file_id, str(message.chat.first_name) + ' |' + str(message.chat.id) + '| ' + ': \n' + str(message.caption))

        pass

    @bot.message_handler(content_types=['video'])
    def handle_text_doc(message):
        # try:
        #     print(message)
        # except:
        #     pass
        # try:
        #     print(message.video)
        # except:
        #     pass
        # try:
        #     print(message.caption)
        # except:
        #     pass
        # try:
        #     print(message.video.file_id)
        # except:
        #     pass
        # try:
        #     print(message.chat.id)
        # except:
        #     pass

        # если шлет владелец бота

        if int(message.chat.id) == int(constants.owner):
            waitForPost, replyToSubers, listOfSubs, replyToDeadSubers, listOfDeadSubs = globaler()
            def zatuchka(a, b):
                MakeValue(a, b)
            if message.reply_to_message != None:  # reply
                def no_repeat(message, gg):
                    pattern2 = r'(?<=\|)(\d+)(\|)'
                    idd = re.search(pattern2, gg)[0][0:-1]
                    bot.send_video(idd, message.video.file_id, message.caption)
                # блоки трай нужны чтоб выбрать человека которому слать сообщение
                # функция ноу рипит непосредственно отправляет текст пользователю. она одна здесь, поскольку мы точно знаем, что пользователь слал текст
                try:
                    gg = (r'{}'.format(message.reply_to_message.text))  # если ответ админа на текстовое сообщение
                    no_repeat(message, gg)
                except Exception as e:
                    print(e)
                try:
                    gg = (r'{}'.format(message.reply_to_message.caption))  # если ответ админа на фото
                    no_repeat(message, gg)
                except Exception as e:
                    print(e)

            if message.reply_to_message == None:  # not reply
                if waitForPost == True:
                    bot.send_message(constants.owner, "отложенная отправка стикеров сейчас не поддерживается")
                elif replyToSubers == True:
                    listOfSubs = functions.getUsers()
                    for each in listOfSubs:
                        try:
                            bot.send_video(each[0], message.video.file_id,None, message.caption)
                            print(each[0])
                        except:
                            continue
                    functions.replyToSubersChange(False)
                    zatuchka("replyToSubers", False)
                    bot.send_message(constants.owner, "Пост подписчикам отправлен")

                elif replyToDeadSubers == True:
                    listOfDeadSubs = functions.getDeadUsers()
                    for each in listOfDeadSubs:
                        try:
                            bot.send_video(each[0], message.video.file_id,None, message.caption)
                            print(each[0])
                        except:
                            continue
                    functions.replyToDeadSubersChange(False)
                    zatuchka("replyToDeadSubers", False)
                    bot.send_message(constants.owner, "Пост отписчикам отправлен")
                else:
                    bot.send_message(constants.owner, "Не понял вашу команду")



        # если шлет обычный юзер
        else:
            if message.chat.id in KeyWaitUsers:
                try:
                    k = "я ожидаю от вас ключ"
                    print("человек отправил фото вместо ключа")
                    KeyWaitUsers.pop(KeyWaitUsers.index(message.chat.id))
                    bot.send_message(message.chat.id, k)
                    pass
                except:
                    pass
                pass
            else:
                bot.send_video(constants.owner,message.video.file_id, str(message.chat.first_name) + ' |' + str(message.chat.id) + '| ' + ': \n' + str(message.caption))

        pass



    # sendAudio
    # audio = open('/tmp/audio.mp3', 'rb')
    # bot.send_audio(message.chat.id, audio)
    # bot.send_audio(message.chat.id, "FILEID")
    #
    # ## sendAudio with duration, performer and title.
    # bot.send_audio(message.chat.id, file_data, 1, 'eternnoir', 'pyTelegram')
    #
    # # sendVoice
    # voice = open('/tmp/voice.ogg', 'rb')
    # bot.send_voice(message.chat.id, voice)
    # bot.send_voice(message.chat.id, "FILEID")
    #
    # # sendDocument
    # doc = open('/tmp/file.txt', 'rb')
    # bot.send_document(message.chat.id, doc)
    # bot.send_document(message.chat.id, "FILEID")
    #
    # # sendSticker
    # sti = open('/tmp/sti.webp', 'rb')
    # bot.send_sticker(message.chat.id, sti)
    # bot.send_sticker(message.chat.id, "FILEID")
    #
    # # sendVideo
    # video = open('/tmp/video.mp4', 'rb')
    # bot.send_video(message.chat.id, video)
    # bot.send_video(message.chat.id, "FILEID")
    #
    # # sendVideoNote
    # videonote = open('/tmp/videonote.mp4', 'rb')
    # bot.send_video_note(message.chat.id, videonote)
    # bot.send_video_note(message.chat.id, "FILEID")
    #
    # # sendLocation
    # bot.send_location(message.chat.id, lat, lon)


























# пересылка сообщения
# bot.send_photo(constants.owner,  message.photo[-1].file_id, message.caption)

    # print("Aaa")
    bot.polling(none_stop=False, interval=3, timeout=20)

if __name__ == '__main__':
    # listOfSubs = functions.getUsers()
    # waitForPost = False
    # replyToSubers = False

    # import urllib.request
    # import urllib.request
    # from bs4 import BeautifulSoup
    import re
    # import os
    import time
    # from threading import Thread
    # from multiprocessing import Process
    # import ast
    import telebot
    import constants
    import functions

    # runnn()
    while True:
        try:
            runnn()
            time.sleep(3)
        except:
            print('Main file exception')
            time.sleep(7)


    # next_post = None
    # lisst = [4, 14, 20]  # None
    # pr = Process(target=timer.process_creator, args=(next_post,lisst))
    # pr.start()
    # pr.join()
    # pr.terminate()


