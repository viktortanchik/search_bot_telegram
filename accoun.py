import sqlite3
import asyncio
import time
# # from telethon.sync import TelegramClient
# # from telethon import functions, types
# # from telethon.errors import UsernameInvalidError
# # from telethon.errors import UsernameNotOccupiedError
# # #from telethon import errors
# # from db import sql_select_search,sql_update,con,sql_insert_all
# #
# #
# # def start_search():
# #     x = 4
# #     db = sqlite3.connect('Account.db')
# #     cur = db.cursor()
# #     cur.execute(f"SELECT PHONE FROM Account WHERE ID = '{x}'")
# #     time.sleep(0.4)
# #     Phone = str(cur.fetchone()[0])
# #     print("Входим в аккаунт: " + Phone, ' Номер ', x)
# #     cur.execute(f"SELECT API_ID FROM Account WHERE ID = '{x}'")
# #     time.sleep(0.4)
# #     api_id = str(cur.fetchone()[0])
# #     cur.execute(f"SELECT API_HASH FROM Account WHERE ID = '{x}'")
# #     time.sleep(0.4)
# #     api_hash = str(cur.fetchone()[0])
# #     session = str("anon" + str(x))
# #     client = TelegramClient(session, api_id, api_hash)
# #     client.start()
# #     time.sleep(2)
# #     return client
#
#
# async def main(search,client):
#     return await client(functions.contacts.SearchRequest(
#         q=search,
#         limit=5
#     ))
#

import grequests
from bs4 import BeautifulSoup
import requests
#from lxml import html
#url = 'http://mignews.com/mobile'

#url ='https://t.me/uniannet'
#url ='https://t.me/TBattSpeek'
#url ='https://t.me/hao1234bot'

# Асинхронн
###########################################################################################################################

