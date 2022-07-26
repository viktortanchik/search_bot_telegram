import grequests
from bassa import insert_cse_list,sql_select_cse_times,sql_select_cse_numbers,update_cse_list,all_cse_list
from datetime import *

#import requests
from config import search_urls
import random



async def filter(urls):
    temp_s_url = []
    for i in urls:
        if i.find('/s/') > 1:  # Поиск символа что означает что ссылка ведет на пост
            index = i.find('?')  # получаем индекс
            if i.find('?') > 1:  # иногда ссылка может и не содержать спец символа https://t.me/s/chromemusic
                i = i[:index]
                i = i.replace('?', '/')
                #i = i.replace('/s/', '/')
                temp_s_url.append(i)
            else:
                i = i.replace('?', '/')
                ind = i.find('/s/')
                print(f'i[ind:]>>{i[ind + 3:]}')
                if i[ind + 3:].find('/') > 1:
                    url = i[ind + 3:]
                    index_url = url.find('/')
                    url = url[:index_url]
                    print(f'NEW>>{url}')
                    i = 'https://t.me/' + url
                    temp_s_url.append(i)

                # i = i.replace('/s/', '/')
                else:
                    temp_s_url.append(i)
        else:
            temp_s_url.append(i)
    dic = dict.fromkeys(temp_s_url)
    new_urls = list(dic)
    for i in  range(len(new_urls)):
        #print(f'I>>{i}')
        for u in urls:
            #print(u.find(i))
            if u.find(new_urls[i])==0:
                #print(f'new_urls[i]>>{new_urls[i]}')
                new_urls[i]=u
                pass
    dic = dict.fromkeys(new_urls)
    new_urls = list(dic)
    #print(f'new_urls>>{new_urls}')
    return new_urls

async def lict_cse():
    all = all_cse_list()

    for i in all:
        if int(i[3]) < 40:############################  Ограничения на один аккаунт ############################
            number = int(i[3])
            #print(f'number>>{number}')
            number += 1
            #print(f'NEW_number>>{number}')
            update_cse_list(i[1], 'numbers', str(number))
            todays = date.today()
            todays = str(todays).replace('-', '')
            #print(todays)
            update_cse_list(i[1], 'times', str(todays))
            return i[1]

async def search_sce_(serach):
    data = []
    urls = []
    key = await lict_cse()
    for i in range(2):
        #url = f"https://www.googleapis.com/customsearch/v1?key=AIzaSyCB3rMM4vcu3Ildll2Aw43CRWbBky8k9SM&cx=9573f7af3478ae9ff&q={str(serach)}&start={i}"
        url = f"https://www.googleapis.com/customsearch/v1?{key}{str(serach)}&start={i}"
        #url = f"https://www.googleapis.com/customsearch/v1?key=AIzaSyCsQmQmUhkzDsytRDGO0ZKb0peA_IBh0Nk&cx=98cfda31ab1f938c6&q={str(serach)}&start={i}"
        # data = requests.get(url).json()
        urls.append(url)
    response = (grequests.get(url) for url in urls)
    pages = grequests.map(response)
    for r in pages:
        # r = requests.get('https://www.googleapis.com/customsearch/v1?'+url)
        # print(url)
        reqiest = r.json()
        # print("reqiest['items']>>",reqiest['items'])
        try:
            for i in reqiest['items']:
                items = {}
                # print(i['link'])
                items['title'] = i['title']
                items['link'] = i['link']
                # data.append(items)
                data.append(i['link'])
            # print(data)
        except KeyError as er:
            print("Error", er)
    # print('##############################')
    # print(data)
    dic = dict.fromkeys(data)
    # print(dic)
    new_urls = list(dic)
    print(f'new_urls>>>>><<<<>>{new_urls}')
    if len(new_urls)<1:
        return False
    new_urls=await filter(new_urls)
    return new_urls

class Search_sce:
    def __init__(self):
        #self.search = None
        self.serach=self

    async def search_sce(self,serach):
        range_url_search=int(len(search_urls))
        range_url_search = (int(range_url_search) -1)
        #print("range_url_search>>",range_url_search)
        #url = search_urls[(random.randint(0,int(len(search_urls))))]
        url = search_urls[random.randint(1,int(range_url_search))]
        print('RANDOM_URL',url)
        r = requests.get(
            'https://www.googleapis.com/customsearch/v1?'+url + str(
                serach))
        #print(r.text)
        reqiest =  r.json()
        #print("reqiest['items']>>",reqiest['items'])
        data = []
        try:
            for i in reqiest['items']:
                items = {}
                #print(i['link'])
                items['title'] = i['title']
                items['link'] = i['link']
                data.append(items)
            #print(data)
            return (data)
        except KeyError as er :
            print("Error",er)
            return False




#
# searc = Search_sce('music')
# #
# searc.search_sce()

#search('ClickBee')

