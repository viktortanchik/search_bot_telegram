from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from bassa import sql_select_user_id_on_ads
#button_hi = KeyboardButton('Привет! 👋')
from language import language_keyboard

def keyboard(leng):
    menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    #button_hi=['🏁 Language: English (English)','📢 Channels','👥 Groups','🤖 Bots','🏷 Tags','❓ Help!','👤 Me']

    button_hi=['🏁 Language',language_keyboard[leng+'_help'],language_keyboard[leng+'_me']]
    print(f'button_hi>>{button_hi}')
    menu_kb.add(*button_hi)

    my_kb=ReplyKeyboardMarkup(resize_keyboard=True)
    return menu_kb

def get_keyboard(types):
    # Генерация клавиатуры.
    buttons = [
        types.InlineKeyboardButton(text="⬅️", callback_data="num_decr"),
        types.InlineKeyboardButton(text="➡️", callback_data="num_incr"),
        #types.InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")
    ]
    # Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
    # уйдёт на следующую строку
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard

def modify_keyboard(types,id):
    keyboard = types.InlineKeyboardMarkup()
    ads = sql_select_user_id_on_ads(id)
    if ads:
        buttons = []
        for i in ads:
            buttons.append(types.InlineKeyboardButton(text=str(i[4]), callback_data="ads"+str(i[0])))
        keyboard.add(*buttons)
        #keyboard.add(types.InlineKeyboardButton(text="❌Cancel", callback_data="cancel"))
        return keyboard
'''


def buyad_inli_keyboard(types):
    keyboard = types.InlineKeyboardMarkup()
    #keyboard.add(types.InlineKeyboardButton(text="🔥Randomly suggest popular channels ads", callback_data="ad_randomad_"))
    keyboard.add(
        types.InlineKeyboardButton(text="🔥Randomly suggest popular channels ads", callback_data="test_ad_randomad_"))
    keyboard.add(types.InlineKeyboardButton(text="🥇keyword ranking ads", callback_data="test_ad_first_place_ad"))
    keyboard.add(types.InlineKeyboardButton(text="🥈top of search results", callback_data="test_ad_second_place_ad"))
    keyboard.add(types.InlineKeyboardButton(text="🥉Group built-in top ad", callback_data="test_ad_third_place_ad"))
    keyboard.add(types.InlineKeyboardButton(text="🏅Join the group infomercial", callback_data="test_ad_infomercial_ad"))
    return keyboard

def choice_tariff_randomad_keyboard(types):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="❌Cancel", callback_data="cancel"))
    keyboard.add(types.InlineKeyboardButton(text="✅pay", callback_data="choice_tariff_pay_randomad"))
    keyboard.add(types.InlineKeyboardButton(text="Advertising Effectiveness❓", callback_data="choice_tariff_advertising_randomad"))
    return keyboard

def choice_tariff_keyword_keyboard(types):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="❌Cancel", callback_data="cancel"))
    keyboard.add(types.InlineKeyboardButton(text="✅pay", callback_data="choice_tariff_pay_keyword"))
    keyboard.add(types.InlineKeyboardButton(text="Advertising Effectiveness❓", callback_data="choice_tariff_advertising_keyword"))
    return keyboard

def choice_tariff_ad_second_place_ad(types):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="❌Cancel", callback_data="cancel"))
    keyboard.add(types.InlineKeyboardButton(text="✅pay", callback_data="choice_tariff_pay_ad_second_place_ad"))
    keyboard.add(types.InlineKeyboardButton(text="Advertising Effectiveness❓", callback_data="choice_tariff_advertising_ad_second_place_ad"))
    return keyboard

def choice_tariff_ad_third_place_ad(types):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="❌Cancel", callback_data="cancel"))
    keyboard.add(types.InlineKeyboardButton(text="✅pay", callback_data="choice_tariff_pay_ad_third_place_ad"))
    keyboard.add(types.InlineKeyboardButton(text="Advertising Effectiveness❓", callback_data="choice_tariff_advertising_ad_second_place_ad"))
    return keyboard

def choice_tariff_ad_infomercial_place_ad(types):
    print('TEST2.3')
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="❌Cancel", callback_data="cancel"))
    keyboard.add(types.InlineKeyboardButton(text="✅pay", callback_data="choice_tariff_pay_ad_infomercial_place_ad"))
    keyboard.add(types.InlineKeyboardButton(text="Advertising Effectiveness❓", callback_data="choice_tariff_advertising_ad_second_place_ad"))
    return keyboard

def tariff_pay_end(types):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="🔙Back", callback_data="choice_tariff_back"))
    keyboard.add(types.InlineKeyboardButton(text="✅Modification", callback_data="choice_tariff_modification"))
    keyboard.add(types.InlineKeyboardButton(text="〽️Purchase History", callback_data="choice_tariff_purchase_history"))
    return keyboard

def modify_keyboard(types,id):
    keyboard = types.InlineKeyboardMarkup()
    ads = sql_select_user_id_on_ads(id)
    if ads:
        buttons = []
        for i in ads:
            buttons.append(types.InlineKeyboardButton(text=str(i[4]), callback_data="ads"+str(i[0])))
        keyboard.add(*buttons)
        keyboard.add(types.InlineKeyboardButton(text="❌Cancel", callback_data="cancel"))
        return keyboard
    else:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(text="🔥Randomly suggest popular channels ads", callback_data="ad_randomad_"))
        keyboard.add(types.InlineKeyboardButton(text="🥇keyword ranking ads", callback_data="ad_first_place_ad"))
        keyboard.add(types.InlineKeyboardButton(text="🥈top of search results", callback_data="ad_second_place_ad"))
        keyboard.add(types.InlineKeyboardButton(text="🥉Group built-in top ad", callback_data="ad_third_place_ad"))
        keyboard.add(types.InlineKeyboardButton(text="🏅Join the group infomercial", callback_data="ad_infomercial_ad"))
        return keyboard



def cancel(types):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="❌Cancel", callback_data="cancel"))
    return keyboard

def nexts(types,type):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="✅NEXT", callback_data=type))
    return keyboard


'''


    # buttons = [
    #     types.InlineKeyboardButton(text="⬅️", callback_data="num_decr"),
    #     types.InlineKeyboardButton(text="➡️", callback_data="num_incr"),
    #     #types.InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")
    # ]


#🔰「ad」This is keyword advertising·