import os
import sys
import glob
import time
import telebot
from telebot import types
import psycopg2
import psycopg2.extras
import datetime
from datetime import datetime
import logging 
from decouple import config
from aiohttp import web

BOT_TOKEN = config('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
#app = web.Application()
admin_ids = [301284229, 1023605829, 295651970]


DB_HOST = config('DB_HOST')
DB_NAME = config('DB_NAME')
DB_USERN = config('DB_USERN')
DB_PASS = config('DB_PASS')
DATABASE_URL = config('DATABASE_URL')



#logger = telebot.logger
#telebot.logger.setLevel(logging.INFO)



MODE = config('MODE')
if MODE == "dev":
    def run():
       # logger.info("Start in DEV MODE")
        bot.infinity_polling()



elif MODE == "prod":
    def run():
       # logger.info("Start in DEV MODE")
        bot.infinity_polling()
else:
    #logger.error("No mode specified")
    sys.exit()
#-------------------------------------------------
list = []


returnToMainBTN = types.KeyboardButton("القائمة الرئيسية")
# Main Menu Keyboard
mainKB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
requestBTN = types.KeyboardButton("طلب منتج")
pricesBTN = types.KeyboardButton("لائحة الأسعار")
blcBTN = types.KeyboardButton("معرفة رصيدي")
payBTN = types.KeyboardButton("شحن رصيدي")
contactBTN = types.KeyboardButton("تواصل معنا")
fbBTN = types.KeyboardButton("شاركنا رأيك واقتراحاتك")
mainKB.add(requestBTN, pricesBTN, blcBTN, payBTN, contactBTN, fbBTN)
# ---------------------------------
# Products Request Menu - Main Keyboard
requestKB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
product_1BTN = types.KeyboardButton("تحضير حساب حقيقي")
product_2BTN = types.KeyboardButton("تحضير حساب حقيقي مع SSN")
product_3BTN = types.KeyboardButton("SSN")
requestKB.add(product_2BTN)
requestKB.add(product_1BTN, product_3BTN)
requestKB.add(pricesBTN, blcBTN)
requestKB.add(returnToMainBTN)
# ---------------------------------
# Prices Menu - Main Keyboard
pricesKB = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
pricesKB.add(requestBTN, blcBTN)
pricesKB.add(returnToMainBTN)
# ---------------------------------
# Balance Menu - Main Keyboard
balanceKB = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
balanceKB.add(payBTN, requestBTN)
balanceKB.add(returnToMainBTN)
# ---------------------------------
# Return to Main Menu Menu Keyboard
# Contact
# fbBTN
returnToMainKB = types.ReplyKeyboardMarkup(resize_keyboard= True)
returnToMainKB.add(returnToMainBTN)
# ---------------------------------
# pay Menu - Main Keyboard
payKB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
visa_1BTN = types.KeyboardButton("Visa Token \"لا تدمج\"")
visa_2BTN = types.KeyboardButton("Visa Token \"تدمج\"")
payeerBTN = types.KeyboardButton("Payeer")
yobitBTN = types.KeyboardButton("Yobit Code")
syriatelBTN = types.KeyboardButton("Syriatel Cash")
mtnBTN = types.KeyboardButton("MTN Cash")
haramBTN = types.KeyboardButton("حوالة مالية (هرم)")
otherBTN = types.KeyboardButton("other")
payKB.add(visa_1BTN, visa_2BTN, payeerBTN, yobitBTN, syriatelBTN, mtnBTN, haramBTN, otherBTN, returnToMainBTN)
# ---------------------------------
# Visa Token Mergable - Pay Menu 
visatoken_1KB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
confirm_BTN = types.KeyboardButton("تأكيد")
cancel_BTN = types.KeyboardButton("إلغاء ❌")
visatoken_1KB.add(confirm_BTN, cancel_BTN, returnToMainBTN)
# ---------------------------------
# Yobit Code - Pay Menu 
yobitKB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
confirm_BTN = types.KeyboardButton("تأكيد")
yobitKB.add(confirm_BTN, cancel_BTN, returnToMainBTN)
# ---------------------------------
# Haram - Pay Menu
haramKB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
send_photoBTN = types.KeyboardButton("إرسال صورة وصل")
haramKB.add(send_photoBTN, cancel_BTN, returnToMainBTN)
# ---------------------------------
# Price List
# ---------------------------------
# Check Code
checkKB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
yes_BTN = types.KeyboardButton("نعم")
no_BTN = types.KeyboardButton("لا")
checkKB.add(no_BTN, yes_BTN, returnToMainBTN)
# ---------------------------------
# Request Product
req_productKB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
one_productBTN = types.KeyboardButton("طلب منتج واحد")
many_productBTN = types.KeyboardButton("طلب كمية")
req_productKB.add(one_productBTN, many_productBTN, cancel_BTN, returnToMainBTN)
# ---------------------------------
# check 
check2KB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
check2KB.add(confirm_BTN, cancel_BTN, returnToMainBTN)
# ---------------------------------
# check 
check3KB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
check3KB.add(cancel_BTN, returnToMainBTN)
# ---------------------------------
# Price List  
price_listKB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
blc_priceBTN = types.KeyboardButton("أسعار رصيد البوت")
product_priceBTN = types.KeyboardButton("أسعار منتجاتنا")
price_listKB.add(blc_priceBTN, product_priceBTN, returnToMainBTN)





# -------------------------------------------------------
# -------------------------------------------------------
# -------------------------------------------------------
# Admin Control Panel - Main
admin_cpKB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
add_balanceBTN = types.KeyboardButton("إضافة رصيد ⬆️")
reduce_balanceBTN = types.KeyboardButton("إنقاص رصيد ⬇️")
get_balanceBTN = types.KeyboardButton("استعلام عن رصيد ❓")
send_productBTN = types.KeyboardButton("إرسال منتج 🚚")
update_pricelistBTN = types.KeyboardButton("تحديث لائحة الأسعار ♻️")
reportsBTN = types.KeyboardButton("التقارير 📊")
verify_paymentsBTN = types.KeyboardButton("تأكيد الدفعات 💰")
send_messageBTN = types.KeyboardButton("إرسال رسالة 📝")
admin_cpKB.add(add_balanceBTN, reduce_balanceBTN, get_balanceBTN, send_productBTN, update_pricelistBTN, reportsBTN, verify_paymentsBTN, send_messageBTN)
# ---------------------------------
# Admin Control Panel - Reports:
reportsKB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
payments_reportBTN = types.KeyboardButton("تقرير عن الدفعات")
orders_reportBTN = types.KeyboardButton("تقرير عن الطلبات")
client_reportBTN = types.KeyboardButton("تقرير عن عميل")
full_reportBTN = types.KeyboardButton("تقرير شامل")
admincp_BTN = types.KeyboardButton("/AdminCP")
reportsKB.add(payments_reportBTN, orders_reportBTN, client_reportBTN, full_reportBTN, admincp_BTN)
# ---------------------------------
# Only Admin CP:
only_cpKB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=1)
only_cpKB.add(admincp_BTN)
# ---------------------------------
# Admin Control Panel - Reports - Period:
periodsKB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
h24BTN = types.KeyboardButton("آخر 24 ساعة")
weekBTN = types.KeyboardButton("آخر أسبوع")
monthBTN = types.KeyboardButton("آخر شهر")
admincp_BTN = types.KeyboardButton("/AdminCP")
periodsKB.add(h24BTN, weekBTN, monthBTN, admincp_BTN)

# ---------------------------------
# Admin Control Panel - Update Price List
update_pricelistKB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
balance_priceBTN = types.KeyboardButton("أسعار شحن رصيد البوت")
product_priceBTN = types.KeyboardButton("أسعار المنتجات")
admincp_BTN = types.KeyboardButton("/AdminCP")
update_pricelistKB.add(balance_priceBTN, product_priceBTN, admincp_BTN)
# ---------------------------------
# Admin Control Panel - Update Price List - Balance Price Update
balance_priceKB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
balance_priceKB.add(visa_1BTN, visa_2BTN, payeerBTN, yobitBTN, syriatelBTN, mtnBTN, admincp_BTN, haramBTN)
# ---------------------------------
# Admin Control Panel - Update Price List - Products Price Update
product_priceKB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
product_priceKB.add(product_2BTN)
product_priceKB.add(product_1BTN, product_3BTN)
product_priceKB.add(admincp_BTN)
# ---------------------------------
# Admin Control Panel - Update Price List - Balance Price Update - All
# Admin Control Panel - Update Price List - Products Price Update - All
update_priceKB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
update_priceKB.add(cancel_BTN, admincp_BTN)
# ---------------------------------
# Admin Control Panel - Send Product
send_productKB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
old_orderBTN = types.KeyboardButton("طلب سابق")
new_orderBTN = types.KeyboardButton("طلب جديد")
send_productKB.add(old_orderBTN, new_orderBTN, admincp_BTN)

# ---------------------------------
# Admin Control Panel - Send Product - Order Check
check_orderKB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
old_orderBTN = types.KeyboardButton("طلب سابق")
new_orderBTN = types.KeyboardButton("طلب جديد")
check_orderKB.add(confirm_BTN, cancel_BTN, admincp_BTN)
# ---------------------------------
# Admin Control Panel - Send Message 
send_message2KB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
send_message2KB.add(cancel_BTN, admincp_BTN)
# ---------------------------------
# Admin Control Panel - Send Message 2
send_message1KB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
single_messageBTN = types.KeyboardButton("رسالة فردية")
group_messageBTN = types.KeyboardButton("رسالة جماعية")
send_message1KB.add(single_messageBTN, group_messageBTN, cancel_BTN, admincp_BTN)
# ---------------------------------
# Admin Control Panel - Send Message - Confirm
check_messageKB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
check_messageKB.add(confirm_BTN, cancel_BTN, admincp_BTN)
# ---------------------------------
# Admin Control Panel - Send product
check_product1KB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
check_product1KB.add(one_productBTN, many_productBTN, cancel_BTN, admincp_BTN)




# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------
@bot.message_handler(commands = ["AdminCP"])
def admin_cp1(message):
    first_name = message.chat.first_name 
    if message.chat.id in admin_ids:
        # Welcome Message
        welcome = bot.send_message(message.chat.id,
        "أهلا وسهلا *{}* ❤️ \n هاي اللوحة خاصة بالمشرفين 😎، اكبس عالزر اللي بيلزمك 👍🏻".format(first_name),
        reply_markup = admin_cpKB, parse_mode="Markdown")
        bot.register_next_step_handler(welcome, admin_cp2)
    elif message.chat.id not in admin_ids:
        bot.send_message(message.chat.id,
        "بعتذر منك، ماعندك الصلاحية لتدخل هاي القائمة 🙂")


#-------------------
def admin_cp2(message):
    if message.text == "إضافة رصيد ⬆️":
        add_balance_step1(message)
    elif message.text == "إنقاص رصيد ⬇️":
        reduce_balance_step1(message)
    elif message.text == "استعلام عن رصيد ❓":
        get_balance_step1(message)
    elif message.text == "إرسال منتج 🚚":
        send_product1(message)
    elif message.text == "تحديث لائحة الأسعار ♻️":
        update_price_list1(message)
    elif message.text == "إرسال رسالة 📝":
        send_message1(message)
    elif message.text == "التقارير 📊":
        choose_report1(message)
    elif message.text == "تأكيد الدفعات 💰":
        verify_payment1(message)
    elif message.text == "/start":
        start(message)
    elif message.text == "/AdminCP":
        admin_cp1(message)
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
# Update Price List
def update_price_list1(message):
    update_type_ask = bot.send_message(message.chat.id,
    "من فضلك قم باختيار القائمة التي تريد تعديلها", reply_markup=update_pricelistKB)
    bot.register_next_step_handler(update_type_ask, update_price_list2)
#-------------------
def update_price_list2(message):
    if message.text == "أسعار شحن رصيد البوت":
        product_ask = bot.send_message(message.chat.id,
        "من فضلك قم باختيار وسيلة الدفع لتعديل السعر", reply_markup=balance_priceKB)
        bot.register_next_step_handler(product_ask, update_price_list3)

    elif message.text == "أسعار المنتجات":
        product_ask = bot.send_message(message.chat.id,
        "من فضلك قم باختيار المنتج لتعديل سعره", reply_markup=product_priceKB)
        bot.register_next_step_handler(product_ask, update_price_list3)

    elif message.text == "/AdminCP":
        admin_cp1(message)