class Get_info_url_grequests:
    async def info_url(self,urls):
        temp_data_db = ['', '', '', '', '', '', '']
        mess = ''
        # if url.find('?')>1:
        #     print(f'FIND Post!!{url}')
        #url = url.replace('/s/', '/')
        pa = (requests.get(url) for url in urls)
        pages = grequests.map(pa)
        soup = (BeautifulSoup(page.text, "html.parser") for page in pages)
        try:
            tb = soup.find('a', class_='tgme_action_button_new shine').text
            print('tb>>',tb)

            if tb == 'Send Message':
                letters = ['\n','`', '<', '>', '?', ':', ';', '"', "'", '[', ']', '{', '}', '&', '^', '%''']
                temp_name = soup.find('div', class_='tgme_page_title').text
                temp_name_db=''
                for i in letters:
                    temp_name = temp_name.replace(i, '')
                    temp_name_db=temp_name
                #print(soup.find('div', class_='tgme_page_title').text)

                #print(soup.find('a', class_='tgme_action_button_new shine').text)
                #print('Найден БОТ')

                nextline = 100
                step = (int(len(temp_name)) / nextline).__ceil__()
                temp_name_new = ''
                if step > 2:
                    #mes = ''
                    for x in range(step):
                        x = x + 1
                        print("X=", x)
                        mes = temp_name[((nextline * x) - nextline):nextline * x]
                        print(f'mes=={mes}')
                        if step != x:
                            temp_name_new += mes + '\n       '
                        else:
                            temp_name_new += mes
                elif step <= 2:
                    if len(temp_name) > nextline:
                        temp_name_new = (temp_name[:nextline - 1] + '\n       ' + (temp_name[nextline:]))
                    else:
                        temp_name_new = temp_name

                mess += ("🤖 " + "[" + temp_name_new + "]" + '(' + url + ')' + '\n\n')
                temp_data_db[0] += url
                temp_data_db[1] += temp_name_db
                temp_data_db[2] += 'bot'
            elif tb == 'View in Telegram':
                try:
                    #print(soup.find('a', class_='tgme_page_context_link').text)
                    #print('Найден канал')
                    letters = ['\n','`', '<', '>', '?', ':', ';', '"', "'", '[', ']', '{', '}', '&', '^', '%''']
                    temp_name = soup.find('div', class_='tgme_page_title').text
                    temp_name_db = ''
                    for i in letters:
                        temp_name = temp_name.replace(i, '')
                        temp_name_db = temp_name

                    nextline = 10
                    step = (int(len(temp_name)) / nextline).__ceil__()
                    temp_name_new=''
                    if step > 2:
                        #mes=''
                        for x in range(step):
                            x = x + 1
                            print("X=", x)
                            mes = temp_name[((nextline * x) - nextline):nextline * x]
                            print(f'mes=={mes}')
                            if step!=x:
                                temp_name_new += mes + '\n       '
                            else:
                                temp_name_new += mes

                            #temp_name_new = (temp_name[:nextline - 1] + '\n       ' + (temp_name[nextline:]))
                    elif step <= 2:
                        if len(temp_name) > nextline:
                            temp_name_new = (temp_name[:nextline - 1] + '\n       ' + (temp_name[nextline:]))
                        else:
                            temp_name_new = temp_name


                    mess += ("📢 " + '[' + temp_name_new + ']' + '(' + url + ')' + "\n\n")
                    temp_data_db[0] += url
                    temp_data_db[1] += temp_name_db
                    temp_data_db[2] += 'chanel'
                except AttributeError:
                    #print('Найден чат')
                    letters = ['\n','`', '<', '>', '?', ':', ';', '"', "'", '[', ']', '{', '}', '&', '^', '%''']
                    #print(soup.find('div', class_='tgme_page_title').text)

                    temp_name = soup.find('div', class_='tgme_page_title').text
                    temp_name_db = ''
                    for i in letters:
                        temp_name = temp_name.replace(i, '')
                        temp_name_db = temp_name

                    nextline = 10
                    step = (int(len(temp_name)) / nextline).__ceil__()
                    temp_name_new=''
                    if step > 2:
                        #mes=''
                        for x in range(step):
                            x = x + 1
                            print("X=", x)
                            mes = temp_name[((nextline * x) - nextline):nextline * x]
                            print(f'mes=={mes}')
                            if step!=x:
                                temp_name_new += mes + '\n       '
                            else:
                                temp_name_new += mes
                    elif step <= 2:
                        if len(temp_name) > nextline:
                            temp_name_new = (temp_name[:nextline - 1] + '\n       ' + (temp_name[nextline:]))
                        else:
                            temp_name_new = temp_name

                    mess += ("👥 " + '[' + temp_name_new + ']' + '(' + url + ')' + "\n\n")
                    temp_data_db[0] += url
                    temp_data_db[1] += temp_name_db
                    temp_data_db[2] += 'chat'
            return mess, temp_data_db
        except AttributeError:
            return False


    async def dele_letter(self,text):
        letters=['`','<','>','?',':',';','"',"'",'[',']','{','}','&','^','%''']
        for i in letters:
            text = text.replace(i,'')
        return text


