 # Использования поиска от GOOGLE
from accoun import Get_info_url, req_ansyn #main,start_search,Get_info
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

from aiogram.types import Message, ShippingOption, ShippingQuery, LabeledPrice, PreCheckoutQuery
from aiogram.types.message import ContentType,ReplyKeyboardMarkup
import time
from datetime import *
import time#from db import sql_select_search,sql_update,con,sql_insert_all
from bassa import *
import asyncio
from parser import search_sce_
from config import API_TOKEN,PAYMENTS_TOKEN,itetm_url
#import keyboards as kb
from keyboards import keyboard
from keyboards import get_keyboard,modify_keyboard
from PIL import Image
import os
from language import *

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}


async def chek_admins(user_id):
    admin = sql_select_admins(user_id)
    return admin

async def create_admins(user_id):
    temp_admin=[user_id,'temp']
    insert_admin_list(temp_admin)






@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    print(message["from"].id)
    user =sql_select_user_id_on_users(int(message["from"].id))
    kb = keyboard(user[0][4])

    if user:
        print(user[0])
        if user[0][3] == 'True' and user[0][4]=='en':
            update_user(int(message["from"].id), "search", 'True')
            await message.reply(language_start['en_start'], reply_markup=kb)
        if user[0][3] == 'True' and user[0][4]=='ch':
            update_user(int(message["from"].id), "search", 'True')
            await message.reply(language_start['ch_start'], reply_markup=kb)

    else:
        create_user_test = [int(message["from"].id), 9999, 'True', 'en', '0']
        insert_table_users(create_user_test)
        await message.reply("Send keywords to find groups, channels or bots.", reply_markup=kb)


@dp.message_handler(commands=['add_admin'])
async def process_start_command(message: types.Message):

    if await chek_admins(str(message["from"].id)):
        user = sql_select_user_id_on_users(int(message["from"].id))
        text=(message.text).lower()
        kb = keyboard(user[0][4])

        text = text.replace('/add_admin ','')
        adm = sql_select_admins(str(text))
        if adm != False:
            if user[0][4] == 'en':
                mess = language_add_admin['error_en']
            elif user[0][4] == 'ch':
                mess = language_add_admin['error_ch']
            await message.reply(str(mess),reply_markup=keyboard(user[0][4]))
        else:
            if user[0][4] == 'en':
                mess = language_add_admin['en_admin']
            elif user[0][4] == 'ch':
                mess = language_add_admin['ch_admin']
            #print('ID не найден')
            await create_admins(text)
            await message.reply(mess+str(text), reply_markup=kb)


@dp.message_handler(commands=['add_ad'])
async def process_start_command(message: types.Message):
    if await chek_admins(str(message["from"].id)):
        user = sql_select_user_id_on_users(int(message["from"].id))
        leng =user[0][4]

        kb = keyboard(user[0][4])

        #print(f"message: {message}")
        text=(message.text).lower()
        text = text.replace('/add_ad ','')
        li_text = text.split(',')
        #print("List:", li_text)
        #print(f'li_text[1]{li_text[2]}')
        try:
            d = date.today() + timedelta(days=int(li_text[2]))
            #print(f'd>>{d}')
            temp = [int(li_text[3]), 'Randomly ads', li_text[1], li_text[0], 'subtitle', 'status', str(d)]
            insert_table_ads(temp)
            todays = date.today()
            #print(todays)
            # print(todays.strftime("%m/%d/%Y"))

            await message.reply(language_add_ad[leng+'_ad']+
                                language_add_ad[leng+'_User']+li_text[3]+"\n"+
                                language_add_ad[leng+'_Title']+li_text[0]+'\n'+
                                language_add_ad[leng+'_Url']+li_text[1]+'\n'+
                                language_add_ad[leng+'_Date']+str(d), reply_markup=kb)

        except ValueError:
            await message.reply(language_add_ad[leng+'_error']+
                                language_add_ad[leng+'_User']+li_text[3]+"\n"+
                                language_add_ad[leng+'_Title']+li_text[0]+'\n'+
                                language_add_ad[leng+'_Url']+li_text[1]+'\n'
                                , reply_markup=kb)


async def get_user_spam(user_id):
    user = sql_select_user_id_on_users(user_id)
    if user:
        spam = user[0][5]
    else:
        print(f'user_id>>{user_id}')
        create_user_test = [int(user_id), 9999, 'True', 'en', '0']
        insert_table_users(create_user_test)
        user = sql_select_user_id_on_users(user_id)
        spam = user[0][5]

    if int(spam) >=3:

        user = sql_select_user_id_on_users(user_id)
        leng =user[0][4]

        await bot.send_message(user_id, spam_ban[leng+'_spam'])
        return False
    else:
        return True