#-------------------
def update_price_list3(message):
    con = psycopg2.connect(DATABASE_URL)
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    product = message.text
    if (product == "Visa Token \"لا تدمج\"" or product == "Visa Token \"تدمج\""
    or  product == "Payeer" or product == "Yobit Code"
    or  product == "Syriatel Cash" or product == "MTN Cash"
    or product == "تحضير حساب حقيقي" or product == "تحضير حساب حقيقي مع SSN"
    or product == "SSN" or product == "حوالة مالية (هرم)"):
        select_script =  'SELECT * FROM price_list WHERE product_name = %s'
        select_value = (product,)
        cur.execute(select_script, select_value)
        for record in cur.fetchall():
            old_price = str(record['price'])
        #old_price = price
        update_ask = bot.send_message(message.chat.id, 
        "اسم الخدمة: " + product + "\n"
        "السعر القديم: " + old_price + "\n" + 
        "يرجى كتابة السعر الجديد", reply_markup=update_priceKB)
        bot.register_next_step_handler(update_ask, update_price_list4, product)

    elif message.text == "إلغاء ❌":
        bot.send_message(message.chat.id, "تم إلغاء العملية", reply_markup=admin_cpKB)
        update_price_list1(message)
    elif message.text == "/AdminCP":
        admin_cp1(message)
    con.commit()
    cur.close()
    con.close() # End Database Connection
#-------------------
def update_price_list4(message, product):
    con = psycopg2.connect(  # Start Database Connection

                host = DB_HOST,
                database = DB_NAME,
                user = DB_USERN,
                password = DB_PASS,
                port = 5432
            )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    if (message.text != "إلغاء ❌" and message.text != "Visa Token \"لا تدمج\""
    and message.text != "Visa Token \"تدمج\"" and message.text != "/AdminCP"
    and  message.text != "Payeer" and message.text != "Yobit Code"
    and  message.text != "Syriatel Cash" and message.text != "MTN Cash"):
        msg_dt = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        username = "@" + message.from_user.username
        new_price = str(message.text)
        con = psycopg2.connect(  # Start Database Connection

                host = DB_HOST,
                database = DB_NAME,
                user = DB_USERN,
                password = DB_PASS,
                port = 5432
            )
        cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
        update_script = """UPDATE price_list SET
                            price = %s,
                            last_update_dt = %s,
                            editor = %s
                            WHERE product_name = %s"""
        update_value = (new_price, msg_dt, username, product)
        cur.execute(update_script, update_value)
        bot.send_message(message.chat.id, "تم تعديل السعر بنجاح !", reply_markup=admin_cpKB)
    elif message.text == "إلغاء ❌":
        bot.send_message(message.chat.id, "تم إلغاء العملية", reply_markup=admin_cpKB)
    elif message.text == "/AdminCP":
        admin_cp1(message)
    con.commit()
    cur.close()
    con.close() # End Database Connection
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
# Add Balance To Users By Admin
# Ask For Username
def add_balance_step1(message):
    username_ask = bot.send_message(message.chat.id,
    "اكتبلي اسم المستخدم اللي بدك تضفله رصيد 😁:\n@username",
    reply_markup=update_priceKB)
    bot.register_next_step_handler(username_ask, add_balance_step2)
#-------------------
# Ask For Balance
def add_balance_step2(message):
    con = psycopg2.connect(  # Start Database Connection

                host = DB_HOST,
                database = DB_NAME,
                user = DB_USERN,
                password = DB_PASS,
                port = 5432
            )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    if (message.text != "/AdminCP") & (message.text != "إلغاء ❌"):
        username_answer = str(message.text)
        select_script = "SELECT * FROM clients WHERE username = %s"
        select_value = (username_answer, )
        cur.execute(select_script, select_value)
        if bool(cur.rowcount) == True:
            balance_ask = bot.send_message(message.chat.id,
            "اكتبلي الرصيد اللي بدك تضيفه لـ *{}*".format(username_answer) ,reply_markup=update_priceKB, parse_mode="Markdown")
            bot.register_next_step_handler(balance_ask, add_balance_step3, username_answer)
        elif bool(cur.rowcount) == False:
            username_ask = bot.send_message(message.chat.id,
            "ما قدرت ألاقي *{}* بقاعدة البيانات 🙁 .. جرب مرة تانية".format(username_answer),
            reply_markup=update_priceKB, parse_mode="Markdown")
            bot.register_next_step_handler(username_ask, add_balance_step2)           
    elif message.text == "إلغاء ❌":
        bot.send_message(message.chat.id, "تم إلغاء العملية",  reply_markup=only_cpKB)
        
    elif message.text == "/AdminCP":
        admin_cp1(message)
    con.commit()
    cur.close()
    con.close() # End Database Connection    
#-------------------
# Add the requested Balance
def add_balance_step3(message, username_answer):
    con = psycopg2.connect(  # Start Database Connection

            host = DB_HOST,
            database = DB_NAME,
            user = DB_USERN,
            password = DB_PASS,
            port = 5432
        )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    if (message.text != "/AdminCP") & (message.text != "إلغاء ❌"):
        # Old Balance
        balance_answer = message.text
        #------------------
        # Getting old balance & tele_id
        select_script =  'SELECT * FROM clients WHERE username = %s'
        select_value = (username_answer,)
        cur.execute(select_script, select_value)
        for record in cur.fetchall():
            tele_id = record['tele_id']
            old_balance = str(record['balance'])
            username = record['username']
        #------------------
        # Updating The Balance
        update_script = 'UPDATE clients SET balance = balance + %s WHERE username = %s'
        update_value = (balance_answer, username_answer)
        cur.execute(update_script, update_value)
        #--------------------------------
        # Getting New Balance
        cur.execute(select_script, select_value)
        for record in cur.fetchall():
            new_balance = str(record['balance'])
        #-------------------------------
        # Succes Message For Admin & Client
        bot.send_message(message.chat.id, # For Admin
        "تمت إضافة *{}* SP إلى رصيد *{}* بنجاح !".format(f'{int(balance_answer):,}', username) +
        "\n الرصيد السابق: *{}* SP".format(f'{int(old_balance):,}') +
        "\n الرصيد الحالي: *{}* SP".format(f'{int(new_balance):,}'), reply_markup=only_cpKB, parse_mode="Markdown")
        bot.send_message(tele_id, # For Client
        "تم إضافة *{}* SP لرصيدك 😍!".format(f'{int(balance_answer):,}') +
        "\nرصيدك السابق: *{}* SP".format(f'{int(old_balance):,}') +
        "\nرصيدك الحالي: *{}* SP".format(f'{int(new_balance):,}'), reply_markup=mainKB , parse_mode="Markdown")
        
    elif message.text == "إلغاء ❌":
        bot.send_message(message.chat.id, "تم إلغاء العملية", reply_markup=only_cpKB)
        
    elif message.text == "/AdminCP":
        admin_cp1(message)
    con.commit()
    cur.close()
    con.close() # End Database Connection    
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
# Reduce Balance To Users By Admin
# Ask For Username
def reduce_balance_step1(message):
    username_ask = bot.send_message(message.chat.id,
    "اكتبلي اسم المستخدم اللي بدك تنقصله رصيده:\n@username",
    reply_markup=update_priceKB)
    bot.register_next_step_handler(username_ask, reduce_balance_step2)
#-------------------
# Ask For Balance
def reduce_balance_step2(message):
    con = psycopg2.connect(  # Start Database Connection

            host = DB_HOST,
            database = DB_NAME,
            user = DB_USERN,
            password = DB_PASS,
            port = 5432
        )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    if (message.text != "/AdminCP") & (message.text != "إلغاء ❌"):
        username_answer = message.text
        select_script = "SELECT * FROM clients WHERE username = %s"
        select_value = (username_answer, )
        cur.execute(select_script, select_value)
        if bool(cur.rowcount) == True:
            balance_ask = bot.send_message(message.chat.id,
            "اكتبلي الرصيد اللي بدك تنقصه من *{}*".format(username_answer) ,reply_markup=update_priceKB, parse_mode="Markdown")
            bot.register_next_step_handler(balance_ask, reduce_balance_step3, username_answer)
        elif bool(cur.rowcount) == False:
            username_ask = bot.send_message(message.chat.id,
            "ما قدرت ألاقي *{}* بقاعدة البيانات 🙁 .. جرب مرة تانية".format(username_answer),
            reply_markup=update_priceKB, parse_mode="Markdown")
            bot.register_next_step_handler(username_ask, reduce_balance_step2)
            
    elif message.text == "إلغاء ❌":
        bot.send_message(message.chat.id, "تم إلغاء العملية",  reply_markup=only_cpKB)
    elif message.text == "/AdminCP":
        admin_cp1(message)  
    con.commit()
    cur.close()
    con.close() # End Database Connection   
#-------------------
# Reduce the requested Balance
def reduce_balance_step3(message, username_answer):
    con = psycopg2.connect(  # Start Database Connection

            host = DB_HOST,
            database = DB_NAME,
            user = DB_USERN,
            password = DB_PASS,
            port = 5432
        )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    if (message.text != "/AdminCP") & (message.text != "إلغاء ❌"):
        # Old Balance
        balance_answer = message.text
        #------------------
        # Getting old balance & tele_id
        select_script =  'SELECT * FROM clients WHERE username = %s'
        select_value = (username_answer,)
        cur.execute(select_script, select_value)
        for record in cur.fetchall():
            tele_id = record['tele_id']
            old_balance = str(record['balance'])
            username = record['username']
        if int(old_balance) >= int(balance_answer):
            #------------------------
            # Updating The Balance
            update_script = 'UPDATE clients SET balance = balance - %s WHERE username = %s'
            update_value = (balance_answer, username_answer)
            cur.execute(update_script, update_value)
            #--------------------------------
            # Getting New Balance
            cur.execute(select_script, select_value)
            for record in cur.fetchall():
                new_balance = str(record['balance'])
            #-------------------------------
            # Succes Message For Admin & Client
            bot.send_message(message.chat.id, # For Admin
            "تم إنقاص *{}* SP من رصيد *{}* بنجاح".format(f'{int(balance_answer):,}', username) +
            "\n الرصيد السابق: *{}* SP".format(f'{int(old_balance):,}') +
            "\n الرصيد الحالي: *{}* SP".format(f'{int(new_balance):,}'), reply_markup=only_cpKB, parse_mode="Markdown")
            bot.send_message(tele_id, # For Client
            "تم إنقاص *{}* SP من رصيدك".format(f'{int(balance_answer):,}') +
            "\nرصيدك السابق: *{}* SP".format(f'{int(old_balance):,}') +
            "\nرصيدك الحالي: *{}* SP".format(f'{int(new_balance):,}'), reply_markup=mainKB , parse_mode="Markdown")
            
        elif old_balance < balance_answer:
            balance_ask = bot.send_message(message.chat.id,
            "ما بيصير يكون الرصيد اللي بدك تنقصه أكبر من الرصيد الحالي 😐" + 
            "\n الرصيد الحالي: *{}*".format(f'{int(old_balance):,}') +
            "\n جرب مرة تانية", reply_markup=update_priceKB, parse_mode="Markdown")
            bot.register_next_step_handler(balance_ask, reduce_balance_step3, username_answer)
    elif message.text == "إلغاء ❌":
        bot.send_message(message.chat.id, "تم إلغاء العملية",  reply_markup=only_cpKB)
        
    elif message.text == "/AdminCP":
        admin_cp1(message)  
    con.commit()
    cur.close()
    con.close() # End Database Connection
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# Get Client Balance By Admin
def get_balance_step1(message):
    username_ask = bot.send_message(message.chat.id,
    "اكتبلي اسم المستخدم اللي بدك تستفسر عن رصيده:\n@username",reply_markup=update_priceKB)
    bot.register_next_step_handler(username_ask, get_balance_step2)