###########################################################################################################################
async def req_ansyn(urls):
    response = (grequests.get(url) for url in urls)
    pages = grequests.map(response)
    temp_data_dbs = []
    mess = ''

    for page in pages:
        temp_data_db = ['', '', '', '', '', '', '']
        #print(page.url)
        soup = BeautifulSoup(page.text, "html.parser")
        #print(" page.url >>", page.url )
        try:
            tb = soup.find('a', class_='tgme_action_button_new shine').text
            #print('tb>>',tb)

            if tb == 'Send Message':
                letters = ['\n','`', '<', '>', '?', ':', ';', '"', "'", '[', ']', '{', '}', '&', '^', '%''']
                temp_name = soup.find('div', class_='tgme_page_title').text
                temp_name_db=''
                for i in letters:
                    temp_name = temp_name.replace(i, '')
                    temp_name_db=temp_name
                #print(soup.find('div', class_='tgme_page_title').text)

                #print(soup.find('a', class_='tgme_action_button_new shine').text)
                #print('Найден БОТ')

                nextline = 100
                step = (int(len(temp_name)) / nextline).__ceil__()
                temp_name_new = ''
                if step > 2:
                    #mes = ''
                    for x in range(step):
                        x = x + 1
                        #print("X=", x)
                        mes = temp_name[((nextline * x) - nextline):nextline * x]
                        #print(f'mes=={mes}')
                        if step != x:
                            temp_name_new += mes + '\n       '
                        else:
                            temp_name_new += mes
                elif step <= 2:
                    if len(temp_name) > nextline:
                        temp_name_new = (temp_name[:nextline - 1] + '\n       ' + (temp_name[nextline:]))
                    else:
                        temp_name_new = temp_name
                mess += ("🤖 " + "[" + temp_name_new + "]" + '(' + page.url + ')' + '\n\n')
                temp_data_db[0] += page.url
                temp_data_db[1] += temp_name_db
                temp_data_db[2] += 'bot'
                temp_data_dbs.append(temp_data_db)
            elif tb == 'View in Telegram':
                try:
                    #print(soup.find('a', class_='tgme_page_context_link').text)
                    #print('Найден канал')
                    letters = ['\n','`', '<', '>', '?', ':', ';', '"', "'", '[', ']', '{', '}', '&', '^', '%''']
                    temp_name = soup.find('div', class_='tgme_page_title').text
                    temp_name_db = ''
                    for i in letters:
                        temp_name = temp_name.replace(i, '')
                        temp_name_db = temp_name
                    nextline = 100
                    step = (int(len(temp_name)) / nextline).__ceil__()
                    temp_name_new=''
                    if step > 2:
                        #mes=''
                        for x in range(step):
                            x = x + 1
                            #print("X=", x)
                            mes = temp_name[((nextline * x) - nextline):nextline * x]
                            #print(f'mes=={mes}')
                            if step!=x:
                                temp_name_new += mes + '\n       '
                            else:
                                temp_name_new += mes
                            #temp_name_new = (temp_name[:nextline - 1] + '\n       ' + (temp_name[nextline:]))
                    elif step <= 2:
                        if len(temp_name) > nextline:
                            temp_name_new = (temp_name[:nextline - 1] + '\n       ' + (temp_name[nextline:]))
                        else:
                            temp_name_new = temp_name
                    mess += ("📢 " + '[' + temp_name_new + ']' + '(' + page.url + ')' + "\n\n")
                    temp_data_db[0] += page.url
                    temp_data_db[1] += temp_name_db
                    temp_data_db[2] += 'chanel'
                    temp_data_dbs.append(temp_data_db)
                except AttributeError:
                    #print('Найден чат')
                    letters = ['\n','`', '<', '>', '?', ':', ';', '"', "'", '[', ']', '{', '}', '&', '^', '%''']
                    #print(soup.find('div', class_='tgme_page_title').text)

                    temp_name = soup.find('div', class_='tgme_page_title').text
                    temp_name_db = ''
                    for i in letters:
                        temp_name = temp_name.replace(i, '')
                        temp_name_db = temp_name
                    nextline = 100
                    step = (int(len(temp_name)) / nextline).__ceil__()
                    temp_name_new=''
                    if step > 2:
                        #mes=''
                        for x in range(step):
                            x = x + 1
                            #print("X=", x)
                            mes = temp_name[((nextline * x) - nextline):nextline * x]
                            #print(f'mes=={mes}')
                            if step!=x:
                                temp_name_new += mes + '\n       '
                            else:
                                temp_name_new += mes
                    elif step <= 2:
                        if len(temp_name) > nextline:
                            temp_name_new = (temp_name[:nextline - 1] + '\n       ' + (temp_name[nextline:]))
                        else:
                            temp_name_new = temp_name
                    mess += ("👥 " + '[' + temp_name_new + ']' + '(' + page.url + ')' + "\n\n")
                    temp_data_db[0] += page.url
                    temp_data_db[1] += temp_name_db
                    temp_data_db[2] += 'chat'
                    temp_data_dbs.append(temp_data_db)
        except AttributeError as er:
            #print(er)
            try:
                tb = soup.find('a', class_='tgme_channel_download_telegram').text

                #print(f'Name tb:{tb[1:9]}')
                if tb[1:9]=='Download':
                    #print('start')
                    letters = ['\n', '`', '<', '>', '?', ':', ';', '"', "'", '[', ']', '{', '}', '&', '^', '%''']
                    # print(soup.find('div', class_='tgme_page_title').text)
                    temp_name = soup.find('div', class_='tgme_channel_info_header_title').text
                    #print(f'temp_name>>{temp_name}')
                    temp_name_db = ''
                    for i in letters:
                        temp_name = temp_name.replace(i, '')
                        temp_name_db = temp_name
                    nextline = 100
                    step = (int(len(temp_name)) / nextline).__ceil__()
                    temp_name_new = ''
                    if step > 2:
                        # mes=''
                        for x in range(step):
                            x = x + 1
                            # print("X=", x)
                            mes = temp_name[((nextline * x) - nextline):nextline * x]
                            # print(f'mes=={mes}')
                            if step != x:
                                temp_name_new += mes + '\n       '
                            else:
                                temp_name_new += mes
                    elif step <= 2:
                        if len(temp_name) > nextline:
                            temp_name_new = (temp_name[:nextline - 1] + '\n       ' + (temp_name[nextline:]))
                        else:
                            temp_name_new = temp_name
                    mess += ("🖼" + '[' + temp_name_new + ']' + '(' + page.url + ')' + "\n\n")
                    temp_data_db[0] += page.url
                    temp_data_db[1] += temp_name_db
                    temp_data_db[2] += 'post'
                    temp_data_dbs.append(temp_data_db)
            except AttributeError as er:
                print(f'Error{er}')
    return mess, temp_data_dbs