async def get_spams(user_id,mess_id):
     await bot.delete_message(user_id, mess_id)
     user = sql_select_user_id_on_users(user_id)
     print(user)
     spam =user[0][5]
     spam =int(spam)+1
     update_user(user_id, "likes", str(spam))

     leng = user[0][4]
     if await get_user_spam(user_id):
        await bot.send_message(user_id, spams_strike[leng+'_spam'])

     #await bot.send_message(user_id, "DELETE")


# @dp.message_handler(content_types=['photo'])
# async def handle_docs_photo(message):
#     await get_spams(message["from"].id,message.message_id)


@dp.message_handler(commands=['delet_spam'])
async def process_start_command(message: types.Message):
    if await chek_admins(str(message["from"].id)):
        user = sql_select_user_id_on_users(str(message["from"].id))
        leng =user[0][4]
        kb = keyboard(user[0][4])

        mess = message.text
        mess = mess.replace('/delet_spam', '')
        mess = mess.replace(' ', '')
        #user = sql_select_user_id_on_users(mess)
        try:
            update_user(int(mess), "likes", str(0))
            await message.reply(del_spam[leng+'_ok'], reply_markup=kb)
        except:
            await message.reply(del_spam[leng+'_error'], reply_markup=kb)

@dp.message_handler(commands=['add_cse'])
async def process_start_command(message: types.Message):
    if await chek_admins(str(message["from"].id)):
        user = sql_select_user_id_on_users(str(message["from"].id))
        leng =user[0][4]
        kb = keyboard(user[0][4])

        mess = message.text
        mess = mess.replace('/add_cse', '')
        mess = mess.replace(' ', '')
        #user = sql_select_user_id_on_users(mess)
        try:
            #new_adress = ['key=AIzaSyBZdL-1Lvf58QfBw-aIf8NhDjvZBX-6fvI&cx=dd562bd2b71096921&q=', ' 0', '0']
            new_adress = [str(mess), ' 0', '0']
            # adress, times,numbers
            insert_cse_list(new_adress)
            await message.reply(language_add_cse[leng+'_ok'], reply_markup=kb)
        except:
            await message.reply(language_add_cse[leng+'_error'], reply_markup=kb)


@dp.message_handler(commands=['get_spam'])
async def process_start_command(message: types.Message):
    if await chek_admins(str(message["from"].id)):
        user = sql_select_user_id_on_users(str(message["from"].id))
        leng =user[0][4]
        kb = keyboard(user[0][4])

        user_data =all_user()
        print(user_data)
        mess=''
        mess+=language_get_spam[leng+'_spam']
        user=[]
        for i in user_data:
            if int(i[5])>=3:
                user.append(i[1])
                mess+=str(i[1])
        #mess+=str(len(user))
        await message.reply(mess, reply_markup=kb)


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def fileHandle(message: types.Document):
    print(message)
    await get_spams(message["from"].id,message.message_id)

    #await message.reply(text='файл получен, начинаю поиск ошибок...')

@dp.message_handler(commands=['add_bl'])
async def process_start_command(message: types.Message):
    if await chek_admins(str(message["from"].id)):

        text=message.text
        text = text.replace('/add_bl ','')
        li_text = text.split(',')
        print("List:", li_text)
        temp = ['title', li_text[0]]
        insert_black_list(temp)

@dp.message_handler(commands=['del_bl'])
async def process_start_command(message: types.Message):
    if await chek_admins(str(message["from"].id)):

        text=message.text
        text = text.replace('/del_bl ','')
        li_text = text.split(',')
        #print("List:", li_text)
        temp = sql_select_black_list(li_text[0])
        #print(f'temp{temp}')
        delete_black(temp[0])

@dp.message_handler(commands=['del_photo'])
async def process_start_command(message: types.Message):
    if await chek_admins(str(message["from"].id)):
        getchat = await bot.get_chat(message.chat.id)
        if getchat.title == None:
            user = sql_select_user_id_on_users(str(message["from"].id))
            leng = user[0][4]

            text = message.text
            text = text.replace('/del_photo ', '')
            li_text = text.split(',')
            ads = sql_select_user_id_on_ads(int(li_text[0]))
            if ads != False:
                temp = sql_select_title_id_on_ads(li_text[1])
                print(f'temp{temp}')
                if temp != False:
                    try:
                        os.remove(li_text[1] + '.jpg')
                        await message.answer(language_del_photo[leng+'_im']+li_text[1] + '.jpg')
                    except:
                        await message.answer(language_del_photo[leng+"_im_error"] + li_text[1] + '.jpg')
                else:
                    await message.answer(language_del_photo[leng+'_error_title'])
            else:
                await message.answer(language_del_photo[leng+'_error_user'])