#-------------------
def get_balance_step2(message):
    con = psycopg2.connect(  # Start Database Connection

        host = DB_HOST,
        database = DB_NAME,
        user = DB_USERN,
        password = DB_PASS,
        port = 5432
    )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    if (message.text != "/AdminCP") & (message.text != "إلغاء ❌"):
        username_answer = message.text
        select_script = "SELECT * FROM clients WHERE username = %s"
        select_value = (username_answer, )
        cur.execute(select_script, select_value)
        if bool(cur.rowcount) == True:
            cur.execute(select_script, select_value)
            for record in cur.fetchall():
                user_ID = str(record['id'])
                balance = str(record['balance'])
                username = str(record['username'])
            bot.send_message(message.chat.id,
            "ID: `{}`".format(user_ID) + 
            "\n اسم المستخدم: *{}*".format(username) + 
            "\n الرصيد الحالي: *{}*".format(f'{int(balance):,}') + " SP", reply_markup=only_cpKB, parse_mode="Markdown")
        elif bool(cur.rowcount) == False:
            username_ask = bot.send_message(message.chat.id,
            "ما قدرت ألاقي *{}* بقاعدة البيانات 🙁 .. جرب مرة تانية".format(username_answer),
            reply_markup=update_priceKB, parse_mode="Markdown")
            bot.register_next_step_handler(username_ask, get_balance_step2)        
    elif message.text == "إلغاء ❌":
        bot.send_message(message.chat.id, "تم إلغاء العملية", reply_markup=only_cpKB)
    elif message.text == "/AdminCP":
        admin_cp1(message)  
    
    con.commit()
    cur.close()
    con.close()
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
# Verify Payments
def verify_payment1(message):
    id_ask = bot.send_message(message.chat.id,
    "اكتبلي المعرف الخاص بالدفعة (Payment ID)", reply_markup = update_priceKB)
    bot.register_next_step_handler(id_ask, verify_payment2)
#-------------------
def verify_payment2(message):
    con = psycopg2.connect(  # Start Database Connection

        host = DB_HOST,
        database = DB_NAME,
        user = DB_USERN,
        password = DB_PASS,
        port = 5432
    )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    if (message.text != "/AdminCP") & (message.text != "إلغاء ❌"):
        payment_id = str(message.text)
        select_script = "SELECT * FROM received_payments WHERE id = %s"
        select_value = (payment_id, )
        cur.execute(select_script, select_value)
        # Checking If The Payment exists before
        if bool(cur.rowcount) == True:
            script_select = "SELECT * FROM received_payments WHERE id = %s"
            script_value = (payment_id, )
            cur.execute(script_select, script_value)
            for record in cur.fetchall():
                status = record["status"]
            # Checking If The Payment is Already Paid
            if status == "pending":
                value_ask = bot.send_message(message.chat.id, "اكتبلي قيمة الدفعة بعملة الدفعة نفسها", reply_markup = update_priceKB)
                bot.register_next_step_handler(value_ask, verify_payment3, payment_id)
            elif status == "paid":
                id_ask = bot.send_message(message.chat.id, "هاي الدفعة مأكدة من قبل .. جرب مرة تانية", reply_markup = update_priceKB)
                bot.register_next_step_handler(id_ask, verify_payment2)
        elif bool(cur.rowcount) == False:
            id_ask = bot.send_message(message.chat.id, "ما قدرت ألاقي هاي الدفعة بقاعدة البيانات 🙁 .. جرب مرة تانية")
            bot.register_next_step_handler(id_ask, verify_payment2)
    elif message.text == "إلغاء ❌":
        bot.send_message(message.chat.id, "تم إلغاء العملية", reply_markup=only_cpKB)
    elif message.text == "/AdminCP":
        admin_cp1(message) 
    con.commit()
    cur.close()
    con.close()
#-------------------
def verify_payment3(message, payment_id):
    con = psycopg2.connect(  # Start Database Connection

        host = DB_HOST,
        database = DB_NAME,
        user = DB_USERN,
        password = DB_PASS,
        port = 5432
    )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    if (message.text != "/AdminCP") & (message.text != "إلغاء ❌"):
        code_value = message.text
        # Gathering Order Information
        script_select = "SELECT * FROM received_payments WHERE id = %s"
        script_value = (payment_id, )
        cur.execute(script_select, script_value)
        for record in cur.fetchall():
            username = record["source"]
            type = record["type"]
            code = record["code"]
            price = record["price"]
            receive_dt = record["receive_dt"]
            status = record["status"]
            taken = record["taken"]
        balance_add = int(code_value)*int(price)
        bot.send_message(message.chat.id, "معلومات الدفعة:"
                    + "\n Payment ID: `{}`".format(payment_id)
                    + "\n النوع: *{}*".format(type)
                    + "\n اسم المستخدم: *{}*".format(username)
                    + "\n تاريخ الاستلام: *{}*".format(receive_dt)
                    + "\n الحالة: *{}*".format(status)
                    + "\n حالة الاستلام: *{}*".format(taken)
                    + "\n------------------"
                    + "\n الكود الخاص بالدفعة: `{}`".format(code)
                    + "\n سعر الشراء: *{:,}*".format(price) + " SP"
                    + "\n قيمة الكود: *{}*".format(code_value)
                    + "\n الرصيد اللي رح ينضاف: *{:,}*".format(balance_add) +  " SP", parse_mode="Markdown")
        check_ask = bot.send_message(message.chat.id, "بدك تأكد الدفعة؟", reply_markup=check_orderKB)
        bot.register_next_step_handler(check_ask, verify_payment4, payment_id, code_value)
    elif message.text == "إلغاء ❌":
        bot.send_message(message.chat.id, "تم إلغاء العملية", reply_markup=only_cpKB)
    elif message.text == "/AdminCP":
        admin_cp1(message)  
    con.commit()
    cur.close()
    con.close()
#-------------------
def verify_payment4(message, payment_id, code_value):
    con = psycopg2.connect(  # Start Database Connection

        host = DB_HOST,
        database = DB_NAME,
        user = DB_USERN,
        password = DB_PASS,
        port = 5432
    )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    if message.text == "تأكيد":
        # Gathering Payment Information
        script_select = "SELECT * FROM received_payments WHERE id = %s"
        script_value = (payment_id, )
        cur.execute(script_select, script_value)
        for record in cur.fetchall():
            username = record["source"]
            type = record["type"]
            price = record["price"]
        balance_add = int(code_value)*(price)
        script_select = "SELECT * FROM clients WHERE username = %s"
        script_value = (username, )
        cur.execute(script_select, script_value)
        for record in cur.fetchall():
            user_id = record["tele_id"]
            old_balance = str(record['balance'])
        #------------------
        # Updating The Balance
        update_script = 'UPDATE clients SET balance = balance + %s WHERE username = %s'
        update_value = (balance_add, username)
        cur.execute(update_script, update_value)
        #--------------------------------
        # Getting New Balance
        cur.execute(script_select, script_value)
        for record in cur.fetchall():
            new_balance = str(record['balance'])
        #-------------------------------
        # Succes Message For Admin & Client
        bot.send_message(message.chat.id, # For Admin
        "تم تأكيد الدفعة الخاصة بـ *{}*".format(username) +
        "\n Payment ID: `{}`".format(payment_id) +
        "\n من نوع  *{}*".format(type)  +
        "\n وإضافة *{:,}* SP إلى رصيد *{}* بنجاح !".format(balance_add, username) +
        "\n الرصيد السابق: *{:,}* SP".format(int(old_balance)) +
        "\n الرصيد الحالي: *{:,}* SP".format(int(new_balance)), parse_mode="Markdown", reply_markup=only_cpKB)
        bot.send_message(user_id, # For Client
        "تم تأكيد الدفعة الخاصة بك " +
        "\nوإضافة *{:,}* SP إلى رصيدك بنجاح !".format(balance_add) + 
        "\nرصيدك السابق: *{:,}* SP".format(int(old_balance)) + 
        "\nرصيدك الحالي: *{:,}* SP".format(int(new_balance)), parse_mode="Markdown", reply_markup=mainKB)
        #-------------------------------
        # Changing Deliver Status & Date in the Database
        check_dt = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        update_script = """UPDATE received_payments SET
                        taken = %s,
                        check_dt = %s,
                        status = %s,
                        value = %s
                        WHERE id = %s"""
        update_value = (True, check_dt, "paid", code_value, payment_id)
        cur.execute(update_script, update_value)
    #--------------------------
    elif message.text == "إلغاء ❌":
        bot.send_message(message.chat.id, "تم إلغاء العملية", reply_markup=only_cpKB)
    elif message.text == "/AdminCP":
        admin_cp1(message)
    con.commit()
    cur.close()
    con.close()
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
# Send Products to users
def send_product1(message):
    order_ask = bot.send_message(message.chat.id,
    "الطلب موجود من قبل؟ ولا بدك تعمل طلب جديد؟ 🤔 ", reply_markup = send_productKB)
    bot.register_next_step_handler(order_ask, send_product2)
#-------------------
def send_product2(message):
    if message.text == "طلب سابق":
        id_ask = bot.send_message(message.chat.id,
        "ابعتلي المعرف الخاص بالطلب (order_id)", reply_markup = update_priceKB)
        bot.register_next_step_handler(id_ask, send_product3)
    elif message.text == "طلب جديد":
        username_ask = bot.send_message(message.chat.id,
        "اكتبلي اسم المستخدم اللي بدك تبعتله المنتج", reply_markup=update_priceKB)
        bot.register_next_step_handler(username_ask, send_product_new2)
    elif message.text == "/AdminCP":
        admin_cp1(message)
#-------------------
def send_product3(message):
    con = psycopg2.connect(  # Start Database Connection

        host = DB_HOST,
        database = DB_NAME,
        user = DB_USERN,
        password = DB_PASS,
        port = 5432
    )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    if (message.text != "/AdminCP") & (message.text != "إلغاء ❌"):
        order_id = message.text
        # Gathering Order Information
        script_select = "SELECT * FROM product_orders WHERE id = %s"
        script_value = (order_id, )
        cur.execute(script_select, script_value)
        # Checking If The Order Exists
        if bool(cur.rowcount) == True:
            for record in cur.fetchall():
                username = record["client_username"]
                product = record["product_name"]
                price = record["price"]
                qnt = record["quantity"]
                total_price = price*qnt
                order_dt = record["order_dt"]
                status = record["status"]
                delivered = record["delivered"]
            if delivered == "no":
                bot.send_message(message.chat.id, "معلومات الطلب:"
                            + "\n Order ID : `{}`".format(order_id)
                            + "\n اسم المنتج: *{}*".format(product)
                            + "\n سعر المبيع: *{:,}*".format(price) + " SP"
                            + "\n الكمية: *{}*".format(qnt)
                            + "\n السعر الإجمالي: *{:,}*".format(total_price) + " SP"
                            + "\n اسم المستخدم: *{}*".format(username)
                            + "\n تاريخ الطلب: *{}*".format(order_dt)
                            + "\n الحالة: *{}*".format(status)
                            + "\n تم التسليم: *{}*".format(delivered), parse_mode="Markdown")
                check_ask = bot.send_message(message.chat.id,
                "بدك تبعت المنتجات؟", reply_markup=check_orderKB)
                bot.register_next_step_handler(check_ask, send_product4, order_id)
            elif delivered == "yes":
                id_ask = bot.send_message(message.chat.id,
                "تم تسليم الطلب سابقاً .. جرب مرة تانية", reply_markup = update_priceKB)
                bot.register_next_step_handler(id_ask, send_product3)
                
        elif bool(cur.rowcount) == False:
            id_ask = bot.send_message(message.chat.id,
            "ما قدرت ألاقي الطلب بقاعدة البيانات .. جرب مرة تانية", reply_markup = update_priceKB)
            bot.register_next_step_handler(id_ask, send_product3)
    elif message.text == "إلغاء ❌":
        bot.send_message(message.chat.id, "تم إلغاء العملية", reply_markup=only_cpKB)
    elif message.text == "/AdminCP":
        admin_cp1(message)  
    
    con.commit()
    cur.close()
    con.close()
