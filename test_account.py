from bassa import insert_cse_list,sql_select_cse_times,sql_select_cse_numbers,update_cse_list,all_cse_list

from test import find_test

new_adress=['key=AIzaSyBZdL-1Lvf58QfBw-aIf8NhDjvZBX-6fvI&cx=dd562bd2b71096921&q=',' 0','0']
#adress, times,numbers
#insert_cse_list(new_adress)


#update_cse_list()
# all = all_cse_list()
#
#
#
# print(all)
# for i in all:
#     if int(i[3])<2:
#         number = int(i[3])
#         print(f'number>>{number}')
#         number +=1
#         print(f'NEW_number>>{number}')
#         update_cse_list(i[1], 'numbers', str(number))
#         find_test(i[1])
#         break
# #find_test()

url_list=['https://t.me/s/PAOFEN?before=280','https://t.me/s/PAOFEN/1','https://t.me/s/PAOFEN?before=20'
    ,'https://t.me/s/MentaCarMarket?after=139','https://t.me/PAOFEN']

def filter(urls):
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
                print(f'i[ind:]>>{i[ind+3:]}')
                if i[ind+3:].find('/')>1:
                    url = i[ind+3:]
                    index_url=url.find('/')
                    url=url[:index_url]
                    print(f'NEW>>{url}')
                    i='https://t.me/'+url
                    temp_s_url.append(i)

                #i = i.replace('/s/', '/')
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

print(filter(url_list))