@dp.message_handler(commands=['get_photo'])
async def process_start_command(message: types.Message):
    if await chek_admins(str(message["from"].id)):
        getchat = await bot.get_chat(message.chat.id)
        user = sql_select_user_id_on_users(str(message["from"].id))
        leng = user[0][4]
        if getchat.title == None:
            text = message.text
            text = text.replace('/get_photo ', '')
            li_text = text.split(',')
            ads = sql_select_user_id_on_ads(int(li_text[0]))
            if ads != False:
                temp = sql_select_title_id_on_ads(li_text[1])
                print(f'temp{temp}')
                if temp != False:
                    try:
                        #os.remove(li_text[1] + '.jpg')
                        await bot.send_photo(chat_id=message.chat.id, caption=str(li_text[1]),
                                             photo=open(li_text[1] + '.jpg', 'rb'))

                        #await message.answer("Images del. "+li_text[1] + '.jpg')
                    except:
                        await message.answer(language_del_photo[leng+'_not_find']+ li_text[1] + '.jpg')
                else:
                    await message.answer(language_del_photo[leng+'_error_title'])
            else:
                await message.answer(language_del_photo[leng+'_error_user'])

async def photo_add(message,bot):
    getchat = await bot.get_chat(message.chat.id)
    if getchat.title == None:
        user = sql_select_user_id_on_users(str(message["from"].id))
        leng = user[0][4]
        text = message.caption
        #text = text.replace('/mod ', '')
        li_text = text.split(',')
        ads = sql_select_user_id_on_ads(int(li_text[0]))
        if ads != False:
            temp = sql_select_title_id_on_ads(li_text[1])
            #print(f'temp{temp}')
            if temp != False:
                try:
                    await message.photo[-1].download(li_text[1] + '.jpg')

                    await message.answer(language_photo_add[leng+'_im']+ message.caption + '.jpg')
                    im = Image.open(li_text[1] + '.jpg')
                    (width, height) = im.size
                    new_image = im.resize((640,1280))
                    #new_image.show()
                    new_image.save(li_text[1] + '.jpg')
                    #print(f'width>>{width} height>>{height}')
                    await bot.send_photo(chat_id=message.chat.id, caption=str(li_text[1]),
                                         photo=open(li_text[1] + '.jpg', 'rb'))

                except:
                    await message.answer(language_photo_add[leng+'_not_saved'])
            else:
                await message.answer(language_photo_add[leng+'_error_title'])
        else:
            await message.answer(language_photo_add[leng+'_error_user'])

@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    if await chek_admins(str(message["from"].id)):
        await photo_add(message, bot)

    elif await chek_admins(str(message["from"].id))== False:
        await get_spams(message["from"].id, message.message_id)

@dp.message_handler(commands=['mod'])
async def process_start_command(message: types.Message):
    if await chek_admins(str(message["from"].id)):
        user = sql_select_user_id_on_users(str(message["from"].id))
        leng = user[0][4]
        kb = keyboard(user[0][4])

        # language_photo_add[leng+'_not_saved']
        text=message.text
        text = text.replace('/mod ','')
        li_text = text.split(',')
        #print("List:", li_text)
        ads = sql_select_user_id_on_ads(int(li_text[0]))
        #print(f'ads{ads}')
        if ads != False:
            temp = sql_select_title_id_on_ads(li_text[1])
            #print(f'temp{temp}')
            if temp != False:
                update_ads(temp[0][0], 'title', li_text[2]) # name
                await message.reply(language_mod[leng+'_name']+li_text[0]+language_mod[leng+'_title']+li_text[1]+li_text[2], reply_markup=kb.menu_kb)
                #await message.reply("you changed the user: "+li_text[0]+" ad titles "+li_text[1]+" to the new ad titles "+li_text[2], reply_markup=kb.menu_kb)
            else:
                await message.reply(language_mod[leng+'_not_found'], reply_markup=kb)

                #print('Ключевое слово не найдено')
        else:
            #print('ID не найден')
            await message.reply(language_mod[leng+'_id_not'], reply_markup=kb)