#-------------------
def send_product4(message, order_id):
    con = psycopg2.connect(  # Start Database Connection

        host = DB_HOST,
        database = DB_NAME,
        user = DB_USERN,
        password = DB_PASS,
        port = 5432
    )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    if message.text == "تأكيد":
        
        # Gathering Order Information
        script_select = "SELECT * FROM product_orders WHERE id = %s"
        script_value = (order_id, )
        cur.execute(script_select, script_value)
        for record in cur.fetchall():
            username = record["client_username"]
            product = record["product_name"]
            price = record["price"]
            qnt = record["quantity"]
            total_price = price*qnt
            order_dt = record["order_dt"]
            status = record["status"]
            delivered = record["delivered"]
        script_select = "SELECT * FROM clients WHERE username = %s"
        script_value = (username, )
        cur.execute(script_select, script_value)
        for record in cur.fetchall():
            user_id = record["tele_id"]
        #--------------------------------
        # Dir Names
        if product == "Account":
            product_dir = "C:/Users/mjkha/Desktop/Personal/Programming Projects/bablyon/telegram_bot/products/account"
            sold_dir = product_dir + "_sold"
            available_products = len(os.listdir(product_dir))
        elif product == "Account+SSN":
            product_dir = "C:/Users/mjkha/Desktop/Personal/Programming Projects/bablyon/telegram_bot/products/account+ssn"
            sold_dir = product_dir + "_sold"
            available_products = len(os.listdir(product_dir))
        elif product == "SSN":
            product_dir = "C:/Users/mjkha/Desktop/Personal/Programming Projects/bablyon/telegram_bot/products/ssn"
            sold_dir = product_dir + "_sold"
            available_products = len(os.listdir(product_dir))
        if available_products >= qnt: #  Enough Products => Sending Imediatly
            #-------------------------------
            # Sending The Oldest File in the folder
            x = 1
            while x <= int(qnt):
                list_of_files = glob.glob(product_dir + '/*') # * means all if need specific format then *.csv
                latest_file = min(list_of_files, key=os.path.getctime)
                product_file = open(latest_file, "r")
                bot.send_document(user_id, product_file)
                product_file.close()
                #-------------------------
                # Changing File name And Moving it to The Sold Folder
                file_name = os.path.basename(latest_file)
                f_n_without_ext = os.path.splitext(file_name)[0]
                os.rename(latest_file, (sold_dir+"/"+ f_n_without_ext +"_sold.txt"))
                x = x + 1
            #-------------------------------
            # Changing Deliver Status & Date in the Database
            deliver_dt = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
            update_script = """UPDATE product_orders SET
                            delivered = %s,
                            deliver_dt = %s
                            WHERE id = %s"""
            update_value = (True, deliver_dt, order_id)
            cur.execute(update_script, update_value)
                #-----------------------
            # Success Message - Admin        
            for id in admin_ids:
                bot.send_message(id, "تم إرسال المنتج بنجاح !"
                + "\n Order ID: `{}`".format(order_id)
                + "\n اسم المنتج: *{}*".format(product)
                + "\n سعر المبيع: *{:,}*".format(price) + " SP"
                + "\n السعر الإجمالي: *{:,}*".format(total_price) + " SP"
                + "\n اسم المستخدم: *{}*".format(username)
                + "\n تاريخ الطلب: *{}*".format(order_dt)
                + "\n الحالة: *{}*".format(status)
                + "\n تم التسليم: *{}*".format(delivered), reply_markup=only_cpKB, parse_mode="Markdown")
            
            
            #--------------------------
        elif available_products < int(qnt): # No Enough Products => Rejecting Order
            
            check_ask = bot.send_message(message.chat.id,
            "ما لقيت عدد كافي من المنتجات 😐", reply_markup=check_orderKB)
            bot.register_next_step_handler(check_ask, send_product4, order_id)
            

        
    elif message.text == "إلغاء ❌":
        bot.send_message(message.chat.id, "تم إلغاء العملية", reply_markup=only_cpKB)
    elif message.text == "/AdminCP":
        admin_cp1(message)  
    


    con.commit()
    cur.close()
    con.close()
#-------------------
def send_product_new1(message):
    username_ask = bot.send_message(message.chat.id,
    "اكتبلي اسم المستخدم اللي بدك تبعتله المنتج", reply_markup=update_priceKB)
    bot.register_next_step_handler(username_ask, send_product_new2)

def send_product_new2(message):
    con = psycopg2.connect(  # Start Database Connection
            host = DB_HOST,
            database = DB_NAME,
            user = DB_USERN,
            password = DB_PASS,
            port = 5432
        )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    if (message.text != "/AdminCP") & (message.text != "إلغاء ❌"):
        username = message.text
        select_script = "SELECT * FROM clients WHERE username = %s"
        select_value = (username, )
        cur.execute(select_script, select_value)
        # Checking If the username exists
        if bool(cur.rowcount) == True:
            product_ask = bot.send_message(message.chat.id,
            "اختار الخدمة أو المنتج الذي بدك تبعته", reply_markup = product_priceKB)
            bot.register_next_step_handler(product_ask, send_product_new3, username)
        elif bool(cur.rowcount) == False:
            username_ask = bot.send_message(message.chat.id,
            "ما قدرت ألاقي *{}* بقاعدة البيانات 🙁 .. جرب مرة تانية".format(username),
            reply_markup=update_priceKB, parse_mode="Markdown")
            bot.register_next_step_handler(username_ask, send_product_new2)
    elif message.text == "إلغاء ❌":
        bot.send_message(message.chat.id, "تم إلغاء العملية", reply_markup=only_cpKB)
    elif message.text == "/AdminCP":
        admin_cp1(message)  
        
    con.commit()
    cur.close()
    con.close()  

def send_product_new3(message, username):
    con = psycopg2.connect(  # Start Database Connection
            host = DB_HOST,
            database = DB_NAME,
            user = DB_USERN,
            password = DB_PASS,
            port = 5432
        )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    select_script =  """SELECT * FROM price_list where product_name = %s"""
    product_ans = message.text
    if product_ans == "تحضير حساب حقيقي":
        cur.execute(select_script, (product_ans, ))
        for record in cur.fetchall():
            price = str(record["price"])
        product = "Account"
        ask_text = """اسم المنتج: تحضير حساب حقيقي\n
            **وصف مختصر**\n
            سعر المنتج: """ + str(price) + " SP"
        markup = check_product1KB
        product_ask = bot.send_message(message.chat.id, ask_text, reply_markup = markup)
        bot.register_next_step_handler(product_ask, send_product_new4, price, product, product_ans, username)
    #---------------------------
    elif product_ans == "تحضير حساب حقيقي مع SSN":
        cur.execute(select_script, (product_ans, ))
        for record in cur.fetchall():
            price = str(record["price"])
        product = "Account+SSN"
        ask_text = """اسم المنتج: تحضير حساب حقيقي مع SSN\n
            **وصف مختصر**\n
            سعر المنتج: """ + str(price) + " SP"
        markup = check_product1KB
        product_ask = bot.send_message(message.chat.id, ask_text, reply_markup = markup)
        bot.register_next_step_handler(product_ask, send_product_new4, price, product, product_ans, username)
    #---------------------------
    elif product_ans == "SSN":
        cur.execute(select_script, (product_ans, ))
        for record in cur.fetchall():
            price = str(record["price"])
        product = "SSN"
        ask_text = """اسم المنتج: SSN\n
            **وصف مختصر**\n
            سعر المنتج: """ + str(price) + " SP"
        markup = check_product1KB
        product_ask = bot.send_message(message.chat.id, ask_text, reply_markup = markup)
        bot.register_next_step_handler(product_ask, send_product_new4, price, product, product_ans, username)
    elif message.text == "/AdminCP":
        admin_cp1(message)  
    
    con.commit()
    cur.close()
    con.close()

def send_product_new4(message, price, product, product_ans, username):
    if (message.text == "طلب منتج واحد"):
        msg_dt = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        qnt = 1
        order_id = product[0] + product[-1] + (username[1:3]) + str(int(time.time())) + (username[-3:-1])
        list.append((order_id, username, product , qnt, price, "paid", msg_dt, "no"))
        order_check = bot.send_message(message.chat.id,
        text = "معلومات الطلب الخاص بك:"
        + "\nاسم المستلم: *{}*".format(username)
        + "\nاسم المنتج: *{}*".format(product_ans)
        + "\nالكمية: *{}*".format(qnt)
        + "\nالسعر الإجمالي: *{:,}*".format(int(qnt*price))
        + "\nاضغط زر \"تأكيد\" لتأكيد الطلب"
        + "\nاضغط زر \"إلغاء ❌\" لإلغاء الطلب.", reply_markup = check_messageKB, parse_mode="Markdown")
        bot.register_next_step_handler(order_check, send_product_new6, price, qnt, product, order_id, username)
    elif message.text == "طلب كمية":
        qnt_ask = bot.send_message(message.chat.id,
        "اكتبلي كمية المنتجات اللي بدك تبعتها", reply_markup = send_message2KB)
        bot.register_next_step_handler(qnt_ask, send_product_new5, price, product, product_ans, username)
    elif message.text == "إلغاء ❌":
        bot.send_message(message.chat.id, "تم إلغاء العملية", reply_markup=only_cpKB)
    elif message.text == "/AdminCP":
        admin_cp1(message)  

def send_product_new5(message, price, product, product_ans, username):
    if (message.text != "/AdminCP") & (message.text != "إلغاء ❌"):
        msg_dt = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        qnt = message.text
        order_id = product[0] + product[-1] + (username[1:3]) + str(int(time.time())) + (username[-3:-1])
        list.append((order_id, username, product , qnt, price, "paid", msg_dt, "no"))
        order_check = bot.send_message(message.chat.id,
        text = "معلومات الطلب الخاص بك:"
        + "\nاسم المستلم: *{}*".format(username)
        + "\nاسم المنتج: *{}*".format(product_ans)
        + "\nالكمية: *{}*".format(qnt)
        + "\nالسعر الإجمالي: *{:,}*".format(int(qnt)*int(price))
        + "\nاضغط زر \"تأكيد\" لتأكيد الطلب"
        + "\nاضغط زر \"إلغاء ❌\" لإلغاء الطلب.", reply_markup = check_messageKB, parse_mode="Markdown")
        bot.register_next_step_handler(order_check, send_product_new6, price, qnt, product, order_id, username)
    elif message.text == "إلغاء ❌":
        bot.send_message(message.chat.id, "تم إلغاء العملية", reply_markup=only_cpKB)
    elif message.text == "/AdminCP":
        admin_cp1(message)  

def send_product_new6(message, price, qnt, product, order_id, username):
    con = psycopg2.connect(  # Start Database Connection

            host = DB_HOST,
            database = DB_NAME,
            user = DB_USERN,
            password = DB_PASS,
            port = 5432
            )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    # Dir Names:
    if product == "Account":
        product_dir = "C:/Users/mjkha/Desktop/Personal/Programming Projects/bablyon/telegram_bot/products/account"
        sold_dir = product_dir + "_sold"
        available_products = len(os.listdir(product_dir))
    elif product == "Account+SSN":
        product_dir = "C:/Users/mjkha/Desktop/Personal/Programming Projects/bablyon/telegram_bot/products/account+ssn"
        sold_dir = product_dir + "_sold"
        available_products = len(os.listdir(product_dir))
    elif product == "SSN":
        product_dir = "C:/Users/mjkha/Desktop/Personal/Programming Projects/bablyon/telegram_bot/products/ssn"
        sold_dir = product_dir + "_sold"
        available_products = len(os.listdir(product_dir))
    #-------------------------------
    if message.text == "تأكيد":
        first_name = message.chat.first_name
        # Getting Old Balance
        select_script =  'SELECT * FROM clients WHERE username = %s'
        select_value = (username,)
        cur.execute(select_script, select_value)
        for record in cur.fetchall():
            old_balance = str(record['balance'])
        #------------------------------
        # Checking if the balance is enough
        if (int(qnt)*int(price)) <= int(old_balance):
            # Checing If the Products are Enough
            if available_products >= int(qnt): #  Enough Products => Sending Imediatly
                # Inserting Order in the database
                for d in list:
                        script_insert = "INSERT into product_orders (id, client_username, product_name, quantity, price, status, order_dt, delivered) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                        script_value = d
                        cur.execute(script_insert, script_value)
                #----------------------------
                    # Updating Balance
                update_script = "UPDATE clients SET balance = balance - %s WHERE username = %s"
                update_value = ((int(qnt)*int(price)), username)
                cur.execute(update_script, update_value)
                #--------------------
                # Getting The New Balance
                cur.execute(select_script, select_value)
                for record in cur.fetchall():
                    new_balance = str(record['balance'])
                    tele_id = record['tele_id']
                #-------------------------------
                # Sending The Oldest File in the folder
                x = 1
                while x <= int(qnt):
                    list_of_files = glob.glob(product_dir + '/*') # * means all if need specific format then *.csv
                    latest_file = min(list_of_files, key=os.path.getctime)
                    product_file = open(latest_file, "r")
                    bot.send_document(tele_id, product_file)
                    product_file.close()
                    #-------------------------
                    # Changing File name And Moving it to The Sold Folder
                    file_name = os.path.basename(latest_file)
                    f_n_without_ext = os.path.splitext(file_name)[0]
                    os.rename(latest_file, (sold_dir+"/"+ f_n_without_ext +"_sold.txt"))
                    x = x + 1
                #-------------------------------
                # Changing Deliver Status & Date in the Database
                deliver_dt = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
                update_script = """UPDATE product_orders SET
                                delivered = %s,
                                deliver_dt = %s
                                WHERE id = %s"""
                update_value = ("yes", deliver_dt, order_id)
                cur.execute(update_script, update_value)
                #-----------------------
                # Success Message - Admin
                script_select = "SELECT * FROM product_orders WHERE id = %s"
                script_value = (order_id, )
                cur.execute(script_select, script_value)
                for record in cur.fetchall():
                    username = record["client_username"]
                    product = record["product_name"]
                    price = str(record["price"])
                    qnt = str(record["quantity"])
                    total_price = int(price)*int(qnt)
                    order_dt = record["order_dt"]
                    status = record["status"]
                    delivered = record["delivered"] 
                #--------------------------
                bot.send_message(tele_id,
                "رصيدك السابق: " + old_balance +" SP\nرصيدك الحالي: " + new_balance + " SP")
                #--------------------------
                for id in admin_ids:
                    bot.send_message(id, "طلب شراء منتج جديد من قبل " + message.from_user.username
                    + "\n Order ID: `{}`".format(order_id)
                    + "\n اسم المنتج: *{}*".format(product)
                    + "\n سعر المبيع: *{:,}*".format(int(price)) + " SP"
                    + "\n السعر الإجمالي: *{:,}*".format(int(total_price)) + " SP"
                    #+ "\n الاسم الأول: *{}*".format(first_name)
                    + "\n اسم المستخدم: *{}*".format(username)
                    + "\n تاريخ الطلب: *{}*".format(order_dt)
                    + "\n الحالة: *{}*".format(status)
                    + "\n تم التسليم: *{}*".format(delivered), parse_mode="Markdown")
                    
            elif available_products < int(qnt): # No Enough Products => Recording Order
                bot.send_message(message.chat.id,
                "عذراً، لا يوجد عدد كافي من المنتجات التي طلبتها", reply_markup=only_cpKB)
        elif (int(qnt)*int(price)) > int(old_balance):
            cur.execute(select_script, select_value)
            for record in cur.fetchall():
                balance = str(record['balance'])
            bot.send_message(message.chat.id,
            "عذراً، ليس لدى " + username + " رصيد كاف لإتمام العملية\n الرصيد الحالي: " + str(balance) + " SP", reply_markup = mainKB)          
    elif message.text == "إلغاء ❌":
        list.clear()
        bot.send_message(message.chat.id, "تم إلغاء العملية", reply_markup=only_cpKB)
    elif message.text == "القائمة الرئيسية":
        list.clear()
        admin_cp1(message)

    con.commit()
    cur.close()
    con.close()


