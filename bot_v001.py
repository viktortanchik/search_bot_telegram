 # Использования поиска от GOOGLE
from accoun import Get_info_url  #main,start_search,Get_info
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

from aiogram.types import Message, ShippingOption, ShippingQuery, LabeledPrice, PreCheckoutQuery
from aiogram.types.message import ContentType

import time
#from db import sql_select_search,sql_update,con,sql_insert_all
from bassa import *
import asyncio
from parser import Search_sce
from config import API_TOKEN,PAYMENTS_TOKEN,itetm_url
import keyboards as kb
from keyboards import get_keyboard,buyad_inli_keyboard,choice_tariff_randomad_keyboard,tariff_pay_end,modify_keyboard,\
    cancel,choice_tariff_keyword_keyboard,choice_tariff_ad_second_place_ad,choice_tariff_ad_third_place_ad,\
    nexts,choice_tariff_ad_infomercial_place_ad


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}

@dp.message_handler(commands=['pay'])
async def process_start_command(message: types.Message):
    print('+++++++PAY+++++++')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="pay!", callback_data="pay_test",))
    #keyboard.add(types.InlineKeyboardButton(text="Click me!",callback_data="random_value"))зфн
    await message.answer("Still in development", reply_markup=keyboard)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    print(message["from"].id)
    user =sql_select_user_id_on_users(int(message["from"].id))
    if user:
        print(user[0])
        if user[0][3] == 'False':
            update_user(int(message["from"].id), "search", 'True')
    else:
        create_user_test = [int(message["from"].id), 9999, 'True', 'en', '']
        insert_table_users(create_user_test)



    await message.reply("Send keywords to find groups, channels or bots.", reply_markup=kb.menu_kb)


async def update_num_text(message: types.Message, mess: str,number:int,type:str):
    # Общая функция для обновления текста с отправкой той же клавиатуры
    if type=='chanel':
        await message.edit_text(f"📢 Channels {number}  \n\n{mess}", reply_markup=get_keyboard(types),parse_mode='Markdown', disable_web_page_preview=True)
    elif type == 'chat':
        await message.edit_text(f"👥 Groups {number}  \n\n{mess}", reply_markup=get_keyboard(types),parse_mode='Markdown', disable_web_page_preview=True)
    elif type == 'bot':
        await message.edit_text(f"🤖 Bots {number}  \n\n{mess}", reply_markup=get_keyboard(types),
                                parse_mode='Markdown', disable_web_page_preview=True)

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