@dp.message_handler(commands=['ad_time'])
async def process_start_command(message: types.Message):
    if await chek_admins(str(message["from"].id)):
        user = sql_select_user_id_on_users(str(message["from"].id))
        leng = user[0][4]
        kb = keyboard(user[0][4])

        text=message.text
        text = text.replace('/ad_time ','')
        li_text = text.split(',')
        print("List:", li_text)
        ads = sql_select_user_id_on_ads(int(li_text[0]))
        print(f'ads{ads}')
        if ads != False:
            temp = sql_select_title_id_on_ads(li_text[1])
            print(f'temp{temp}')
            if temp != False:
                try:

                    todays = date.today()
                    d1 = datetime.strptime(str(todays), "%Y-%m-%d")
                    d2 = datetime.strptime(str(temp[0][7]), "%Y-%m-%d")
                    print((d2 - d1).days)
                    newdate=(d2 - d1).days
                    newdate=newdate+int(li_text[2])

                    d = date.today() + timedelta(days=newdate)
                    print(f'd>>{d}')
                    update_ads(temp[0][0], 'time', str(d)) # name
                    await message.reply(language_ad_time[leng+'_user']+li_text[0]+language_ad_time[leng+'_time']+str(d), reply_markup=kb)
                    #await message.reply("you changed the user: "+li_text[0]+" ad time "+str(d), reply_markup=kb.menu_kb)
                except ValueError:
                    await message.reply(language_ad_time[leng+'_error'], reply_markup=kb)
                    #await message.reply('❌ ERROR!!! ❌\n\nCheck the correctness of the data entered\n\n', reply_markup=kb.menu_kb)
            else:
                await message.reply(language_ad_time[leng + '_error'], reply_markup=kb)
                print('Ключевое слово не найдено')
        else:
            print('ID не найден')
            await message.reply(language_ad_time[leng+'_not_find'], reply_markup=kb)

@dp.message_handler(commands=['delete_admin'])
async def process_start_command(message: types.Message):
    if await chek_admins(str(message["from"].id)):
        user = sql_select_user_id_on_users(str(message["from"].id))
        leng = user[0][4]
        kb = keyboard(user[0][4])

        text=message.text
        text = text.replace('/delete_admin ','')
        li_text = text.split(',')
        #print("List:", li_text)
        adm = sql_select_admins(str(li_text[0]))
        if adm != False:
            delete_admins(adm[0][0])
            await message.reply(language_delete_admin[leng+'_admin']+str(li_text[0]), reply_markup=kb)

        else:
            #print('ID не найден')
            await message.reply(language_delete_admin[leng+'_error'], reply_markup=kb)

@dp.message_handler(commands=['delete_ad'])
async def process_start_command(message: types.Message):
    if await chek_admins(str(message["from"].id)):
        user = sql_select_user_id_on_users(str(message["from"].id))
        leng = user[0][4]
        kb = keyboard(user[0][4])

        text=message.text
        text = text.replace('/delete_ad ','')
        li_text = text.split(',')
        print("List:", li_text)
        ads = sql_select_user_id_on_ads(int(li_text[0]))
        print(f'ads{ads}')
        if ads != False:
            temp = sql_select_title_id_on_ads(li_text[1])
            print(f'temp{temp}')
            if temp != False:
                #update_ads(temp[0][0], 'title', li_text[2]) # name
                delete_part(temp[0][0])
                await message.reply(language_delete_ad[leng+'_delete']+li_text[1], reply_markup=kb)
            else:
                await message.reply(language_delete_ad[leng+'_not_key'], reply_markup=kb)

                #print('Ключевое слово не найдено')
        else:
            #print('ID не найден')
            await message.reply(language_delete_ad[leng+'_not_user'], reply_markup=kb)

@dp.message_handler(commands=['all_admin'])
async def process_start_command(message: types.Message):
    if await chek_admins(str(message["from"].id)):

        temp_all=all_admin()
        user = sql_select_user_id_on_users(str(message["from"].id))
        leng = user[0][4]
        kb = keyboard(user[0][4])

        mess=''
        mess+=language_all_admin[leng+'_user']
        for i in temp_all:
            print(i)
            mess += str(i[1])+'\n\n'
        await message.reply(mess, reply_markup=kb)

@dp.message_handler(commands=['all'])
async def process_start_command(message: types.Message):
    if await chek_admins(str(message["from"].id)):
        user = sql_select_user_id_on_users(str(message["from"].id))
        leng = user[0][4]
        kb = keyboard(user[0][4])

        temp_all=all_ads()
        mess=''
        for i in temp_all:
            print(i)
            mess += language_all[leng+'_user']+str(i[1])+'\n'
            mess += language_all[leng+'_title'] + i[4] + '\n'
            mess += language_all[leng+'_Url'] + i[3] + '\n'
            mess +=  language_all[leng+'_date'] + i[7] + '\n\n'

        await message.reply(mess, reply_markup=kb)

@dp.message_handler(commands=['all_black'])
async def process_start_command(message: types.Message):
    if await chek_admins(str(message["from"].id)):
        user = sql_select_user_id_on_users(str(message["from"].id))
        leng = user[0][4]
        kb = keyboard(user[0][4])

        temp_all=all_bl()
        mess=''
        for i in temp_all:
            print(i)
            mess += language_all_black[leng+'_Url'] + i[2] + '\n\n'

        await message.reply(mess, reply_markup=kb )

