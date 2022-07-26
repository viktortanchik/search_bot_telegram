import time
from datetime import *
from bassa import all_ads,delete_part
from main import send_ad_delet
import asyncio
from bassa import insert_cse_list,sql_select_cse_times,sql_select_cse_numbers,update_cse_list,all_cse_list

#674868256


async def days():
    todays = date.today()
    todays=str(todays).replace('-','')
    #print(todays)
    temp_all = all_ads()
    #print(temp_all)
    for i in temp_all:
        #print(i)
        #print(i[7])
        temp = str(i[7]).replace('-', '')
        if int(temp) < int(todays):
            print("delete ADD")
            await send_ad_delet(str(i[1]), i[4], i[3], i[7])
            delete_part(i[0])
asyncio.run(days())



async def days_cse():
    todays = date.today()
    todays = str(todays).replace('-', '')
    #print(todays)
    #todays='20220712'
    all = all_cse_list()
    for i in all:
        if int(todays) != int(i[2]):
            update_cse_list(i[1], 'times', str(0))
            update_cse_list(i[1], 'numbers', str(0))

    # print(temp_all)


asyncio.run(days_cse())

# print(todays.strftime("%m/%d/%Y"))
# d = date.today() + timedelta(days=100)
# print(d)