async def update_ad_text(message: types.Message, mess: str,type: str,number:int):
    # После выбора тарифа появится окно с предложениям о покупки
    if type=='randomad':
        await message.edit_text(f"Test mess \n\n{mess}", reply_markup=choice_tariff_randomad_keyboard(types),parse_mode='Markdown', disable_web_page_preview=True)
    elif type=='keyword':
        await message.edit_text(f"Test mess \n\n{mess}", reply_markup=choice_tariff_keyword_keyboard(types),parse_mode='Markdown', disable_web_page_preview=True)
    elif type=='second_place_ad':
        await message.edit_text(f"Test mess \n\n{mess}", reply_markup=choice_tariff_ad_second_place_ad(types),
                                parse_mode='Markdown', disable_web_page_preview=True)
    elif type=='third_place_ad':
        await message.edit_text(f"Test mess \n\n{mess}", reply_markup=choice_tariff_ad_third_place_ad(types),
                                parse_mode='Markdown', disable_web_page_preview=True)
    elif type=='infomercial_ad':
        print("TEST2.2")
        await message.edit_text(f"Test mess \n\n{mess}", reply_markup=choice_tariff_ad_infomercial_place_ad(types),
                                parse_mode='Markdown', disable_web_page_preview=True)
    # elif type =='tariff_pay_keyword':
    #     await message.edit_text(f"{mess}\n\nAn advertisement template has been created, go to the ✅Modification section to modify ", reply_markup=tariff_pay_end(types),
    #                             parse_mode='Markdown', disable_web_page_preview=True)
    #     temp = [int(message.chat.id), 'keyword ads', 'WWW_LINKE', 'title', 'subtitle', 'status', 'date']
    #     insert_table_ads(temp)
    # elif type =='tariff_pay_second_place_ad':
    #     await message.edit_text(f"{mess}\n\nAn advertisement template has been created, go to the ✅Modification section to modify ", reply_markup=tariff_pay_end(types),
    #                             parse_mode='Markdown', disable_web_page_preview=True)
    #     temp = [int(message.chat.id), 'second_place_ad', 'WWW_LINKE', 'title', 'subtitle', 'status', 'date']
    #     insert_table_ads(temp)
    # elif type =='tariff_pay_third_place_ad':
    #     await message.edit_text(f"{mess}\n\nAn advertisement template has been created, go to the ✅Modification section to modify ", reply_markup=tariff_pay_end(types),
    #                             parse_mode='Markdown', disable_web_page_preview=True)
    #     temp = [int(message.chat.id), 'third_place_ad', 'WWW_LINKE', 'title', 'subtitle', 'status', 'date']
    #     insert_table_ads(temp)


    elif type=='modify':
        await message.edit_text(f"Test mess \n\n{mess}", reply_markup=modify_keyboard(types,int(message.chat.id)),
                                parse_mode='Markdown', disable_web_page_preview=True)
    elif type=='my_ads':
        await message.edit_text(f"\n\n{mess}", reply_markup=modify_keyboard(types,int(message.chat.id)),
                                parse_mode='Markdown', disable_web_page_preview=True)
    elif type=='ads_modify_title':
        user_data['type'] = 'ads_modify_title'
        await message.edit_text(f"\n\n{mess}", reply_markup=cancel(types),
                                parse_mode='Markdown', disable_web_page_preview=True)
    elif type=='start':
        await message.edit_text(f"\n\n{mess}",
                                parse_mode='Markdown', disable_web_page_preview=True)
    elif type=='test_randomad':# для оплаты картой
        user_data['type'] = 'test_randomad'
        await message.edit_text(f"\n\n{mess}", reply_markup=cancel(types),
                                parse_mode='Markdown', disable_web_page_preview=True)
    elif type=='test_first_place_ad':# для оплаты картой
        user_data['type'] = 'test_first_place_ad'
        await message.edit_text(f"\n\n{mess}", reply_markup=cancel(types),
                                parse_mode='Markdown', disable_web_page_preview=True)
    elif type=='test_second_place_ad':# для оплаты картой
        user_data['type'] = 'test_second_place_ad'
        await message.edit_text(f"\n\n{mess}", reply_markup=cancel(types),
                                parse_mode='Markdown', disable_web_page_preview=True)
    elif type=='test_third_place_ad':# для оплаты картой
        user_data['type'] = 'test_third_place_ad'
        await message.edit_text(f"\n\n{mess}", reply_markup=cancel(types),
                                parse_mode='Markdown', disable_web_page_preview=True)
    elif type=='test_infomercial_ad':# для оплаты картой
        user_data['type'] = 'test_infomercial_ad'
        await message.edit_text(f"\n\n{mess}", reply_markup=cancel(types),
                                parse_mode='Markdown', disable_web_page_preview=True)
    elif type=='test_try':
        user_data['type'] = 'test_try'
        await message.edit_text(f"\n\n{mess}", reply_markup=cancel(types),
                                parse_mode='Markdown', disable_web_page_preview=True)


# @dp.message_handler(commands=['buy'])
# async def buy_process(message: types.Message):
PICKUP_SHIPPING_OPTION = ShippingOption(id='pickup',
                                            title='Самовывоз').add(LabeledPrice('Лично', 1000))