async def update_num_text(message: types.Message, mess: str,number:int,type:str):
    # Общая функция для обновления текста с отправкой той же клавиатуры
    if type=='chanel':
        await message.edit_text(f"📢 Channels {number}  \n\n{mess}", reply_markup=get_keyboard(types),parse_mode='Markdown', disable_web_page_preview=True)
    elif type == 'chat':
        await message.edit_text(f"👥 Groups {number}  \n\n{mess}", reply_markup=get_keyboard(types),parse_mode='Markdown', disable_web_page_preview=True)
    elif type == 'bot':
        await message.edit_text(f"🤖 Bots {number}  \n\n{mess}", reply_markup=get_keyboard(types),
                                parse_mode='Markdown', disable_web_page_preview=True)

async def send_ad_delet(id,title,url,date):

    await bot.send_message(674868256, "Added new advertisement\n"
                                      "User id: " + str(id) + "\n"
                           + "Title: " + title + '\n'
                           + 'Url: ' + url + '\n'
                           + 'Date: ' + date, )

@dp.message_handler(Text(equals="📢 Channels"))
async def with_puree(message: types.Message):
    print(message.text)
    mess=''
    mes=[]
    user_data[message.from_user.id]= 0
    user_data['type']='chanel'
    for i in sql_select_type('chanel') [:10] :
        if i[2]=='chanel':
            mess += ("📢 " + '[' + i[1] + ']' + '(' + i[4] + ')' + "\n")
            #mes.append("📢 " + '[' + i[1] + ']' + '(' + i[4] + ')' + "\n")
    await message.answer('📢 Channels 0\n\n'+mess, reply_markup=get_keyboard(types),parse_mode='Markdown', disable_web_page_preview=True)
    #print('Масив чатов >>',mes)

@dp.callback_query_handler(Text(startswith="num_"))
async def callbacks_num(call: types.CallbackQuery):
    print("####",user_data['type'])
    # Получаем текущее значение для пользователя, либо считаем его равным 0
    user_value = user_data.get(call.from_user.id, 0)
    # Парсим строку и извлекаем действие, например `num_incr` -> `incr`
    action = call.data.split("_")[1]
    if action == "incr":
        user_data[call.from_user.id] = user_value+10
        # if user_value> len(mes):
        #     user_value =(len(mes)-1)
        #user_value+=10
        print("user_value>>>",user_value)
        mess = ''
        for i in sql_select_type(user_data['type'])[user_data[call.from_user.id]:(user_data[call.from_user.id]+10)]:
            if i[2] == "chanel":
                mess += ("📢 " + '[' + i[1] + ']' + '(' + i[4] + ')' + "\n")
            if i[2] == 'chat':
                mess += ("👥 " + '[' + i[1] + ']' + '(' + i[4] + ')' + "\n")
            if i[2] == 'bot':
                mess += ("🤖 " + "[" + i[1] + "]" + '(' + i[4] + ')' + '\n')
        await update_num_text(call.message, mess,user_data[call.from_user.id],user_data['type'])#user_value+1)

    elif action == "decr":

        user_data[call.from_user.id] = user_value-10

        if user_data[call.from_user.id]<0:
            user_value=0
            user_data[call.from_user.id] =user_value
        else:
            mess = ''
            for i in sql_select_type(user_data['type'])[user_data[call.from_user.id]:(user_data[call.from_user.id] + 10)]:
                if i[2] == 'chanel':
                    mess += ("📢 " + '[' + i[1] + ']' + '(' + i[4] + ')' + "\n")
                if i[2] == 'chat':
                    mess += ("👥 " + '[' + i[1] + ']' + '(' + i[4] + ')' + "\n")
                if i[2] == 'bot':
                    mess += ("🤖 " + "[" + i[1] + "]" + '(' + i[4] + ')' + '\n')
            await update_num_text(call.message, mess,user_data[call.from_user.id],user_data['type'])#user_value+1)
        print("user_value<<<", user_data[call.from_user.id] )

    elif action == "finish":

        # Если бы мы не меняли сообщение, то можно было бы просто удалить клавиатуру
        # вызовом await call.message.delete_reply_markup().
        # Но т.к. мы редактируем сообщение и не отправляем новую клавиатуру,
        # то она будет удалена и так.
        await call.message.edit_text(f"Итого: {user_value}")
    # Не забываем отчитаться о получении колбэка
    await call.answer()