##################################################################################################

class Get_info_url:
    async def info_url(self,url):
        temp_data_db = ['', '', '', '', '', '', '']
        mess = ''
        if url.find('?')>1:
            print(f'FIND Post!!{url}')
        #url = url.replace('/s/', '/')
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        try:
            tb = soup.find('a', class_='tgme_action_button_new shine').text
            print('tb>>',tb)

            if tb == 'Send Message':
                letters = ['\n','`', '<', '>', '?', ':', ';', '"', "'", '[', ']', '{', '}', '&', '^', '%''']
                temp_name = soup.find('div', class_='tgme_page_title').text
                temp_name_db=''
                for i in letters:
                    temp_name = temp_name.replace(i, '')
                    temp_name_db=temp_name
                #print(soup.find('div', class_='tgme_page_title').text)

                #print(soup.find('a', class_='tgme_action_button_new shine').text)
                #print('Найден БОТ')

                nextline = 10
                step = (int(len(temp_name)) / nextline).__ceil__()
                temp_name_new = ''
                if step > 2:
                    #mes = ''
                    for x in range(step):
                        x = x + 1
                        print("X=", x)
                        mes = temp_name[((nextline * x) - nextline):nextline * x]
                        print(f'mes=={mes}')
                        if step != x:
                            temp_name_new += mes + '\n       '
                        else:
                            temp_name_new += mes
                elif step <= 2:
                    if len(temp_name) > nextline:
                        temp_name_new = (temp_name[:nextline - 1] + '\n       ' + (temp_name[nextline:]))
                    else:
                        temp_name_new = temp_name

                mess += ("🤖 " + "[" + temp_name_new + "]" + '(' + url + ')' + '\n\n')
                temp_data_db[0] += url
                temp_data_db[1] += temp_name_db
                temp_data_db[2] += 'bot'
            elif tb == 'View in Telegram':
                try:
                    #print(soup.find('a', class_='tgme_page_context_link').text)
                    #print('Найден канал')
                    letters = ['\n','`', '<', '>', '?', ':', ';', '"', "'", '[', ']', '{', '}', '&', '^', '%''']
                    temp_name = soup.find('div', class_='tgme_page_title').text
                    temp_name_db = ''
                    for i in letters:
                        temp_name = temp_name.replace(i, '')
                        temp_name_db = temp_name

                    nextline = 10
                    step = (int(len(temp_name)) / nextline).__ceil__()
                    temp_name_new=''
                    if step > 2:
                        #mes=''
                        for x in range(step):
                            x = x + 1
                            print("X=", x)
                            mes = temp_name[((nextline * x) - nextline):nextline * x]
                            print(f'mes=={mes}')
                            if step!=x:
                                temp_name_new += mes + '\n       '
                            else:
                                temp_name_new += mes

                            #temp_name_new = (temp_name[:nextline - 1] + '\n       ' + (temp_name[nextline:]))
                    elif step <= 2:
                        if len(temp_name) > nextline:
                            temp_name_new = (temp_name[:nextline - 1] + '\n       ' + (temp_name[nextline:]))
                        else:
                            temp_name_new = temp_name


                    mess += ("📢 " + '[' + temp_name_new + ']' + '(' + url + ')' + "\n\n")
                    temp_data_db[0] += url
                    temp_data_db[1] += temp_name_db
                    temp_data_db[2] += 'chanel'
                except AttributeError:
                    #print('Найден чат')
                    letters = ['\n','`', '<', '>', '?', ':', ';', '"', "'", '[', ']', '{', '}', '&', '^', '%''']
                    #print(soup.find('div', class_='tgme_page_title').text)

                    temp_name = soup.find('div', class_='tgme_page_title').text
                    temp_name_db = ''
                    for i in letters:
                        temp_name = temp_name.replace(i, '')
                        temp_name_db = temp_name

                    nextline = 10
                    step = (int(len(temp_name)) / nextline).__ceil__()
                    temp_name_new=''
                    if step > 2:
                        #mes=''
                        for x in range(step):
                            x = x + 1
                            print("X=", x)
                            mes = temp_name[((nextline * x) - nextline):nextline * x]
                            print(f'mes=={mes}')
                            if step!=x:
                                temp_name_new += mes + '\n       '
                            else:
                                temp_name_new += mes
                    elif step <= 2:
                        if len(temp_name) > nextline:
                            temp_name_new = (temp_name[:nextline - 1] + '\n       ' + (temp_name[nextline:]))
                        else:
                            temp_name_new = temp_name

                    mess += ("👥 " + '[' + temp_name_new + ']' + '(' + url + ')' + "\n\n")
                    temp_data_db[0] += url
                    temp_data_db[1] += temp_name_db
                    temp_data_db[2] += 'chat'
            return mess, temp_data_db
        except AttributeError:
            return False


    async def dele_letter(self,text):
        letters=['`','<','>','?',':',';','"',"'",'[',']','{','}','&','^','%''']
        for i in letters:
            text = text.replace(i,'')
        return text