#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
# Send Messages to users
def send_message1(message):
    type_ask = bot.send_message(message.chat.id,
    "هل تريد إرسال فردية إلى عضو واحد أم رسالة جماعية لجميع عملاء البوت؟", reply_markup = send_message1KB)
    bot.register_next_step_handler(type_ask, send_message2)
#----------------
def send_message2(message):
    type_ans = message.text
    if type_ans == "رسالة جماعية":
        send_message3(message, type_ans)
    elif type_ans == "رسالة فردية":
        username_ask = bot.send_message(message.chat.id,
        "من فضلك قم بإرسال اسم المستخدم بالشكل التالي:\n" + 
        "@username", reply_markup = send_message2KB)
        bot.register_next_step_handler(username_ask, send_message3, type_ans)
    elif message.text == "إلغاء ❌":
        bot.send_message(message.chat.id, "تم إلغاء العملية")
        send_message1(message)
    elif message.text == "/AdminCP":
        admin_cp1(message)
#----------------
def send_message3(message, type_ans):
    con = psycopg2.connect(

            host = DB_HOST,
            database = DB_NAME,
            user = DB_USERN,
            password = DB_PASS,
            port = 5432
        )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    if (message.text != "إلغاء ❌") & (message.text != "/AdminCP"):
        username_ans = message.text
        if type_ans == "رسالة جماعية":
            message_ask = bot.send_message(message.chat.id,
            "من فضلك قم بإرسال الرسالة كما تريدها أن تصل", reply_markup = send_message2KB)
            bot.register_next_step_handler(message_ask, send_message4, type_ans, username_ans)
        elif type_ans == "رسالة فردية":
             # Check If User Already esists in the database
            select_script = "SELECT * FROM clients WHERE username = %s"
            select_value = (username_ans, )
            cur.execute(select_script, select_value)
            if bool(cur.rowcount) == True:
                message_ask = bot.send_message(message.chat.id,
                "من فضلك قم بإرسال الرسالة كما تريدها أن تصل", reply_markup = send_message2KB)
                bot.register_next_step_handler(message_ask, send_message4, type_ans, username_ans)
            elif bool(cur.rowcount) == False:
                bot.send_message(message.chat.id,
                "اسم المستخدم غير موجود، يرجى المحاولة مرة أخرى")
                send_message1(message)
    elif message.text == "إلغاء ❌":
        bot.send_message(message.chat.id, "تم إلغاء العملية")
        send_message1(message)
    elif message.text == "/AdminCP":
        admin_cp1(message)
    con.commit()
    cur.close()
    con.close()
#----------------
def send_message4(message, type_ans, username_ans):
    if (message.text != "إلغاء ❌") & (message.text != "/AdminCP"):
        message_ans = str(message.text)
        if type_ans == "رسالة جماعية":
            check_ask = bot.send_message(message.chat.id,
            "سوف تصل الرسالة إلى جميع مستخدمين البوت بالشكل التالي:\n-------------\n" + 
            message_ans + 
            "\n-------------\n هل تريد تأكيد العملية؟", reply_markup = check_messageKB)
            bot.register_next_step_handler(check_ask, send_message5, message_ans, username_ans, type_ans)
        elif type_ans == "رسالة فردية":
            check_ask = bot.send_message(message.chat.id,
            "سوف تصل الرسالة إلى " + username_ans + " بالشكل التالي:\n-------------\n" + 
            message_ans + 
            "\n-------------\n هل تريد تأكيد العملية؟", reply_markup = check_messageKB)
            bot.register_next_step_handler(check_ask, send_message5, message_ans, username_ans, type_ans)
    elif message.text == "إلغاء ❌":
        bot.send_message(message.chat.id, "تم إلغاء العملية")
        send_message1(message)
    elif message.text == "/AdminCP":
        admin_cp1(message)
#----------------
def send_message5(message, message_ans, username_ans, type_ans):
    con = psycopg2.connect(

            host = DB_HOST,
            database = DB_NAME,
            user = DB_USERN,
            password = DB_PASS,
            port = 5432
        )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    check_ans = message.text
    if check_ans == "تأكيد":    
        if type_ans == "رسالة جماعية":
            select_script = "SELECT tele_id FROM clients"
            cur.execute(select_script)
            for record in cur.fetchall():
                tele_id = record["tele_id"]
                bot.send_message(tele_id, message_ans)
            bot.send_message(message.chat.id, "تم إرسال الرسائل بنجاح")
            admin_cp1(message)
        elif type_ans == "رسالة فردية":
            select_script = "SELECT tele_id FROM clients WHERE username = %s"
            select_value = (username_ans, )
            cur.execute(select_script, select_value)
            for record in cur.fetchall():
                tele_id = record["tele_id"]
            bot.send_message(tele_id, message_ans)
            bot.send_message(message.chat.id, "تم إرسال الرسالة بنجاح")
            admin_cp1(message)
    elif message.text == "إلغاء ❌":
        bot.send_message(message.chat.id, "تم إلغاء العملية")
        send_message1(message)
    elif message.text == "/AdminCP":
        admin_cp1(message)
    con.commit()
    cur.close()
    con.close()
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------
def choose_report1(message):
    type_ask = bot.send_message(message.chat.id,
    "اختر نوع التقرير الذي تريده", reply_markup=reportsKB)
    bot.register_next_step_handler(type_ask, choose_report2)
#------------------
def choose_report2(message):
    if message.text == "تقرير عن الدفعات":
        payments_report1(message)
    elif message.text == "تقرير عن الطلبات":
        orders_report1(message)
    elif message.text == "تقرير عن عميل":
        client_report1(message)
    elif message.text == "تقرير شامل":
        pass
    elif message.text == "/AdminCP":
        pass
#------------------
#------------------
def payments_report1(message):
    period_ask = bot.send_message(message.chat.id,
    "من فضلك حدد مدة التقرير", reply_markup=periodsKB)
    bot.register_next_step_handler(period_ask, payments_report2)
#------------------
def payments_report2(message):
    con = psycopg2.connect(

            host = DB_HOST,
            database = DB_NAME,
            user = DB_USERN,
            password = DB_PASS,
            port = 5432
        )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    if message.text != "/AdminCP":
        period = message.text
        select_script = """SELECT * from received_payments
        where receive_dt >  CURRENT_DATE - INTERVAL %s"""
    
        if period == "آخر 24 ساعة":
            select_value = ("'24 hour'",)
        elif period == "آخر أسبوع":
            select_value = ("'7 day'",)
        elif period == "آخر شهر":
            select_value = ("'1 month'",)
        cur.execute(select_script, select_value)
        payments_count = cur.rowcount
        report_text = ""
        for record in cur.fetchall():
            username = record["source"]
            type = record["type"]
            code = record["code"]
            status = record["status"]
            receive_dt = record["receive_dt"]
            report_text += ("اسم المستخدم: " + username +
            "\n نوع الدفعة: " + type + 
            "\n كود الدفعة: " + code + 
            "\n الحالة: " + status + 
            "\n تاريخ الاستلام: " + str(receive_dt) + 
            "\n-----\n")
        bot.send_message(message.chat.id,
        "عدد الدفعات: " + str(payments_count) + 
        "\n------------\n معلومات الدفعات: \n" + report_text)
        admin_cp1(message)
    elif message.text == "/AdminCP":
        admin_cp1(message)

    con.commit()
    cur.close()
    con.close()
#------------------
#------------------
def orders_report1(message):
    period_ask = bot.send_message(message.chat.id,
    "من فضلك حدد مدة التقرير", reply_markup=periodsKB)
    bot.register_next_step_handler(period_ask, orders_report2)
#------------------
def orders_report2(message):
    con = psycopg2.connect(

            host = DB_HOST,
            database = DB_NAME,
            user = DB_USERN,
            password = DB_PASS,
            port = 5432
        )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    if message.text != "/AdminCP":
        period = message.text
        select_script = """SELECT * from product_orders
        where order_dt >  CURRENT_DATE - INTERVAL %s"""
    
        if period == "آخر 24 ساعة":
            select_value = ("'24 hour'",)
        elif period == "آخر أسبوع":
            select_value = ("'7 day'",)
        elif period == "آخر شهر":
            select_value = ("'1 month'",)
        cur.execute(select_script, select_value)
        orders_count = cur.rowcount
        report_text = ""
        for record in cur.fetchall():
            username = record["client_username"]
            product = record["product_name"]
            qnt = record["quantity"]
            delivered = record["delivered"]
            order_dt = record["order_dt"]
            report_text += ("\n اسم المستخدم: " + username +
            "\n اسم المنتج: " + product + 
            "\n الكمية: " + str(qnt) + 
            "\n تم التسليم: " + str(delivered) + 
            "\n تاريخ الطلب: " + str(order_dt) + 
            "\n-----")
        bot.send_message(message.chat.id,
        "عدد الطلبات: " + str(orders_count) + 
        "\n------------\n معلومات الطلبات: \n" + report_text)
        admin_cp1(message)
    elif message.text == "/AdminCP":
        admin_cp1(message)

    con.commit()
    cur.close()
    con.close()
#------------------
#------------------
def client_report1(message):
    client_ask = bot.send_message(message.chat.id,
    "من فضلك أرسل اسم المستخدم الخاص بالعميل", reply_markup=send_message2KB)
    bot.register_next_step_handler(client_ask, client_report2)