@dp.message_handler(Text(equals="👥 Groups"))
async def with_puree(message: types.Message):
    mess=''
    user_data[message.from_user.id] = 0
    user_data['type'] = 'chat'
    for i in sql_select_type('chat')[:10]:
        if i[2] == 'chat':
            mess += ("👥 " + '[' + i[1] + ']' + '(' + i[4] + ')' + "\n")
    await message.answer('👥 Groups 0\n\n' + mess, reply_markup=get_keyboard(types), parse_mode='Markdown',
                         disable_web_page_preview=True)

    # for i in sql_select_type('chat'):
    #     if i[2]=='chat':
    #         mess += ("👥 " + '[' + i[1] + ']' + '(' + i[4] + ')' + "\n")
    # await bot.send_message(message['from'].id, mess, parse_mode='Markdown', disable_web_page_preview=True)\

    # Общая функция для обновления текста с отправкой той же клавиатуры

@dp.message_handler(Text(equals="🤖 Bots"))
async def with_puree(message: types.Message):
    mess=''
    user_data[message.from_user.id] = 0
    user_data['type'] = 'bot'
    for i in sql_select_type('bot')[:10]:
        if i[2] == 'bot':
            mess += ("🤖 " + "[" + i[1] + "]" + '(' + i[4] + ')' + '\n')
    await message.answer('👥 Groups 0\n\n' + mess, reply_markup=get_keyboard(types), parse_mode='Markdown',
                         disable_web_page_preview=True)
    # mess=''
    # for i in sql_select_type('bot'):
    #     if i[2]=='bot':
    #         mess += ("🤖 " + "[" + i[1] + "]" + '(' + i[4] + ')' + '\n')
    # await bot.send_message(message['from'].id, mess, parse_mode='Markdown', disable_web_page_preview=True)

@dp.message_handler(Text(equals="🏁 Language"))
async def with_puree(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="English", callback_data="Language_English"))
    keyboard.add(types.InlineKeyboardButton(text="简体中文（中文）", callback_data="Language_China"))
    #keyboard.add(types.InlineKeyboardButton(text="Click me!",callback_data="random_value"))
    await message.answer("Still in development", reply_markup=keyboard)

@dp.message_handler(Text(equals="🏷 Tags"))
async def with_puree(message: types.Message):
    print('🏷 Tags')
    await message.reply("still in development")

@dp.message_handler(Text(equals="❓ Help!"))
async def with_puree(message: types.Message):
    print('❓ Help!')
    await message.reply("still in development")

@dp.message_handler(Text(equals="❓ 帮助"))
async def with_puree(message: types.Message):
    print('❓ Help!')
    await message.reply("still in development")

@dp.message_handler(Text(equals="👤 Me"))
async def with_puree(message: types.Message):
    #print(message)
    print('👤 Me')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Click me!", callback_data="random_value"))
    keyboard.add(types.InlineKeyboardButton(text="❤️my ad", callback_data="my_ads"))
    #keyboard.add(types.InlineKeyboardButton(text="Click me!",callback_data="random_value"))
    await message.answer("Still in development", reply_markup=keyboard)

@dp.message_handler(Text(equals="👤 我的"))
async def with_puree(message: types.Message):
    #print(message)
    print('👤 Me')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="查看ID", callback_data="random_value"))
    keyboard.add(types.InlineKeyboardButton(text="我的广告", callback_data="my_ads"))
    #keyboard.add(types.InlineKeyboardButton(text="Click me!",callback_data="random_value"))
    await message.answer("Still in development", reply_markup=keyboard)

@dp.callback_query_handler(Text(startswith="Language"))
async def send_random_value(call: types.CallbackQuery):
     action = call.data  ##cancel
     print(call['from'].id)
     #user = sql_select_user_id_on_users(str(call["from"].id))

     #kb = keyboard(user[0][4])

     if action == 'Language_English':
         print(f'Language_English')
         update_user(call['from'].id,'language','en')
         kb = keyboard('en')

         await bot.send_message(call['from'].id,"language English",reply_markup=kb)
         #await call.answer(text='Send /start', show_alert=True)
         #await call.answer("language English")
     if action == 'Language_China':
         print(f'Language_China')
         update_user(call['from'].id,'language','ch')
         kb = keyboard('ch')
         #await call.answer("language 简体中文（中文）",reply_markup=kb)
         await bot.send_message(call['from'].id,"language 简体中文（中文）",reply_markup=kb)


async def update_ad_text(message: types.Message, mess: str,type: str,number:int):
    if type =='my_ads':
        await message.edit_text(f"\n\n{mess}", reply_markup=modify_keyboard(types, int(message.chat.id)),
                                parse_mode='Markdown', disable_web_page_preview=True)

@dp.callback_query_handler(text="my_ads")
async def send_random_value(call: types.CallbackQuery):
     action = call.data  ##cancel
     if action == 'my_ads':
         mess = 'My ads.'
         type = 'my_ads'
         await update_ad_text(call.message, mess, type, 0)