class Get_info:
    def __init__(self,client):
        #self.search = None
        self.client=client
        #self.url=url
    async def dele_letter(self,text):
        letters=['`','<','>','?',':',';','"',"'",'[',']','{','}','&','^','%''']
        for i in letters:
            text = text.replace(i,'')
        return text


    async def get_info(self,url):
        temp_data_db = ['', '', '', '', '', '', '']
        #Нужно почистить URL от лишней информации https://t.me/s/vdovin_music?before=1127 все что после ? нужно удалить!
        #https: // t.me / +VllBe6oCgIJiNjI0
        if url.find('/+')>1:
            print(" ERROR +++")
            return False
        if url.find('/s/')>1: # Поиск символа что означает что ссылка ведет на пост
            index=url.find('?') # получаем индекс
            if url.find('?')>1: #  иногда ссылка может и не содержать спец символа https://t.me/s/chromemusic
                url=url[:index]
                url = url.replace('/s/','/')
            else:
                url = url.replace('/s/','/')
        # https://t.me/Minenergo_by/202 Иногда ссылка может и не содержать символа поста
        temp_url= url
        temp_url=temp_url.replace('https://t.me/','')
        if temp_url.find('/')>0:# and url.find('https://t.me/joinchat/')<0:
            print("Найдена галимая ссылка")
            index=temp_url.find('/') # получаем индекс
            temp_url = temp_url[:index]
            print('Новый адрес ',temp_url)
            url='https://t.me/'+temp_url
            #print("URL>",url)
        if url.find('/s/')<1:
            print('Проверка адресса',url)
            try:
                if url.find('joinchat')<1:
                    channel = await self.client.get_entity(url)
                    mess = ''
                    try:
                        if channel.bot:
                            letters = ['`', '<', '>', '?', ':', ';', '"', "'", '[', ']', '{', '}', '&', '^', '%''']
                            temp_name = channel.first_name
                            for i in letters:
                                temp_name = temp_name.replace(i, '')

                            mess += ("🤖 " + "[" + temp_name  + "]" + '(' + url + ')' + '\n')
                            temp_data_db[0] += url
                            temp_data_db[1] += temp_name
                            temp_data_db[2]+='bot'
                    except AttributeError:
                        try:
                            if channel.megagroup:
                                letters = ['`', '<', '>', '?', ':', ';', '"', "'", '[', ']', '{', '}', '&', '^', '%''']
                                temp_name = channel.title
                                for i in letters:
                                    temp_name = temp_name.replace(i, '')

                                mess += ("👥 " + '[' + temp_name + ']' + '(' + url + ')' + "\n")
                                temp_data_db[0] += url
                                temp_data_db[1] += temp_name
                                temp_data_db[2] += 'chat'

                            elif not channel.megagroup:
                                letters = ['`', '<', '>', '?', ':', ';', '"', "'", '[', ']', '{', '}', '&', '^', '%''']
                                temp_name = channel.title
                                for i in letters:
                                    temp_name = temp_name.replace(i, '')
                                mess += ("📢 " + '[' + temp_name + ']' + '(' + url + ')' + "\n")
                                temp_data_db[0] += url
                                temp_data_db[1] += temp_name
                                temp_data_db[2] += 'chanel'

                        except:
                            print("except>>", channel)
                    #sql_insert_all(con, temp_data_db)
                    return mess,temp_data_db
                else:
                    print("https://t.me/joinchat ERROR")
                    return False
            except UsernameInvalidError:
                print("ERROR UsernameInvalidError")
                return False
            except UsernameNotOccupiedError:
                print("ERROR UsernameNotOccupiedError")
                return False
            except ValueError:
                print('FAQ')
                return False