def client_report2(message):
    con = psycopg2.connect(

            host = DB_HOST,
            database = DB_NAME,
            user = DB_USERN,
            password = DB_PASS,
            port = 5432
        )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    if (message.text != "إلغاء ❌") & (message.text != "/AdminCP"):
        username = message.text
        select_script = "SELECT * FROM clients WHERE username = %s"
        select_value = (username, )
        cur.execute(select_script, select_value)
        if bool(cur.rowcount) == True:
            # Client General Info
            for record in cur.fetchall():
                id = record["id"]
                username = record["username"]
                cur_balance = record["balance"]
                join_dt = record["join_dt"]
                frst_name = record["first_name"]
            #-----------------------
            # Product Orders Info - All Time Paid Balance & Orders Count
            select_script = "SELECT * FROM product_orders WHERE client_username = %s"
            select_value = (username, )
            cur.execute(select_script, select_value)
            all_paid = 0
            orders_count = cur.rowcount
            for record in cur.fetchall():
                paid = record["quantity"]*record["price"]
                all_paid += paid
                qnt = record["quantity"]
            #----------
            # Product Orders Info - getting product 1 info
            select_script = "SELECT * FROM product_orders WHERE client_username = %s AND product_name = %s"
            select_value = (username, "Account+SSN")
            cur.execute(select_script, select_value)
            product1_count = 0
            for record in cur.fetchall():
                qnt = record["quantity"]
                product1_count += qnt

            #----------
            # Product Orders Info - getting product 2 info
            select_script = "SELECT * FROM product_orders WHERE client_username = %s AND product_name = %s"
            select_value = (username, "Account")
            cur.execute(select_script, select_value)
            product2_count = 0
            for record in cur.fetchall():
                qnt = record["quantity"]
                product2_count += qnt

            #----------
            # Product Orders Info - getting product 3 info
            select_script = "SELECT * FROM product_orders WHERE client_username = %s AND product_name = %s"
            select_value = (username, "SSN")
            cur.execute(select_script, select_value)
            product3_count = 0
            for record in cur.fetchall():
                qnt = record["quantity"]
                product3_count += qnt
            #-----------------------
            # Payments Info
            select_script = "SELECT * FROM received_payments WHERE source = %s"
            select_value = (username, )
            cur.execute(select_script, select_value)
            
            #-----------------------
            bot.send_message(message.chat.id,
            "🆔 المعرف الخاص بالعميل: " + id + 
            "\n 🧑🏽اسم العميل: " + frst_name + 
            "\n 🧑🏽‍💻 اسم المستخدم: " + username + 
            "\n 💰 الرصيد الحالي: " + str(cur_balance) + 
            "\n 📅 تاريخ الانضمام: " + str(join_dt) + 
            "\n------------------\n" + 
            "---طلبات الشراء--- " +
            "\n 1️⃣ المنتج (Account+SSN)، كمية المشتريات : " + str(product1_count) + 
            "\n 2️⃣ المنتج (Account)، كمية المشتريات : " + str(product2_count) + 
            "\n 3️⃣ المنتج (SSN)، كمية المشتريات : " + str(product3_count) + 
            "\n 🤩 إجمالي الرصيد المدفوع في طلبات الشراء: " + str(all_paid) + " SP" +
            "\n------------------\n" +
            "---الدفعات المستقبلة---" + 
            "\n (Visa_M)، قيمة المدفوعات:" + 
            "\n طريقة الدفع (Visa_NonM)، قيمة المدفوعات:" + 
            "\n طريقة الدفع (YobitCode)، قيمة المدفوعات:" + 
            "\n طريقة الدفع (Haram)، قيمة المدفوعات:" + 
            "\n طريقة الدفع (Payeer)، قيمة المدفوعات:" + 
            "\n إجمالي المدفوعات المستقبلة:" 

            )
        elif bool(cur.rowcount) == False:
            bot.send_message(message.chat.id,
            "اسم المستخدم غير موجود، يرجى المحاولة مرة أخرى")
            client_report1(message)

    elif message.text == "إلغاء ❌":
        bot.send_message(message.chat.id, "تم إلغاء العملية")
        send_message1(message)
    elif message.text == "/AdminCP":
        choose_report1(message)
    con.commit()
    cur.close()
    con.close()

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# Welcome Message & Store user data
@bot.message_handler(commands = ["start"])
def start(message):
    # Check If the user has a username
    if (message.from_user.username) is not None:
        username = "@" + message.from_user.username
        tele_id = message.chat.id
        first_name = message.chat.first_name
        msg_dt = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        user_id = (username[1:3]) + str(int(time.time())) + (username[-3:-1])
        #----------------------
        # Start Database Connection
        con = psycopg2.connect(

                host = DB_HOST,
                database = DB_NAME,
                user = DB_USERN,
                password = DB_PASS,
                port = 5432
            )
        cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
        #-----------------
        # Store user data into Database
        select_script = "SELECT * FROM clients WHERE username = %s"
        select_value = (username, )
        cur.execute(select_script, select_value)
            # Check If User Already esists in the database
        if bool(cur.rowcount) == False:
            insert_script = 'INSERT INTO clients (tele_id, username, balance, join_dt, id, first_name) VALUES (%s, %s, %s, %s, %s, %s)'
            insert_values = tele_id, username, 0, msg_dt, user_id, first_name
            cur.execute(insert_script, insert_values)
        elif bool(cur.rowcount) == True:
            print("user already exists")
            
        # Welcome Message
        bot.send_message(message.chat.id, "أهلاً بك في البوت الخاص بنا " + first_name + "\n كيف يمكنني مساعدتك؟", reply_markup = mainKB)
        #-----------------
        # Commit & End Database Connection
        con.commit()
        cur.close()
        con.close()
    elif (message.from_user.username) is None:
        first_name = message.chat.first_name
        bot.send_message(message.chat.id, "أهلاً بك في البوت الخاص بنا " + first_name + " !\n" +
        "نأسف لحدوث هذا الخطأ،" + 
         "\n من فضلك قم بإضافة اسم مستخدم (username)" + 
         "\n إلى حسابك على تيليجرام حتى تستطيع استخدام البوت بدون أي مشاكل.")
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------





@bot.message_handler(commands=['test'])
def test(message):
    # Start Database Connection
    send_message1(message)