@dp.callback_query_handler(Text(startswith="tyr_tariff_pay_"))
async def callbacks_num(call: types.CallbackQuery):
    action = call.data  # .split("_")[1]
    if action == 'tyr_tariff_pay_randomad':
        PRICES = [
            LabeledPrice(label='Advertising with special words!', amount=10000),
            LabeledPrice('GIFT', 0)
        ]
        print("chat>>",call)
        print("callfrom.id>>",call["from"].id)

        await bot.send_invoice(
            #message.chat.id,  # chat_id
            int(call["from"].id),
            'item_title',
            'item_description',
            # description
            'HAPPY FRIDAYS COUPON',  # invoice_payload
            PAYMENTS_TOKEN,  # provider_token
            'usd',  # currency
            PRICES,  # prices
            #photo_url='http://erkelzaar.tsudao.com/models/perrotta/TIME_MACHINE.jpg',
            photo_url=itetm_url,
            photo_height=512,  # !=0/None or picture won't be shown
            photo_width=512,
            photo_size=512,
            is_flexible=False,  # True If you need to set up Shipping Fee
            start_parameter='time-machine-example')

    elif action=='tyr_tariff_pay_keyword':
        PRICES = [
            LabeledPrice(label='You bought 🥇keyword ranking ads\nDeducted from your balance 150 USTD', amount=15000),
            LabeledPrice('GIFT', 0)
        ]
        print("chat>>", call)
        print("callfrom.id>>", call["from"].id)

        await bot.send_invoice(
            # message.chat.id,  # chat_id
            int(call["from"].id),
            'You bought 🥇keyword ranking ads',
            'Deducted from your balance 150 USTD',
            # description
            'HAPPY FRIDAYS COUPON',  # invoice_payload
            PAYMENTS_TOKEN,  # provider_token
            'usd',  # currency
            PRICES,  # prices
            # photo_url='http://erkelzaar.tsudao.com/models/perrotta/TIME_MACHINE.jpg',
            photo_url=itetm_url,
            photo_height=512,  # !=0/None or picture won't be shown
            photo_width=512,
            photo_size=512,
            is_flexible=False,  # True If you need to set up Shipping Fee
            start_parameter='time-machine-example')

    elif action=='tyr_tariff_pay_second_place':
        PRICES = [
            LabeledPrice(label='You bought 🥈top of search results\nDeducted from your balance 200 USTD', amount=20000),
            LabeledPrice('GIFT', 0)
        ]
        print("chat>>", call)
        print("callfrom.id>>", call["from"].id)

        await bot.send_invoice(
            # message.chat.id,  # chat_id
            int(call["from"].id),
            'You bought 🥈top of search results',
            'Deducted from your balance 200 USTD',
            # description
            'HAPPY FRIDAYS COUPON',  # invoice_payload
            PAYMENTS_TOKEN,  # provider_token
            'usd',  # currency
            PRICES,  # prices
            # photo_url='http://erkelzaar.tsudao.com/models/perrotta/TIME_MACHINE.jpg',
            photo_url=itetm_url,
            photo_height=512,  # !=0/None or picture won't be shown
            photo_width=512,
            photo_size=512,
            is_flexible=False,  # True If you need to set up Shipping Fee
            start_parameter='time-machine-example')

    elif action=='tyr_tariff_pay_third_place':
        PRICES = [
            LabeledPrice(label='You bought 🥉Group built-in top ad\nDeducted from your balance 250 USTD', amount=25000),
            LabeledPrice('GIFT', 0)
        ]
        print("chat>>", call)
        print("callfrom.id>>", call["from"].id)

        await bot.send_invoice(
            # message.chat.id,  # chat_id
            int(call["from"].id),
            'You bought 🥉Group built-in top ad',
            'Deducted from your balance 250 USTD',
            # description
            'HAPPY FRIDAYS COUPON',  # invoice_payload
            PAYMENTS_TOKEN,  # provider_token
            'usd',  # currency
            PRICES,  # prices
            # photo_url='http://erkelzaar.tsudao.com/models/perrotta/TIME_MACHINE.jpg',
            photo_url=itetm_url,
            photo_height=512,  # !=0/None or picture won't be shown
            photo_width=512,
            photo_size=512,
            is_flexible=False,  # True If you need to set up Shipping Fee
            start_parameter='time-machine-example')


    elif action=='tyr_tariff_pay_infomercial_place':
        PRICES = [
            LabeledPrice(label='🏅Join the group infomercial\nDeducted from your balance 300 USTD', amount=30000),
            LabeledPrice('GIFT', 0)
        ]
        print("chat>>", call)
        print("callfrom.id>>", call["from"].id)

        await bot.send_invoice(
            # message.chat.id,  # chat_id
            int(call["from"].id),
            '🏅Join the group infomercial',
            'Deducted from your balance 300 USTD',
            # description
            'HAPPY FRIDAYS COUPON',  # invoice_payload
            PAYMENTS_TOKEN,  # provider_token
            'usd',  # currency
            PRICES,  # prices
            # photo_url='http://erkelzaar.tsudao.com/models/perrotta/TIME_MACHINE.jpg',
            photo_url=itetm_url,
            photo_height=512,  # !=0/None or picture won't be shown
            photo_width=512,
            photo_size=512,
            is_flexible=False,  # True If you need to set up Shipping Fee
            start_parameter='time-machine-example')