@dp.callback_query_handler(text="random_value")
async def send_random_value(call: types.CallbackQuery):
    print(call)
    user = sql_select_user_id_on_users(int(call["from"].id))
    #await call.message.answer(str(randint(1, 10)))
    mess= 'Your id: '+str(call['from'].id)+'\nyour username: '+call['from'].username +'\n'+\
          'Language: '+str(user[0][4])
    await call.answer(text=mess, show_alert=True)
    #await message.reply("still in development")

@dp.message_handler()
async def any_text_message(message: types.Message):
    #print(message)
    flag=True
    try:
        #print('test')
        #print(message.entities)
        if len(message.entities)>0:
            flag=False
            await get_spams(message["from"].id, message.message_id)
    except:
        pass
    if await get_user_spam(int(message["from"].id))==True and flag==True :
    # Проверка пользователя
        user =sql_select_user_id_on_users(int(message["from"].id))
        # Работа поисковой системы
        if   user  and user[0][3]=='True' :
            temp_search = str(message.text).lower()
            search_data = sql_select_search(temp_search)
            search_data_title = sql_select_title_id_on_ads(temp_search)
            if search_data != None:
                #await bot.send_message(message['from'].id, 'Please wait')
                #await bot.send_message(message['from'].id, 'The data is in the database')
                #print("The data is in the database")
                # print(search_data[2])
                # получаем id текста поиска
                #print('Выводим  список ответов на запрос',search_data_title)

                #mess_old = 'Выводим  список ответов на запрос'
                mess_ad = '\n'
                #mess = '👉 Your advertising could be here 👈\n'
                mess = ''
                name_files=''
                if search_data_title:
                    for i in search_data_title:
                        mess_ad+=("🔰  " + "[" + i[4] + "]" + '(' + i[3] + ')' +'\n')#  '  subtitle: '+i[5]+ '\n')
                        name_files=i[4]
                        # try:
                        #     await bot.send_photo(chat_id=message.chat.id, parse_mode='Markdown', caption=str(mess_ad),
                        #                      photo=open(i[4]+ '.jpg', 'rb'))
                        # except:
                        #     pass
                for i in sql_select_link(search_data[0]):
                    nextline = 100
                    names =''
                    step = (int(len(i[1])) / nextline).__ceil__()# Получаем количество переносов строки диления в большую сторону

                    if step>2:# если больше чем 2 переноса
                        #print(f'Больше чем 2 переноа {step}')
                        for x in range(step):
                            x = x + 1
                            #print("X=", x)
                            name=i[1]
                            mes = name[((nextline * x) - nextline):nextline * x]
                            #print(f'mes=={mes}')
                            #names += mes + '\n       '
                            if step != x:
                                names += mes + '\n       '
                            else:
                                names += mes

                    elif step<=2:# если меньше чем 2 переноса
                        if len(i[1]) > nextline:
                             names =(i[1][:nextline - 1] + '\n       ' + (i[1][nextline:]))
                        else:
                            names=i[1]
                        print(names)
                    if i[2]=='bot':
                        mess += ("🤖 " + "[" + names + "]" + '(' + i[4] + ')' + '\n\n')
                    if i[2]=='chat':
                        mess += ("👥 " + '[' + names + ']' + '(' + i[4] + ')' + "\n\n")
                    if i[2]=='chanel':
                        mess += ("📢 " + '[' + names + ']' + '(' + i[4] + ')' + "\n\n")
                    if i[2]=='post':
                        mess += ("🖼" + '[' + names + ']' + '(' + i[4] + ')' + "\n\n")
                try:
                    #await bot.send_message(message['chat'].id, mess_ad + mess, parse_mode='Markdown',disable_web_page_preview=True)
                    #await message.reply(mess_ad + mess, parse_mode='Markdown', disable_web_page_preview=True)
                    try:
                        await bot.send_photo(chat_id=message.chat.id, parse_mode='Markdown', caption=str(mess_ad + mess),
                                             photo=open(name_files + '.jpg', 'rb'))
                    except:
                        await message.reply(mess_ad + mess, parse_mode='Markdown', disable_web_page_preview=True)



                except:
                    try:
                        await bot.send_photo(chat_id=message.chat.id, parse_mode='Markdown', caption=str(mess_ad + mess),
                                             photo=open(name_files + '.jpg', 'rb'))
                    except:
                        await message.reply(mess_ad + mess, parse_mode='Markdown', disable_web_page_preview=True)
                    #await message.reply(mess_ad + mess, parse_mode='Markdown', disable_web_page_preview=True)

                    #await bot.send_message(message['from'].id, mess_ad + mess, parse_mode='Markdown',disable_web_page_preview=True)