# url ='https://t.me/DeezerMusicBot'
# client = start_search()
# inf = Get_info(client,url)
# inf.get_info()




#
# def search():
#     x=1
#     db = sqlite3.connect('Account.db')
#     cur = db.cursor()
#     cur.execute(f"SELECT PHONE FROM Account WHERE ID = '{x}'")
#     time.sleep(0.4)
#     Phone = str(cur.fetchone()[0])
#     print("Входим в аккаунт: " + Phone, ' Номер ', x)
#     cur.execute(f"SELECT API_ID FROM Account WHERE ID = '{x}'")
#     time.sleep(0.4)
#     api_id = str(cur.fetchone()[0])
#     cur.execute(f"SELECT API_HASH FROM Account WHERE ID = '{x}'")
#     time.sleep(0.4)
#     api_hash = str(cur.fetchone()[0])
#     session = str("anon" + str(x))
#
#     client = TelegramClient(session, api_id, api_hash)
#     client.start()
#     time.sleep(2)
#     filter = InputMessagesFilterEmpty()
#     #search_CH_test_01
#     search = 'bitcoin'
#     #client.iter_messages(None, search=search)
#     for i in client.iter_messages(None, search=search):
#         print("###",i)
#     result =  client(functions.contacts.SearchRequest(
#         q=search,
#         limit=0
#     ))
#     time.sleep(2)
#     #print(result.stringify())
#     print(result)
#
#     for i in result.chats:
#         print(">>",i)
#
#     for i in result.users:
#         print(">>",i)
#         if i.bot == True:
#             print("OK")
#
#     client.disconnect()