@dp.pre_checkout_query_handler(lambda q: True)
async def checkout_process(pre_ceckout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_ceckout_query.id,ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message:Message):
    await bot.send_message(message.chat.id,
                     'Hoooooray! Thanks for payment! We will proceed your order for `{} {}` as fast as possible! '
                     'Stay in touch.\nThe ad template has been created, go to the 👤 Me section and select ✅Modification to change it'.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')#,reply_markup=tariff_pay_end(types))

    temp = [int(message.chat.id), 'Randomly ads', 'WWW_LINKE', 'title', 'subtitle', 'status', 'date']
    insert_table_ads(temp)
    update_user(int(message["from"].id), "search", 'True')
    #await update_ad_text(message, 'mess', type,0)




# Кноппа на выбор тарифа для рекламы
@dp.message_handler(Text(equals="✅ Buy ad"))
async def with_puree(message: types.Message):
    print(message)
    mess = 'Here is the introduction of the advertisement,some prompt text, such as searching in English, and then providing English,if in Chinese, it is Chinese prompt.'
    await message.answer('\n\n'+mess, reply_markup=buyad_inli_keyboard(types), parse_mode='Markdown',
                         disable_web_page_preview=True)

# modify Настройка рекламы пользователя
@dp.callback_query_handler(Text(startswith="ads"))
async def callbacks_num(call: types.CallbackQuery):
    action = call.data#[1]#.split("_")[1]
    print("Кнопка нажата", action)
    #user=sql_select_user_id_on_users(int(call["from"].id))
    ads=sql_select_user_id_on_ads(int(call["from"].id))
    ad=[]
    mess='Please enter a new title'
    type='ads_modify_title'
    for i in ads:
        if action ==('ads'+str(i[0])):
            await update_ad_text(call.message, mess, type, i[0])

        #ad.append(i)

# Обработака кноппи ✅pay
@dp.callback_query_handler(Text(startswith="choice_"))
async def callbacks_num(call: types.CallbackQuery):
    action = call.data#[1]#.split("_")[1]
    print("Кнопка нажата", action)
    user=sql_select_user_id_on_users(int(call["from"].id))
    if action =='choice_tariff_pay_randomad':
        mess='You bought 🔥Randomly suggest popular channels ads\nDeducted from your balance 100 USTD'
        type='tyr_tariff_pay_randomad'
        print('tariff_pay_randomad')
        await bot.send_message(int(call["from"].id), mess, reply_markup=nexts(types, type))
        await update_ad_text(call.message, mess, type,0)
    elif action=='choice_tariff_modification':
        ads = sql_select_user_id_on_ads(int(call["from"].id))
        #print(ads)
        update_user(int(call["from"].id), "search", 'False')
        mess='Please select the ad you need to modify'
        type='modify'
        await update_ad_text(call.message, mess, type,0)
    elif action=='choice_tariff_pay_keyword':
        print("choice_tariff_pay_keyword")
        mess='You bought 🥇keyword ranking ads\nDeducted from your balance 150 USTD'
        type='tyr_tariff_pay_keyword'
        print('tyr_tariff_pay_keyword')
        await bot.send_message(int(call["from"].id), mess, reply_markup=nexts(types, type))
        await update_ad_text(call.message, mess, type,0)
    elif action=='choice_tariff_pay_ad_second_place_ad':
        print("choice_tariff_pay_ad_second_place_ad")
        mess='You bought 🥈top of search results\nDeducted from your balance 200 USTD'
        type='tyr_tariff_pay_second_place'
        print('tyr_tariff_pay_second_place')
        await bot.send_message(int(call["from"].id), mess, reply_markup=nexts(types, type))
        await update_ad_text(call.message, mess, type,0)
    elif action=='choice_tariff_pay_ad_third_place_ad':
        print("choice_tariff_pay_ad_third_place_ad")
        mess='You bought 🥉Group built-in top ad\nDeducted from your balance 250 USTD'
        type='tyr_tariff_pay_third_place'
        print('tyr_tariff_pay_third_place')
        await bot.send_message(int(call["from"].id), mess, reply_markup=nexts(types, type))
        await update_ad_text(call.message, mess, type,0)

    elif action=='choice_tariff_pay_ad_infomercial_place_ad':
        print('TEST2.4')
        print("choice_tariff_pay_ad_infomercial_place_ad")
        mess='🏅Join the group infomercial\nDeducted from your balance 300 USTD'
        type='tyr_tariff_pay_infomercial_place'
        print('tyr_tariff_pay_infomercial_place')
        await bot.send_message(int(call["from"].id), mess, reply_markup=nexts(types, type))
        await update_ad_text(call.message, mess, type,0)


@dp.callback_query_handler(Text(startswith="my_ads"))
async def callbacks_num(call: types.CallbackQuery):
    action = call.data##cancel
    if action =='my_ads':
        mess='My ads.'
        type='my_ads'
        await update_ad_text(call.message, mess, type,0)

@dp.callback_query_handler(Text(startswith="cancel"))
async def callbacks_num(call: types.CallbackQuery):
    action = call.data##cancel
    if action =='cancel':
        update_user(int(call["from"].id), "search", 'True')
        mess='Send keywords to find groups, channels or bots.'
        type='start'
        await update_ad_text(call.message, mess, type,0)

#test_ad_randomad_
@dp.callback_query_handler(Text(startswith="test_"))
async def test_ad(call: types.CallbackQuery):
    action = call.data#.split("_")[1]
    #Если нажата ad_random_ad
    print("Кнопка нажата",action)
    if action == "test_ad_randomad_":
        #type="randomad"
        update_user(int(call["from"].id), "search", 'False')
        mess='Please enter a word to check if it is in the database!'
        type='test_randomad'
        await update_ad_text(call.message, mess, type,0)
    elif action == "test_ad_first_place_ad":
        #type="randomad"
        update_user(int(call["from"].id), "search", 'False')
        mess='Please enter a word to check if it is in the database!'
        type='test_first_place_ad'
        await update_ad_text(call.message, mess, type,0)
    elif action == "test_ad_second_place_ad":
        #type="randomad"
        update_user(int(call["from"].id), "search", 'False')
        mess='Please enter a word to check if it is in the database!'
        type='test_second_place_ad'
        await update_ad_text(call.message, mess, type,0)
    elif action == "test_ad_third_place_ad":
        #type="randomad"
        update_user(int(call["from"].id), "search", 'False')
        mess='Please enter a word to check if it is in the database!'
        type='test_third_place_ad'
        await update_ad_text(call.message, mess, type,0)
    elif action == "test_ad_infomercial_ad":
        #type="randomad"
        update_user(int(call["from"].id), "search", 'False')
        mess='Please enter a word to check if it is in the database!'
        type='test_infomercial_ad'
        await update_ad_text(call.message, mess, type,0)
    # test_ad_first_place_ad


# Выбор тарифного плана
@dp.callback_query_handler(Text(startswith="ad_"))
async def callbacks_num(call: types.CallbackQuery):
    action = call.data#.split("_")[1]
    #Если нажата ad_random_ad
    print("Кнопка нажата",action)
    if action == "ad_randomad_":
        type="randomad"
        mess='💡Number of ads： 100\n' \
             '💡Expiring soon： 100\n' \
             '💡Average daily display: 100\n' \
             '🟢Price： 100 USDT'
        await update_ad_text(call.message, mess,type,0)
    elif action =='ad_first_place_ad':
        type="keyword"
        mess='💡Number of ads： 100\n' \
             '💡Expiring soon： 100\n' \
             '💡Average daily display: 100\n' \
             '🟢Price： 150 USDT'
        await update_ad_text(call.message, mess,type,0)
    elif action =='ad_second_place_ad':
        type="second_place_ad"
        mess='💡Number of ads： 100\n' \
             '💡Expiring soon： 100\n' \
             '💡Average daily display: 100\n' \
             '🟢Price： 200 USDT'
        await update_ad_text(call.message, mess,type,0)
    elif action =='ad_third_place_ad':
        type='third_place_ad'
        print("TEST1")
        mess='💡Number of ads： 100\n' \
             '💡Expiring soon： 100\n' \
             '💡Average daily display: 100\n' \
             '🟢Price： 250 USDT'
        await update_ad_text(call.message, mess,type,0)
    elif action =='ad_infomercial_ad':
        type="infomercial_ad'"
        print("TEST2")
        mess='💡Number of ads： 100\n' \
             '💡Expiring soon： 100\n' \
             '💡Average daily display: 100\n' \
             '🟢Price： 300 USDT'
        await update_ad_text(call.message, mess,type,0)




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

@dp.message_handler(Text(equals="🏁 Language: English (English)"))
async def with_puree(message: types.Message):
    print('🏁 Language: English (English)')
    await message.reply("Currently only English is available")

@dp.message_handler(Text(equals="🏷 Tags"))
async def with_puree(message: types.Message):
    print('🏷 Tags')
    await message.reply("still in development")

@dp.message_handler(Text(equals="❓ Help!"))
async def with_puree(message: types.Message):
    print('❓ Help!')
    await message.reply("still in development")

@dp.message_handler(Text(equals="👤 Me"))
async def with_puree(message: types.Message):
    print(message)
    print('👤 Me')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Click me!", callback_data="random_value"))
    keyboard.add(types.InlineKeyboardButton(text="❤️my ad", callback_data="my_ads"))
    keyboard.add(types.InlineKeyboardButton(text="✅Modification", callback_data="choice_tariff_modification"))

    #keyboard.add(types.InlineKeyboardButton(text="Click me!",callback_data="random_value"))
    await message.answer("Still in development", reply_markup=keyboard)

@dp.callback_query_handler(text="random_value")
async def send_random_value(call: types.CallbackQuery):
    print(call)
    user = sql_select_user_id_on_users(int(call["from"].id))
    #await call.message.answer(str(randint(1, 10)))
    mess= 'Your id: '+str(call['from'].id)+' your username: '+call['from'].username +'\n'+'Wallet: '+str(user[0][2])+'\n'+\
          'Language: '+str(user[0][4])
    await call.answer(text=mess, show_alert=True)
    #await message.reply("still in development")


@dp.message_handler()
async def any_text_message(message: types.Message):
    print(message)
    # Проверка пользователя
    user =sql_select_user_id_on_users(int(message["from"].id))
    # Работа поисковой системы
    if   user  and user[0][3]=='True' :
        temp_search = str(message.text).lower()
        search_data = sql_select_search(temp_search)
        search_data_title = sql_select_title_id_on_ads(temp_search)
        if search_data != None:
            #await bot.send_message(message['from'].id, 'Please wait')
            await bot.send_message(message['from'].id, 'The data is in the database')
            print("The data is in the database")
            # print(search_data[2])
            # получаем id текста поиска
            print('Выводим  список ответов на запрос',search_data_title)

            #mess_old = 'Выводим  список ответов на запрос'
            mess_ad = '\n'
            mess = '👉 Your advertising could be here 👈\n'
            for i in search_data_title:
                mess_ad+=("🔰  " + "[" + i[4] + "]" + '(' + i[3] + ')' +'  subtitle: '+i[5]+ '\n')
            for i in sql_select_link(search_data[0]):
                nextline = 10
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
            await bot.send_message(message['from'].id, mess_ad+mess, parse_mode='Markdown', disable_web_page_preview=True)
        elif search_data == None:
            await bot.send_message(message['from'].id, 'This is a new search, please wait')
            searc = Search_sce() # Класс для поиска
            se = await searc.search_sce(str(message.text))
            if se:
                #print("se>>",se)
                #infos = Get_info(client=client)
                infos = Get_info_url()
                info='👉 Your advertising could be here 👈\n'
                data_db=[]
                for i in se:
                    #print('###################',str(i['link']))
                    try:
                        #x ,temp_data_db  = await infos.get_info(str(i['link']))
                        x ,temp_data_db  = await infos.info_url(str(i['link'])) # Рабочий но не асинхроный

                        #x ,temp_data_db  = asyncio.create_task(infos.info_url(str(i['link'])))
                        if x:
                            #print("x===", x)
                            info += x
                            data_db.append(temp_data_db)
                    except TypeError:
                        #print('PASS')
                        pass

                    #print("info>>",info)
                # Добавляем значения поисска в базу
                temp=[str(temp_search),1]
                insert_table_searchs(temp)
                tempdatadb = sql_select_search(temp_search)
                # б
                #print("tempdatadb >>",tempdatadb)
                for i in data_db:
                    # print("ID Search >>",tempdatadb[0])
                    # print("URL >>> ",i[0])
                    # print('Name >> ',i[1])
                    # print('Type >> ',i[2])
                    # (LINK_ID,NAME,TYPE_NAME,TEG,LINK)
                    i_temp=[tempdatadb[0],i[1],i[2],'test_TEG',i[0]]
                    insert_table_link(i_temp)
                print("Это нужно добавить в базу>>> ",data_db,' <<<')
                #print('info>>>>',info)
                await bot.send_message(message['from'].id, info, parse_mode='Markdown',disable_web_page_preview=True)
            elif se ==False:
                await bot.send_photo(chat_id=message['from'].id, photo=open('img/img.png', 'rb'),caption ='Sorry, search:\n'+message.text+'\nnot found!')
                #await bot.send_message(message['from'].id, info, parse_mode='Markdown', disable_web_page_preview=True)

    elif user and user[0][3]=='False':
        print('test>>1')
        try:
            if user_data['type'] == 'ads_modify_title':
                print('test>>2')
                ads = sql_select_user_id_on_ads(int(message["from"].id))
                update_ads(ads[0][0],'title',message.text)
                await bot.send_message(message['from'].id, 'Please enter your subtitle',reply_markup=cancel(types))
                user_data['type'] = 'ads_modify_subtitle'
            elif user_data['type'] == 'ads_modify_subtitle':
                print('test>>3')
                ads = sql_select_user_id_on_ads(int(message["from"].id))
                update_ads(ads[0][0],'subtitle',message.text)
                await bot.send_message(message['from'].id, 'Please enter your channel/group link.',reply_markup=cancel(types))
                user_data['type'] = 'ads_modify_link'
            elif user_data['type'] == 'ads_modify_link':
                print('test>>4')
                ads = sql_select_user_id_on_ads(int(message["from"].id))
                update_ads(ads[0][0],'linke',message.text)
                await bot.send_message(message['from'].id, 'Modified successfully！')#,reply_markup=cancel(types))
                user_data['type'] = 'ads_modify_title'
                update_user(int(message["from"].id), "search", 'True')

                # Проверяем есть ли такое слово в базе данных
            elif user_data['type'] == 'test_randomad':
                print('test>>test_randomad\nСлово для проверки: ',message.text)
                ads = sql_select_title_id_on_ads(message.text)
                print(f'Результат поиска по базе: {ads}')
                if len(ads) == 0:
                    print("Ключевое слово не найдено!\n")
                    type = 'ad_randomad_'
                    await bot.send_message(message['from'].id, 'You can use this word!', reply_markup=nexts(types,type))
                else:
                    #await bot.send_message(message['from'].id, 'This word is already in use! Try another word!')
                    #type = "test_try"
                    mess = 'This word is already in use! Try another word!'
                    await bot.send_message(message['from'].id, mess ,reply_markup=cancel(types))
                    #
            elif user_data['type'] == 'test_first_place_ad':
                print('test>>test_first_place_ad\nСлово для проверки: ', message.text)
                ads = sql_select_title_id_on_ads(message.text)
                print(f'Результат поиска по базе: {ads}')
                if len(ads) == 0:
                    print("Ключевое слово не найдено!\n")
                    type = 'ad_first_place_ad'
                    await bot.send_message(message['from'].id, 'You can use this word!',
                                               reply_markup=nexts(types, type))
                else:
                        # await bot.send_message(message['from'].id, 'This word is already in use! Try another word!')
                        # type = "test_try"
                    mess = 'This word is already in use! Try another word!'
                    await bot.send_message(message['from'].id, mess, reply_markup=cancel(types))
                    #
            elif user_data['type'] == 'test_second_place_ad':
                print('test>>test_first_place_ad\nСлово для проверки: ', message.text)
                ads = sql_select_title_id_on_ads(message.text)
                print(f'Результат поиска по базе: {ads}')
                if len(ads) == 0:
                    print("Ключевое слово не найдено!\n")
                    type = 'ad_second_place_ad'
                    await bot.send_message(message['from'].id, 'You can use this word!',
                                               reply_markup=nexts(types, type))
                else:
                        # await bot.send_message(message['from'].id, 'This word is already in use! Try another word!')
                        # type = "test_try"
                    mess = 'This word is already in use! Try another word!'
                    await bot.send_message(message['from'].id, mess, reply_markup=cancel(types))
                    #
            elif user_data['type'] == 'test_third_place_ad':
                print('test>>test_first_place_ad\nСлово для проверки: ', message.text)
                ads = sql_select_title_id_on_ads(message.text)
                print(f'Результат поиска по базе: {ads}')
                if len(ads) == 0:
                    print("Ключевое слово не найдено!\n")
                    type = 'ad_third_place_ad'
                    await bot.send_message(message['from'].id, 'You can use this word!',
                                               reply_markup=nexts(types, type))
                else:
                        # await bot.send_message(message['from'].id, 'This word is already in use! Try another word!')
                        # type = "test_try"
                    mess = 'This word is already in use! Try another word!'
                    await bot.send_message(message['from'].id, mess, reply_markup=cancel(types))
                    #
            elif user_data['type'] == 'test_infomercial_ad':
                print('test>>test_first_place_ad\nСлово для проверки: ', message.text)
                ads = sql_select_title_id_on_ads(message.text)
                print(f'Результат поиска по базе: {ads}')
                if len(ads) == 0:
                    print("Ключевое слово не найдено! ad_infomercial_ad \n")
                    type = 'ad_infomercial_ad'
                    await bot.send_message(message['from'].id, 'You can use this word!',
                                               reply_markup=nexts(types, type))
                else:
                        # await bot.send_message(message['from'].id, 'This word is already in use! Try another word!')
                        # type = "test_try"
                    mess = 'This word is already in use! Try another word!'
                    await bot.send_message(message['from'].id, mess, reply_markup=cancel(types))

        except KeyError as error:
            print(error)
        #user_data['type'] = 'chanel'
    elif user ==False:
        print('ERROR USER')
        await bot.send_message(message['from'].id, 'send /start')
            # for i in info:
            #     print('info>>',i)
            #await bot.send_message(message['from'].id,'')

if __name__ == '__main__':
    executor.start_polling(dp)