#銀行卡
            elif search_data == None:
                #await bot.send_message(message['from'].id, 'This is a new search, please wait')
                #searc = Search_sce() # Класс для поиска
                #se = await searc.search_sce(str(message.text))
                se = await search_sce_(str(message.text))
                if se:
                    #print("se>>",se)
                    #infos = Get_info(client=client)
                    #infos = Get_info_url()

                    #data_db=[]
                    tepm_url=[]
                    for i in se:
                        try:
                            url = i#['link']
                            if url.find('/s/') > 1:
                                #print("Найден Пост")
                                index = url.find('/s/')
                                temp_url = url[index + 3:]
                                #print(f'temp_url>>{temp_url}')
                                if temp_url.find('?') > 1 or temp_url.find('/') > 1:
                                    #print(f'пост: {url}')
                                    tepm_url.append(url)
                                else:
                                    url = url.replace('/s/', '/')
                                    tepm_url.append(url)
                            else:
                                tepm_url.append(url)

                            #x ,temp_data_db  = await infos.info_url(str(i['link'])) # Рабочий но не асинхроный
                            #urls=str(i['link'])
                            # urls= urls.replace('/s/', '/')
                            #tepm_url.append(urls)
                            # if x:
                            #     info += x
                            #     data_db.append(temp_data_db)
                        except TypeError:
                            #print('PASS')
                            pass
                    #print(f"START>url:{tepm_url}")
                    x = set(tepm_url)
                    dup = []
                    for c in x:
                        if (tepm_url.count(c) > 1):
                            indices = [i for i, x in enumerate(tepm_url) if x == c]
                            dup.append((c, indices))
                    for i in dup:
                        # print(len(i[1][1:]))
                        for _ in i[1][1:]:
                            tepm_url.remove(i[0])
                    #print(f'END>URLS>>{tepm_url}')
                    new_mes,data_db =  await req_ansyn(tepm_url)

                    str(message.text)
                    temp_search = str(message.text).lower()
                    search_data_title = sql_select_title_id_on_ads(temp_search)
                    # НУЖНО ДАБАВИТЬ ПОИСК ПО РЕКЛАМЕ И ЕСЛИ НЕТ РЕКЛАМЫ ТО ВСТАВЛЯТЬ ЭТУ СТРОКУ
                    mess_ad = ''
                    print(f'search_data_title>>>{search_data_title}')
                    if search_data_title:
                        print(f'search_data_title:{search_data_title}')
                        mess_ad+='\n'
                        for i in search_data_title:
                            mess_ad += ("🔰  " + "[" + i[4] + "]" + '(' + i[
                                3] + ')' + '\n')  # '  subtitle: '+i[5]+ '\n')
                            try:
                                await bot.send_photo(chat_id=message.chat.id, parse_mode='Markdown',
                                                     caption=str(mess_ad),
                                                     photo=open(i[4] + '.jpg', 'rb'))
                            except:
                                pass                        #info=search_data_title

                    #info = '👉 Your advertising could be here 👈\n'
                    info = ''

                    info+=mess_ad+new_mes
                    try:
                        #await bot.send_message(message['chat'].id, info, parse_mode='Markdown', disable_web_page_preview=True)
                        await message.reply(info, parse_mode='Markdown', disable_web_page_preview=True)

                    except:
                        #await message.reply(message['chat'].id, info,  disable_web_page_preview=True)
                        await message.reply(info, parse_mode='Markdown', disable_web_page_preview=True)

                        #await bot.send_message(message['from'].id, info, parse_mode='Markdown',disable_web_page_preview=True)
                        #await bot.send_message(message['from'].id, info, parse_mode='Markdown',disable_web_page_preview=True)
                        #print("info>>",info)
                    # Добавляем значения поисска в базу
                    temp=[str(temp_search),1]
                    insert_table_searchs(temp)
                    tempdatadb = sql_select_search(temp_search)
                    # б
                    #print("tempdatadb >>",tempdatadb)
                    for i in data_db:
                        i_temp=[tempdatadb[0],i[1],i[2],'test_TEG',i[0]]
                        insert_table_link(i_temp)

                    #print("Это нужно добавить в базу>>> ",data_db,' <<<')
                    #print('info>>>>',info)
                elif se ==False:
                    try:
                        await bot.send_message(message['chat'].id,'The keyword you query does not have a corresponding content.')

                    except:
                        await bot.send_message(message['from'].id,'The keyword you query does not have a corresponding content.')
        elif user ==False:
            #print('ERROR USER')
            try:
                await bot.send_message(message['chat'].id, 'send /start')
            except:
                await bot.send_message(message['from'].id, 'send /start')
                # for i in info:
                #     print('info>>',i)
                #await bot.send_message(message['from'].id,'')
    # else:
    #     await bot.send_message(message['from'].id, 'BAN')

@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(message: types.Message):
    await get_spams(message["chat"].id,message.message_id)

if __name__ == '__main__':
    executor.start_polling(dp)