#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
# Handling ReplyKeyboard Messages
@bot.message_handler(content_types=['text'])
def rep_MainKB(message):
    list = []
    list2 = []
    def get_method_step1(message):
        method_ask = bot.send_message(message.chat.id, "اختر وسيلة الدفع المناسبة لك", reply_markup= payKB)
        bot.register_next_step_handler(method_ask, get_method_step2)
    #---------------------------
    def get_method_step2(message):
        
        if (message.text == "Visa Token \"تدمج\"") | (message.text == "Visa Token \"لا تدمج\"") | (message.text == "Yobit Code"):
            get_codes_1(message)
        #---------------------------
        elif message.text == "حوالة مالية (هرم)":
            get_photo_1(message)
        #---------------------------
        elif (message.text == "Syriatel Cash") | (message.text == "MTN Cash") | (message.text == "Payeer"):
            get_trancid_1(message)
    #---------------------------
    def get_trancid_1(message):
        con = psycopg2.connect(  # Start Database Connection

            host = DB_HOST,
            database = DB_NAME,
            user = DB_USERN,
            password = DB_PASS,
            port = 5432
        )
        cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
        select_script =  """SELECT * FROM price_list where product_name = %s"""
        method_ans = message.text
        if method_ans == "Syriatel Cash":
            cur.execute(select_script, (method_ans, ))
            for record in cur.fetchall():
                price = str(record["price"])
            type = "Syriatel Cash"
            ask_text = ("كل 1 ليرة سورية من رصيد Syriatel Cash"+
            "\n تعادل " + price + " SP من رصيد البوت"+
            "\n من فضلك قم بإرسال المبلغ عن طريق التحويل اليدوي"+
            "\n إلى حساب التاجر التالي: 23274248" + 
            "\n ثم قم بإرسال رقم عملية التحويل هنا" )
        elif method_ans == "MTN Cash":
            cur.execute(select_script, (method_ans, ))
            for record in cur.fetchall():
                price = str(record["price"])
            type = "MTN Cash"
            ask_text = ("كل 1 ليرة سورية من رصيد MTN Cash"+
            "\n تعادل " + price + " SP من رصيد البوت"+
            "\n من فضلك قم بإرسال المبلغ عن طريق التحويل اليدوي"+
            "\n إلى حساب التاجر التالي: 23274248" + 
            "\n ثم قم بإرسال رقم عملية التحويل هنا" )
        elif method_ans == "Payeer":
            cur.execute(select_script, (method_ans, ))
            for record in cur.fetchall():
                price = str(record["price"])
            type = "Payeer"
            ask_text = ( "نقبل الدفع بعملة USD فقط"
            "\n كل 1 USD من رصيد Payeer"+
            "\n تعادل " + price + " SP من رصيد البوت"+
            "\n من فضلك قم بإرسال المبلغ إلى الحساب التالي: P1028248226" + 
            "\n ثم قم بإرسال رقم عملية التحويل هنا" )
        trancid_ask = bot.send_message(message.chat.id, ask_text, reply_markup = send_message2KB)
        bot.register_next_step_handler(trancid_ask, get_trancid_2, price, type)
        
    def get_trancid_2(message, price, type):
        username = ("@" + message.from_user.username)
        #---------------------
        if ((message.text != "إلغاء ❌") & (message.text != "القائمة الرئيسية")):
            payment_id = type[0:2] + (username[1:3]) + str(int(time.time())) + (username[-3:-1])
            msg_dt = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
            list.append((payment_id, username, message.text, type , "no", msg_dt, "pending", price))
            con = psycopg2.connect(  # Start Database Connection

            host = DB_HOST,
            database = DB_NAME,
            user = DB_USERN,
            password = DB_PASS,
            port = 5432
            )
            cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
            for d in list:
                script_insert = "INSERT into received_payments (id, source, code, type, taken, receive_dt, status, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                script_value = d
                cur.execute(script_insert, script_value)
            #------------------------
            # Sending Payments to Admins
            for id in admin_ids:
                bot.send_message(id,
                "تم استقبال دفعة جديدة !"
                + "\n Payment_ID: " + payment_id
                + "\n Type: " + type
                + "\n Price: " + str(price) + " SP"
                + "\n First Name: " 
                + "\n Username: " + username
                + "\n Date: " + str(msg_dt)
                + "\n Status: " + "pending"
                + "\n----------------"
                + "\n Payment Code: " + message.text
                + "\n Payment ID will be sent Again seperatly")
                bot.send_message(id, payment_id)
            #-----------------------
            # Success Message
            bot.send_message(message.chat.id, text =
            """تم استقبال طلبك بنجاح !\n
            مدة معالجة الطلب 24 ساعة من تاريخ إرسال رقم عملية التحويل.""", reply_markup = mainKB)
            con.commit()
            con.close()
        #-----------------------
        elif message.text == "إلغاء ❌":
            list.clear()
            # UnSuccess Message
            bot.send_message(message.chat.id, text = "تم إلغاء العملية.", reply_markup=payKB)
            get_method_step1(message)
        elif message.text == "القائمة الرئيسية":
            list.clear()
            bot.send_message(message.chat.id,
            "أهلاً بك في البوت الخاص بنا \n كيف يمكنني مساعدتك؟", reply_markup = mainKB)
    #---------------------------
    # visa_M & Visa NonM & Yobit Code
    def get_codes_1(message):
        con = psycopg2.connect(  # Start Database Connection

            host = DB_HOST,
            database = DB_NAME,
            user = DB_USERN,
            password = DB_PASS,
            port = 5432
        )
        cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
        select_script =  """SELECT * FROM price_list where product_name = %s"""
        method_ans = message.text
        if method_ans == "Yobit Code":
            cur.execute(select_script, (method_ans, ))
            for record in cur.fetchall():
                price = str(record["price"])
            type = "YobitCode"
            ask_text = ("كل 1$ يعادل " + str(price) +  " SP"+
            "\nنستقبل الأكواد من عملة USD فقط"+
            "\nيرجى إرسال كل كود برسالة منفصلة بالشكل التالي:"+
            "\nYOBITFR6LC8X3Q764YQGR4FY6NQVXKBTJQGRMUSD"+
            "\nبعد الانتهاء من إرسال الأكواد يرجى الضغط على زر \"تأكيد\""+
            "\n ملاحظة: بعد الضغط على زر تأكيد لا يمكن التراجع عن هذه الخطوة")
            markup = yobitKB

        elif method_ans == "Visa Token \"تدمج\"":
            cur.execute(select_script, (method_ans, ))
            for record in cur.fetchall():
                price = str(record["price"])
            type = "Visa_M"
            ask_text = ("كل 1$ يعادل " + str(price) + " SP"+
            "\nيرجى إرسال كل بطاقة برسالة منفصلة بالشكل التالي:"+
            "\nXXXX-XXXXXX-XXXX"+
            "\nبعد الانتهاء من إرسال بطاقات يرجى الضغط على زر \"تأكيد\""+
            "\n ملاحظة: بعد الضغط على زر تأكيد لا يمكن التراجع عن هذه الخطوة!")
            markup = visatoken_1KB

        elif method_ans == "Visa Token \"لا تدمج\"":
            cur.execute(select_script, (method_ans, ))
            for record in cur.fetchall():
                price = str(record["price"])
            type = "Visa_NonM"
            ask_text = ("كل 1$ يعادل " + str(price) + " SP"+
            "\nيرجى إرسال كل بطاقة برسالة منفصلة بالشكل التالي:"+
            "\nXXXX-XXXXXX-XXXX"+
            "\nبعد الانتهاء من إرسال بطاقات يرجى الضغط على زر \"تأكيد\""+
            "\n ملاحظة: بعد الضغط على زر تأكيد لا يمكن التراجع عن هذه الخطوة!")
            markup = visatoken_1KB
        code_ask = bot.send_message(message.chat.id, ask_text, reply_markup = markup)
        bot.register_next_step_handler(code_ask, get_codes_2, price, type)
    #---------------------------
    def get_codes_2(message, price, type):
        username = ("@" + message.from_user.username)
        #---------------------
        if ((message.text != "تأكيد") & (message.text != "إلغاء ❌")
        & (message.text != "القائمة الرئيسية") & (message.text != "/start")
        & (message.text != "Visa Token \"تدمج\"")):
            payment_id = type[0:2] + (username[1:3]) + str(int(time.time())) + (username[-3:-1])
            msg_dt = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
            list.append((payment_id, username, message.text, type , "no", msg_dt, "pending", price))
            list2.append(payment_id)
            code_ask_2 = bot.send_message(message.chat.id,
            text = "تم استقبال الكود الخاص بك، يمكنك إرسال كود آخر،" +
            "أو الضغط على زر \"تأكيد\" لتاكيد العملية.\n" +
            "اضغط زر \"إلغاء\" لإلغاء العملية.")
            bot.register_next_step_handler(code_ask_2, get_codes_2, price, type)
        elif message.text == "تأكيد":
            check_ask = bot.send_message(message.chat.id,
            ("***هذه الخطوة لا يمكن التراجع عنها***" + 
            "\n هل تريد بالتأكيد إرسال البطاقات السابقة جميعها؟"), reply_markup = checkKB)
            bot.register_next_step_handler(check_ask, get_codes_3, price, type)
        elif message.text == "إلغاء ❌":
            list.clear()
            # UnSuccess Message
            bot.send_message(message.chat.id, text = "تم إلغاء العملية.", reply_markup=payKB)
            get_method_step1(message)
        elif message.text == "القائمة الرئيسية":
            list.clear()
            bot.send_message(message.chat.id,
            "أهلاً بك في البوت الخاص بنا \n كيف يمكنني مساعدتك؟", reply_markup = mainKB)
    #---------------------------
    def get_codes_3(message, price, type):
        if message.text == "نعم":
            #------------------------
            # Gathering info
            username = ("@" + message.from_user.username)
            first_name = message.chat.first_name
            #------------------------
            # Insert Data Into Database
            con = psycopg2.connect(  # Start Database Connection

            host = DB_HOST,
            database = DB_NAME,
            user = DB_USERN,
            password = DB_PASS,
            port = 5432
            )
            cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
            for d in list:
                script_insert = "INSERT into received_payments (id, source, code, type, taken, receive_dt, status, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                script_value = d
                cur.execute(script_insert, script_value)
            #------------------------
            # Sending Payments to Admins
            for x in list2:
                payment_id = x
                script_select = "SELECT * FROM received_payments WHERE id = %s"
                script_value = (payment_id, )
                cur.execute(script_select, script_value)
                for record in cur.fetchall():
                    username = record["source"]
                    type = record["type"]
                    price = str(record["price"])
                    msg_dt = record["receive_dt"]
                    Status = record["status"]
                    payment_code = record["code"]
                for id in admin_ids:
                    bot.send_message(id,
                    "تم استقبال دفعة جديدة !"
                    + "\n Payment_ID: " + payment_id
                    + "\n Type: " + type
                    + "\n Price: " + str(price) + " SP"
                    + "\n First Name: " + first_name
                    + "\n Username: " + username
                    + "\n Date: " + str(msg_dt)
                    + "\n Status: " + Status
                    + "\n----------------"
                    + "\n Payment Code: " + payment_code
                    + "\n Payment ID will be sent Again seperatly")
                    bot.send_message(id, payment_id)
            #-----------------------
            # Success Message
            bot.send_message(message.chat.id, text =
            """تم استقبال جميع البطاقات بنجاح !\n
            مدة معالجة الطلب 24 ساعة من تاريخ إرسال البطاقة.""", reply_markup = mainKB)
            #-----------------------
        elif message.text == "لا":
            list.clear()
            # UnSuccess Message
            bot.send_message(message.chat.id, text = "تم إلغاء العملية.", reply_markup=mainKB)
        con.commit()
        con.close() # End Database Connection
    #---------------------------
    # حوالة مالية (هرم)
    def get_photo_1(message):
        ask_text = bot.send_message(message.chat.id,
        """كل 1 ليرة سورية\n
        تعادل 1 SP من رصيد البوت\n
        من فضلك قم بإرسال المبلغ المطلوب إضافته إلى رصيدك\n
        على بيانات التحويل التالية:
        اسم المستلم: محمد حسام خليلي\n
        المحافظة: دمشق\n
        الهاتف المحمول: 0955110691\n
        ثم اضغط زر 'إرسال صورة وصل' لتأكيد الدفعة الخاصة بك""", reply_markup=haramKB)
        bot.register_next_step_handler(ask_text, get_photo_2,)
   
    def get_photo_2(message,):
        if message.text == "إرسال صورة وصل":
            photo_ask = bot.send_message(message.chat.id,
            """من فضلك قم بإرسال صورة واضحة لوصل التحويل كاملاً،\n
            **مدة معالجة الطلب 24 ساعة من تاريخ إرسال صورة الوصل.""", reply_markup=check3KB)
            bot.register_next_step_handler(photo_ask, get_photo_3)
        elif message.text == "إلغاء ❌":
            get_method_step1(message)
        elif message.text == "القائمة الرئيسية":
            bot.send_message(message.chat.id,
            "أهلاً بك في البوت الخاص بنا \n كيف يمكنني مساعدتك؟", reply_markup = mainKB)
   
    def get_photo_3(message,):
        if (message.text != "إلغاء ❌") & (message.text != "القائمة الرئيسية") & (message.text != "تأكيد"):
            list.append(message.photo[-1].file_id)
            img = list[0]
            confirm_ask = bot.send_message(message.chat.id,
            text = "اضغط زر \"تأكيد\" لتأكيد العملية.", reply_markup=check2KB)
            bot.register_next_step_handler(confirm_ask, get_photo_4, img,)
        elif message.text == "إلغاء ❌":
            get_method_step1(message)
        elif message.text == "القائمة الرئيسية":
            bot.send_message(message.chat.id,
            "أهلاً بك في البوت الخاص بنا \n كيف يمكنني مساعدتك؟", reply_markup = mainKB)
        
    def get_photo_4(message, img,):
        con = psycopg2.connect(  # Start Database Connection

        host = DB_HOST,
        database = DB_NAME,
        user = DB_USERN,
        password = DB_PASS,
        port = 5432
        )
        cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
        if message.text == "تأكيد":
            # Gathering Information
            payment_id = "Ha" + (message.from_user.username[0:2]) + str(int(time.time())) + (message.from_user.username[-3:-1])
            msg_dt = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
            username = "@" + message.from_user.username
            first_name = message.chat.first_name
            price = "1"
            #-----------------------------
            # Insert Order in database
            script_insert = "INSERT into received_payments (id, source, code, type, receive_dt, status, price) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            script_value = (payment_id, username, "Image", "Haram", msg_dt, "pending", price)
            cur.execute(script_insert, script_value)
            for id in admin_ids:
                # Admin Message
                bot.send_photo(id, img,
                "تم استقبال دفعة جديدة !"
                + "\n المعرف (Payment_ID): " + payment_id
                + "\n النوع : " + "Haram"
                + "\n سعر المبيع: " + price + " SP"
                + "\n الاسم الاول: " + first_name
                + "\n اسم المستخدم: " + username
                + "\n تاريخ الإرسال: " + msg_dt
                + "\n الحالة: " + "pending")
                bot.send_message(id, payment_id)
            #-----------------------------
            # Client Message
            bot.send_message(message.chat.id, text = "تم استقبال طلبك بنجاح !", reply_markup=mainKB)
        elif message.text == "إلغاء ❌":
            get_method_step1(message)
        elif message.text == "القائمة الرئيسية":
            bot.send_message(message.chat.id,
            "أهلاً بك في البوت الخاص بنا \n كيف يمكنني مساعدتك؟", reply_markup = mainKB)
        con.commit()
        cur.close()
        con.close()

#------------------------------------------------
#------------------------------------------------
#------------------------------------------------
# طلب منتج
    def choose_product_1(message):
        product_ask = bot.send_message(message.chat.id, "اختر الخدمة أو المنتج الذي تريده", reply_markup = requestKB)
        bot.register_next_step_handler(product_ask, request_product_1)
    #---------------------------
    def request_product_1(message):
        con = psycopg2.connect(  # Start Database Connection
            host = DB_HOST,
            database = DB_NAME,
            user = DB_USERN,
            password = DB_PASS,
            port = 5432
        )
        cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
        select_script =  """SELECT * FROM price_list where product_name = %s"""
        product_ans = message.text
        
        if product_ans == "تحضير حساب حقيقي":
            cur.execute(select_script, (product_ans, ))
            for record in cur.fetchall():
                price = str(record["price"])
            product = "Account"
            ask_text = """اسم المنتج: تحضير حساب حقيقي\n
                **وصف مختصر**\n
                سعر المنتج: """ + str(price) + " SP"
            markup = req_productKB
            product_ask = bot.send_message(message.chat.id, ask_text, reply_markup = markup)
            bot.register_next_step_handler(product_ask, request_product_2, price, product, product_ans)
        #---------------------------
        elif product_ans == "تحضير حساب حقيقي مع SSN":
            cur.execute(select_script, (product_ans, ))
            for record in cur.fetchall():
                price = str(record["price"])
            product = "Account+SSN"
            ask_text = """اسم المنتج: تحضير حساب حقيقي مع SSN\n
                **وصف مختصر**\n
                سعر المنتج: """ + str(price) + " SP"
            markup = req_productKB
            product_ask = bot.send_message(message.chat.id, ask_text, reply_markup = markup)
            bot.register_next_step_handler(product_ask, request_product_2, price, product, product_ans)
        #---------------------------
        elif product_ans == "SSN":
            cur.execute(select_script, (product_ans, ))
            for record in cur.fetchall():
                price = str(record["price"])
            product = "SSN"
            ask_text = """اسم المنتج: SSN\n
                **وصف مختصر**\n
                سعر المنتج: """ + str(price) + " SP"
            markup = req_productKB
            product_ask = bot.send_message(message.chat.id, ask_text, reply_markup = markup)
            bot.register_next_step_handler(product_ask, request_product_2, price, product, product_ans)
        elif message.text == "معرفة رصيدي":
            my_balance(message)
        elif message.text == "لائحة الأسعار":
            price_list1(message)
        elif message.text == "القائمة الرئيسية":
            bot.send_message(message.chat.id,
            "أهلاً بك في البوت الخاص بنا \n كيف يمكنني مساعدتك؟", reply_markup = mainKB)
        con.commit()
        cur.close()
        con.close()
#---------------------------
    def request_product_2(message, price, product, product_ans):
        username = ("@" + message.from_user.username)
        #---------------------
        if (message.text == "طلب منتج واحد"):
            msg_dt = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
            qnt = 1
            order_id = product[0] + product[-1] + (username[1:3]) + str(int(time.time())) + (username[-3:-1])
            list.append((order_id, username, product , qnt, price, "paid", msg_dt, "no"))
            order_check = bot.send_message(message.chat.id,
            text = "معلومات الطلب خاص بك:\n"
            "اسم المنتج: " + product_ans + "\n" +
            "الكمية: " + str(qnt) + "\n" +
            "السعر الإجمالي: " + str(qnt*price) + "\n" +
            """اضغط زر "تأكيد" لتأكيد الطلب\n
            اضغط زر "إلغاء ❌" لإلغاء الطلب.""", reply_markup = check2KB)
            bot.register_next_step_handler(order_check, request_product_4, price, qnt, product, order_id)
        elif message.text == "طلب كمية":
            qnt_ask = bot.send_message(message.chat.id,
            "يرجى كتابة الكمية المطلوبة كرقم", reply_markup = check3KB)
            bot.register_next_step_handler(qnt_ask, request_product_3, price, product, product_ans)
        elif message.text == "إلغاء ❌":
            choose_product_1(message)
        elif message.text == "القائمة الرئيسية":
            bot.send_message(message.chat.id,
            "أهلاً بك في البوت الخاص بنا \n كيف يمكنني مساعدتك؟", reply_markup = mainKB)
    #---------------------------
    def request_product_3(message, price, product, product_ans):
        msg_dt = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        username = ("@" + message.from_user.username)
        qnt = message.text
        order_id = product[0] + product[-1] + (username[1:3]) + str(int(time.time())) + (username[-3:-1])
        list.append((order_id, username, product , qnt, price, "paid", msg_dt, "no"))
        
        order_check = bot.send_message(message.chat.id,
        text = "معلومات الطلب الخاص بك:\n"
        "اسم المنتج: " + product_ans + "\n" +
        "الكمية: " + str(qnt) + "\n" +
        "السعر الإجمالي: " + str(int(qnt)*int(price)) + "\n" +
        """اضغط زر "تأكيد" لتأكيد الطلب\n
        اضغط زر "إلغاء ❌" لإلغاء الطلب.""", reply_markup = check2KB)
        bot.register_next_step_handler(order_check, request_product_4, price, qnt, product, order_id)
    #---------------------------
    def request_product_4(message, price, qnt, product, order_id):
        con = psycopg2.connect(  # Start Database Connection

            host = DB_HOST,
            database = DB_NAME,
            user = DB_USERN,
            password = DB_PASS,
            port = 5432
            )
        cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
        # Dir Names:
        if product == "Account":
            product_dir = "C:/Users/mjkha/Desktop/Personal/Programming Projects/bablyon/telegram_bot/products/account"
            sold_dir = product_dir + "_sold"
            available_products = len(os.listdir(product_dir))
        elif product == "Account+SSN":
            product_dir = "C:/Users/mjkha/Desktop/Personal/Programming Projects/bablyon/telegram_bot/products/account+ssn"
            sold_dir = product_dir + "_sold"
            available_products = len(os.listdir(product_dir))
        elif product == "SSN":
            product_dir = "C:/Users/mjkha/Desktop/Personal/Programming Projects/bablyon/telegram_bot/products/ssn"
            sold_dir = product_dir + "_sold"
            available_products = len(os.listdir(product_dir))
        #-------------------------------
        if message.text == "تأكيد":
            # Getting Old Balance
            username = "@" + message.from_user.username
            select_script =  'SELECT * FROM clients WHERE username = %s'
            select_value = (username,)
            cur.execute(select_script, select_value)
            for record in cur.fetchall():
                old_balance = str(record['balance'])
            
            #------------------------------
            # Checking if the balance is enough
            if (int(qnt)*int(price)) <= int(old_balance):
                first_name = message.chat.first_name
                # Inserting Order in the database
                for d in list:
                        script_insert = "INSERT into product_orders (id, client_username, product_name, quantity, price, status, order_dt, delivered) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                        script_value = d
                        cur.execute(script_insert, script_value)
                #----------------------------
                 # Updating Balance
                update_script = "UPDATE clients SET balance = balance - %s WHERE username = %s"
                update_value = ((int(qnt)*int(price)), username)
                cur.execute(update_script, update_value)
                #--------------------
                # Getting The New Balance
                cur.execute(select_script, select_value)
                for record in cur.fetchall():
                    new_balance = str(record['balance'])
                # Checing If the Products are Enough
                if available_products >= int(qnt): #  Enough Products => Sending Imediatly
                    #-------------------------------
                    # Sending The Oldest File in the folder
                    x = 1
                    while x <= int(qnt):
                        list_of_files = glob.glob(product_dir + '/*') # * means all if need specific format then *.csv
                        latest_file = min(list_of_files, key=os.path.getctime)
                        product_file = open(latest_file, "r")
                        bot.send_document(message.chat.id, product_file)
                        product_file.close()
                        #-------------------------
                        # Changing File name And Moving it to The Sold Folder
                        file_name = os.path.basename(latest_file)
                        f_n_without_ext = os.path.splitext(file_name)[0]
                        os.rename(latest_file, (sold_dir+"/"+ f_n_without_ext +"_sold.txt"))
                        x = x + 1
                    #-------------------------------
                    # Changing Deliver Status & Date in the Database
                    deliver_dt = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
                    update_script = """UPDATE product_orders SET
                                    delivered = %s,
                                    deliver_dt = %s
                                    WHERE id = %s"""
                    update_value = ("yes", deliver_dt, order_id)
                    cur.execute(update_script, update_value)
                     #-----------------------
                    # Success Message - Admin
                    script_select = "SELECT * FROM product_orders WHERE id = %s"
                    script_value = (order_id, )
                    cur.execute(script_select, script_value)
                    for record in cur.fetchall():
                        username = record["client_username"]
                        product = record["product_name"]
                        price = str(record["price"])
                        qnt = str(record["quantity"])
                        total_price = int(price)*int(qnt)
                        order_dt = record["order_dt"]
                        status = record["status"]
                    
                    for id in admin_ids:
                        bot.send_message(id, "طلب شراء منتج جديد !"
                        + "\n Order_ID: " + order_id
                        + "\n Product: " + product
                        + "\n Price: " + str(price) + " SP"
                        + "\n Total Price: " + str(total_price) + " SP"
                        + "\n First Name: " + first_name
                        + "\n Username: " + username
                        + "\n Order Date: " + str(order_dt)
                        + "\n Status: " + status
                        + "\n Delivered: " + "Yes"
                        + "\n----------------"
                        + "\n Order ID will be sent Again seperatly")
                    bot.send_message(id, order_id)
                    #--------------------------
                    bot.send_message(message.chat.id,
                    "رصيدك السابق: " + old_balance +" SP\nرصيدك الحالي: " + new_balance + " SP", reply_markup = mainKB)
                
                elif available_products < int(qnt): # No Enough Products => Recording Order
                    print("no enough products")
                    
                    #-----------------------
                    # Success Message - Admin
                    script_select = "SELECT * FROM product_orders WHERE id = %s"
                    script_value = (order_id, )
                    cur.execute(script_select, script_value)
                    for record in cur.fetchall():
                        username = record["client_username"]
                        product = record["product_name"]
                        price = str(record["price"])
                        qnt = str(record["quantity"])
                        total_price = int(price)*int(qnt)
                        order_dt = record["order_dt"]
                        status = record["status"]
                    print(order_id)
                    for id in admin_ids:
                        bot.send_message(id, "طلب شراء منتج جديد !"
                        + "\n Order_ID: " + order_id
                        + "\n Product: " + product
                        + "\n Price: " + str(price) + " SP"
                        + "\n Total Price: " + str(total_price) + " SP"
                        + "\n First Name: " + first_name
                        + "\n Username: " + username
                        + "\n Order Date: " + str(order_dt)
                        + "\n Status: " + status
                        + "\n Delivered: " + "No"
                        + "\n----------------"
                        + "\n Order ID will be sent Again seperatly")
                    bot.send_message(id, order_id)
                    #-----------------------
                    # Success Message - Client
                    bot.send_message(message.chat.id,
                    "تم استقبال طلبك بنجاح !" + 
                    "\nمدة معالجة الطلب 24 ساعة من تاريخ إرسال الطلب.", reply_markup = mainKB)
                    bot.send_message(message.chat.id,
                    "رصيدك السابق: " + old_balance +" SP\nرصيدك الحالي: " + new_balance + " SP", reply_markup = mainKB)


            elif (int(qnt)*int(price)) > int(old_balance):
                cur.execute(select_script, select_value)
                for record in cur.fetchall():
                    balance = str(record['balance'])
                bot.send_message(message.chat.id,
                "عذراً، ليس لديك رصيد كاف لإتمام العملية\n رصيدك الحالي: " + str(balance) + " SP", reply_markup = mainKB)          
        elif message.text == "إلغاء ❌":
            list.clear()
            choose_product_1(message)
        elif message.text == "القائمة الرئيسية":
            list.clear()
            bot.send_message(message.chat.id,
            "أهلاً بك في البوت الخاص بنا \n كيف يمكنني مساعدتك؟", reply_markup = mainKB)
        con.commit()
        cur.close()
        con.close()
#------------------------------------------------
#------------------------------------------------
#---------------------------------------------------  
# # لائحة الأسعار      
    def price_list1(message):
        list_ask = bot.send_message(message.chat.id, "من فضلك اختر القائمة المطلوبة" , reply_markup=price_listKB)
        bot.register_next_step_handler(list_ask, price_list2)
    
    def price_list2(message):
        text = ""
        list_ans = message.text 
        con = psycopg2.connect(  # Start Database Connection

            host = DB_HOST,
            database = DB_NAME,
            user = DB_USERN,
            password = DB_PASS,
            port = 5432
        )
        cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
        if list_ans == "أسعار رصيد البوت":
            select_script =  """SELECT * FROM price_list
                                where
                                product_name = 'Yobit Code' OR
                                product_name = 'Visa Token "لا تدمج"' OR
                                product_name = 'Visa Token "تدمج"' OR
                                product_name = 'Syriatel Cash' OR
                                product_name = 'Payeer' OR
                                product_name = 'MTN Cash'"""
            cur.execute(select_script)
            for record in cur.fetchall():
                product_name = record["product_name"]
                price = str((record['price']))
                text = text + "\n كل 1$ من: " + product_name + "\n يعادل: " + price + " SP\n--------"
        elif list_ans == "أسعار منتجاتنا":
            select_script =  """SELECT * FROM price_list
                                where
                                product_name = 'تحضير حساب حقيقي' OR
                                product_name = 'تحضير حساب حقيقي مع SSN' OR
                                product_name = 'SSN' """
            cur.execute(select_script)
            for record in cur.fetchall():
                product_name = record["product_name"]
                price = str((record['price']))
                text = text + "\n اسم المنتج: " + product_name + "\n السعر: " + price + " SP\n--------"
        bot.send_message(message.chat.id, text, reply_markup=returnToMainKB)    
        #bot.send_message(message.chat.id, list_str, reply_markup=returnToMainKB)
        
        #bot.send_message(message.chat.id, price_list, reply_markup=returnToMainKB)
        con.commit()
        cur.close()
        con.close() # End Database Connection
#------------------------------------------------
#------------------------------------------------
#---------------------------------------------------  
# # معرفة رصيدي      
    def my_balance(message):
        username = "@" + message.from_user.username
        con = psycopg2.connect(  # Start Database Connection

            host = DB_HOST,
            database = DB_NAME,
            user = DB_USERN,
            password = DB_PASS,
            port = 5432
        )
        cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
        select_script =  'SELECT * FROM clients WHERE username = %s'
        select_value = (username,)
        cur.execute(select_script, select_value)
        for record in cur.fetchall():
            balance = str(record['balance'])
        bot.send_message(message.chat.id,
        "رصيدك الحالي: " + balance + " SP")
        con.commit()
        cur.close()
        con.close()
#------------------------------------------------
#------------------------------------------------
#---------------------------------------------------        

    if message.text == "/AdminCP":
        admin_cp1(message)
    elif message.text == "/start":
        start(message)
    elif message.text == "طلب منتج":
        choose_product_1(message)
    elif message.text == "لائحة الأسعار":
        price_list1(message)
    elif message.text == "معرفة رصيدي":
        my_balance(message)
    elif message.text == "شحن رصيدي":
        get_method_step1(message)
    elif message.text == "تواصل معنا":
        bot.send_message(message.chat.id, "يمكنك التواصل معنا على الحساب التالي: ", reply_markup = returnToMainKB)
    elif message.text == "شاركنا رأيك واقتراحاتك":
        bot.send_message(message.chat.id, "اعطينا رأيك بالبوت واقتراحاتك", reply_markup = returnToMainKB)
    elif message.text == "القائمة الرئيسية":
        bot.send_message(message.chat.id, "أهلاً بك في البوت الخاص بنا \n كيف يمكنني مساعدتك؟", reply_markup = mainKB)
    
#----------------------------------------------    





print("Running ...")
run()
