
import os
import telebot
from telebot import types
import psycopg2
import psycopg2.extras
import datetime
from datetime import datetime

BOT_TOKEN = "5147583630:AAFFpgqmZ05LOIAJln1p5vHjiudoRaUbzTQ"
bot = telebot.TeleBot(BOT_TOKEN)


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
otherBTN = types.KeyboardButton("other")
payKB.add(visa_1BTN, visa_2BTN, payeerBTN, yobitBTN, syriatelBTN, mtnBTN, otherBTN, returnToMainBTN)
# ---------------------------------
# Visa Token Mergable - Pay Menu 
visatoken_1KB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
confirm_BTN = types.KeyboardButton("تأكيد")
cancel_BTN = types.KeyboardButton("إلغاء")
visatoken_1KB.add(confirm_BTN, cancel_BTN, returnToMainBTN)
# ---------------------------------
# Visa Token Non Mergable - Pay Menu 
#visatoken_2KB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
#confirm_BTN = types.KeyboardButton("تأكيد")
#visatoken_2KB.add(confirm_BTN, cancel_BTN, returnToMainBTN)
# ---------------------------------
# Yobit Code - Pay Menu 
yobitKB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
confirm_BTN = types.KeyboardButton("تأكيد")
yobitKB.add(confirm_BTN, cancel_BTN, returnToMainBTN)
# ---------------------------------
# Check Code
checkKB = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
yes_BTN = types.KeyboardButton("نعم")
no_BTN = types.KeyboardButton("لا")
checkKB.add(no_BTN, yes_BTN, returnToMainBTN)


# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# Welcome Message & Store user data
@bot.message_handler(commands = ["start"])
def start(message):    
    con = psycopg2.connect(

            host = "localhost",
            database = "db1",
            user = "postgres",
            password = "admin",
            port = 5432
        )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    # Welcome Message
    bot.send_message(message.chat.id, "أهلاً بك في البوت الخاص بنا \n كيف يمكنني مساعدتك؟", reply_markup = mainKB)
#----------------------
    # User Data
    username = "@" + message.from_user.username
    user_id = message.chat.id
#----------------------
    # Start Database Connection
    con = psycopg2.connect(

            host = "localhost",
            database = "db1",
            user = "postgres",
            password = "admin",
            port = 5432
        )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
#-----------------
    # Store user data into Database
    try:
        insert_script = 'INSERT INTO tb1 (tele_id, username, balance) VALUES (%s, %s, %s)'
        insert_values = user_id, username, 0
        cur.execute(insert_script, insert_values)    
    except Exception as error:
        print("error, user maybe already exists")
        pass
#-----------------
    # Commit & End Database Connection
    con.commit()
    cur.close()
    con.close() 
#------------------------------------------------------------------
#------------------------------------------------------------------
# Add Balance To Users By Admin
@bot.message_handler(commands = ["AddBalance"])
# Ask For Username
def add_balance_step1(message):
    username_ask = bot.send_message(message.chat.id,
    "من فضلك قم بإرسال اسم المستخدم الذي تريد إضافة الرصيد له بالشكل التالي:\n@username")
    bot.register_next_step_handler(username_ask, add_balance_step2)
#-------------------
# Ask For Balance
def add_balance_step2(message):
    username_answer = str(message.text)
    con = psycopg2.connect(  # Start Database Connection

            host = "localhost",
            database = "db1",
            user = "postgres",
            password = "admin",
            port = 5432
        )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    select_script =  'SELECT username FROM tb1 WHERE username = %s'
    select_value = (username_answer,)
    cur.execute(select_script, select_value)
    def user_exists(cur):
        return cur.fetchone() is not None
    if user_exists(cur) == True:
        print("User " + username_answer + " Exists")
        balance_ask = bot.send_message(message.chat.id,
        "من فضلك قم بإرسال قيمة الرصيد الذي تريد تحويله")
        bot.register_next_step_handler(balance_ask, add_balance_step3, username_answer)

    else:
        bot.send_message(message.chat.id,
        "المستخدم " + username_answer + " غير موجود، تأكد من الاسم مرة أخرى.")
        add_balance_step1(message)
#-------------------
# Add the requested Balance
def add_balance_step3(message, username_answer):
    con = psycopg2.connect(  # Start Database Connection

            host = "localhost",
            database = "db1",
            user = "postgres",
            password = "admin",
            port = 5432
        )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    #------------------
    # Old Balance
    balance_answer = str(message.text)
    #------------------
    # Getting old balance & tele_id
    select_script =  'SELECT * FROM tb1 WHERE username = %s'
    select_value = (username_answer,)
    cur.execute(select_script, select_value)
    for record in cur.fetchall():
        tele_id = record['tele_id']
        old_balance = str(record['balance'])
        username = record['username']
    #------------------
    # Updating The Balance
    update_script = 'UPDATE tb1 SET balance = balance + %s WHERE username = %s'
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
    "تمت إضافة " + balance_answer + " SP إلى رصيد " + username + " بنجاح !" +
    "\n الرصيد السابق: " + old_balance +
    "\n الرصيد الحالي: " + new_balance)
    bot.send_message(tele_id, # For Client
    "تمت إضافة " + balance_answer + " SP إلى رصيدك بنجاح !" +
    "\nرصيدك السابق: " + old_balance +
    "\nرصيدك الحالي: " + new_balance)
    con.commit()
    cur.close()
    con.close() # End Database Connection    
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
# Reduce Balance To Users By Admin
@bot.message_handler(commands = ["ReduceBalance"])
# Ask For Username
def reduce_balance_step1(message):
    username_ask = bot.send_message(message.chat.id,
    "من فضلك قم بإرسال اسم المستخدم الذي تريد إنقاص الرصيد له بالشكل التالي:\n@username")
    bot.register_next_step_handler(username_ask, reduce_balance_step2)
#-------------------
# Ask For Balance
def reduce_balance_step2(message):
    username_answer = message.text
    con = psycopg2.connect(  # Start Database Connection

            host = "localhost",
            database = "db1",
            user = "postgres",
            password = "admin",
            port = 5432
        )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    select_script =  'SELECT username FROM tb1 WHERE username = %s'
    select_value = (username_answer,)
    cur.execute(select_script, select_value)
    def user_exists(cur):
        return cur.fetchone() is not None
    if user_exists(cur) == True:
        print("User " + username_answer + " Exists")
        balance_ask = bot.send_message(message.chat.id,
        "من فضلك قم بإرسال قيمة الرصيد الذي تريد إنقاصه")
        bot.register_next_step_handler(balance_ask, reduce_balance_step3, username_answer)
    else:
        bot.send_message(message.chat.id,
        "المستخدم " + username_answer + " غير موجود، تأكد من الاسم مرة أخرى.")
        reduce_balance_step1(message)    
#-------------------
# Reduce the requested Balance
def reduce_balance_step3(message, username_answer):
    con = psycopg2.connect(  # Start Database Connection

            host = "localhost",
            database = "db1",
            user = "postgres",
            password = "admin",
            port = 5432
        )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    #------------------
    # Old Balance
    balance_answer = message.text
    #------------------
    # Getting old balance & tele_id
    select_script =  'SELECT * FROM tb1 WHERE username = %s'
    select_value = (username_answer,)
    cur.execute(select_script, select_value)
    for record in cur.fetchall():
        tele_id = record['tele_id']
        old_balance = str(record['balance'])
        username = record['username']
    if old_balance > balance_answer:
        #------------------------
        # Updating The Balance
        update_script = 'UPDATE tb1 SET balance = balance - %s WHERE username = %s'
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
        "تم إنقاص " + balance_answer + " SP من رصيد " + username + " بنجاح" +
        "\n الرصيد السابق: " + old_balance +
        "\n الرصيد الحالي: " + new_balance)
        bot.send_message(tele_id, # For Client
        "تم إنقاص " + balance_answer + " SP من رصيدك" +
        "\nرصيدك السابق: " + old_balance +
        "\nرصيدك الحالي: " + new_balance)
    else: bot.send_message(message.chat.id,
    "خطأ، لا يمكن أن يكون الرصيد المراد إنقاصه أكبر من الرصيد الحالي.\n الرصيد الحالي: " + old_balance + "\n حاول مرة أخرى")
    #reduce_balance_step2(message)
    
    
    con.commit()
    cur.close()
    con.close() # End Database Connection
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# Get Client Balance By Admin
@bot.message_handler(commands = ["GetBalance"])
def get_balance_step1(message):
    username_ask = bot.send_message(message.chat.id,
    "من فضلك قم بإرسال اسم المستخدم الذي تريد الاستفسار عن رصيده بالشكل التالي:\n@username")
    bot.register_next_step_handler(username_ask, get_balance_step2)
#-------------------
def get_balance_step2(message):
    username_answer = message.text
    con = psycopg2.connect(  # Start Database Connection

        host = "localhost",
        database = "db1",
        user = "postgres",
        password = "admin",
        port = 5432
    )
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    select_script =  'SELECT * FROM tb1 WHERE username = %s'
    select_value = (username_answer,)
    cur.execute(select_script, select_value)
    for record in cur.fetchall():
        user_ID = str(record['id'])
        balance = str(record['balance'])
        username = str(record['username'])
    bot.send_message(message.chat.id,
    "ID: " + user_ID + "\n اسم المستخدم: " + username + "\n الرصيد الحالي: " + balance + " SP")
    con.commit()
    cur.close()
    con.close()
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------



@bot.message_handler(commands = ["test"])
def test(message):
    old_document = "SSNs/fresh/ssn_4.txt"
    new_document = "SSNs/sold/ssn_sold.txt"
    os.rename(old_document, new_document)












#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
# Handling ReplyKeyboard Messages
@bot.message_handler(content_types=['text'])
def rep_MainKB(message):
    list = []
    def get_method_step1(message):
        method_ask = bot.send_message(message.chat.id, "اختر وسيلة الدفع المناسبة لك", reply_markup= payKB)
        bot.register_next_step_handler(method_ask, get_method_step2)
    #---------------------------
    def get_method_step2(message):
        method_ans = message.text
        if method_ans == "Yobit Code":
            get_codes_1(message)
           #---------------------------
        elif message.text == "Visa Token \"تدمج\"":
            get_codes_1(message)
        #---------------------------
        #---------------------------
        elif message.text == "Visa Token \"لا تدمج\"":
            get_codes_1(message)
    #---------------------------
    
    def get_yobitcode_1(message):
            yobit_price = 4000
            price = yobit_price
            code_ask = bot.send_message(message.chat.id,
            "كل 1$ يعادل " + str(price) + " SP\n"
            "نستقبل الأكواد من عملة USD فقط\n" + 
            "يرجى إرسال كل كود برسالة منفصلة بالشكل التالي:\n" + 
            "YOBITFR6LC8X3Q764YQGR4FY6NQVXKBTJQGRMUSD\n" + 
            "بعد الانتهاء من إرسال الأكواد يرجى الضغط على زر \"تأكيد\"\n" + 
            "ملاحظة: بعد الضغط على زر تأكيد لا يمكن التراجع عن هذه الخطوة!", reply_markup = yobitKB)
            bot.register_next_step_handler(code_ask, get_yobitcode_2, price)
    #---------------------------
    def get_yobitcode_2(message, price):
                username = ("@" + message.from_user.username)
                #---------------------
                if ((message.text != "تأكيد") & (message.text != "إلغاء")
                & (message.text != "القائمة الرئيسية") & (message.text != "/start")
                & (message.text != "Yobit Code")):
                    msg_dt = datetime.now().strftime("%A %d-%b-%Y %H:%M:%S")
                    list.append((username, message.text, "YobitCode" , "yes", msg_dt, "pending", price))
                    code_ask_2 = bot.send_message(message.chat.id,
                    text = """تم استقبال البطاقة الخاص بك، يمكنك إرسال بطاقة أخرى
                    أو الضغط على زر "تأكيد" لتاكيد العملية.\n
                    اضغط زر "إلغاء" لإلغاء العملية.""")
                    bot.register_next_step_handler(code_ask_2, get_yobitcode_2, price)
                elif message.text == "تأكيد":
                    check_ask = bot.send_message(message.chat.id,
                    """***هذه الخطوة لا يمكن التراجع عنها***\n
                    هل تريد بالتأكيد إرسال البطاقات السابقة جميعها؟ """, reply_markup = checkKB)
                    bot.register_next_step_handler(check_ask, get_yobitcode_3)
                elif message.text == "إلغاء":
                    list.clear()
                    # UnSuccess Message
                    bot.send_message(message.chat.id, text = "تم إلغاء العملية.", reply_markup=mainKB)
    #---------------------------
    def get_yobitcode_3(message):
        if message.text == "نعم":
            print("yes", list)
            con = psycopg2.connect(  # Start Database Connection

            host = "localhost",
            database = "db1",
            user = "postgres",
            password = "admin",
            port = 5432
            )
            cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
            for d in list:
                script_insert = "INSERT into payments (source, code, type, exists, receive_dt, status, price) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                script_value = d
                cur.execute(script_insert, script_value)
            con.commit()
            #-----------------------
            # Success Message
            bot.send_message(message.chat.id, text =
            """تم استقبال جميع البطاقات بنجاح !\n
            مدة معالجة الطلب 24 ساعة من تاريخ إرسال الكود.""", reply_markup = mainKB)
            #-----------------------
            cur.close()
            con.close() # End Database Connection
        elif message.text == "لا":
            list.clear()
            # UnSuccess Message
            bot.send_message(message.chat.id, text = "تم إلغاء العملية.", reply_markup=mainKB)
#------------------------------------------------
#------------------------------------------------
#------------------------------------------------
    def get_visacard_1(message):
            visam_price = 3700
            visanonm_price = 3200
            method_ans = message.text
            if method_ans == "Visa Token \"تدمج\"":
                price = visam_price
                type = "Visa_M"
            elif method_ans == "Visa Token \"لا تدمج\"":
                price = visanonm_price
                type = "Visa_NonM"
            code_ask = bot.send_message(message.chat.id,)
            bot.register_next_step_handler(code_ask, get_visacard_2, price, type)
    #---------------------------
    def get_visacard_2(message, price, type):
                username = ("@" + message.from_user.username)
                #---------------------
                if ((message.text != "تأكيد") & (message.text != "إلغاء")
                & (message.text != "القائمة الرئيسية") & (message.text != "/start")
                & (message.text != "Visa Token \"تدمج\"")):
                    msg_dt = datetime.now().strftime("%A %d-%b-%Y %H:%M:%S")
                    list.append((username, message.text, type , "yes", msg_dt, "pending", price))
                    code_ask_2 = bot.send_message(message.chat.id,
                    text = """تم استقبال الكود الخاص بك، يمكنك إرسال كود آخر،
                    أو الضغط على زر "تأكيد" لتاكيد العملية.\n
                    اضغط زر "إلغاء" لإلغاء العملية.""")
                    bot.register_next_step_handler(code_ask_2, get_visacard_2, price, type)
                elif message.text == "تأكيد":
                    check_ask = bot.send_message(message.chat.id,
                    """***هذه الخطوة لا يمكن التراجع عنها***\n
                    هل تريد بالتأكيد إرسال البطاقات السابقة جميعها؟ """, reply_markup = checkKB)
                    bot.register_next_step_handler(check_ask, get_visacard_3)
                elif message.text == "إلغاء":
                    list.clear()
                    # UnSuccess Message
                    bot.send_message(message.chat.id, text = "تم إلغاء العملية.", reply_markup=mainKB)
    #---------------------------
    def get_visacard_3(message):
        if message.text == "نعم":
            print("yes", list)
            con = psycopg2.connect(  # Start Database Connection

            host = "localhost",
            database = "db1",
            user = "postgres",
            password = "admin",
            port = 5432
            )
            cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
            for d in list:
                script_insert = "INSERT into payments (source, code, type, exists, receive_dt, status, price) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                script_value = d
                cur.execute(script_insert, script_value)
            con.commit()
            #-----------------------
            # Success Message
            bot.send_message(message.chat.id, text =
            """تم استقبال جميع البطاقات بنجاح !\n
            مدة معالجة الطلب 24 ساعة من تاريخ إرسال البطاقة.""", reply_markup = mainKB)
            #-----------------------
            cur.close()
            con.close() # End Database Connection
        elif message.text == "لا":
            list.clear()
            # UnSuccess Message
            bot.send_message(message.chat.id, text = "تم إلغاء العملية.", reply_markup=mainKB)
#------------------------------------------------
#------------------------------------------------
#------------------------------------------------
    def get_codes_1(message):
            yobit_price = 4000
            visam_price = 3500
            visanonm_price = 3000
            method_ans = message.text
            if method_ans == "Yobit Code":
                price = yobit_price
                type = "YobitCode"
                ask_text = "كل 1$ يعادل " + str(price) + """ SP\nنستقبل الأكواد من عملة USD فقط\n
                يرجى إرسال كل كود برسالة منفصلة بالشكل التالي:\n
                YOBITFR6LC8X3Q764YQGR4FY6NQVXKBTJQGRMUSD\n
                بعد الانتهاء من إرسال الأكواد يرجى الضغط على زر \"تأكيد\"\n
                ملاحظة: بعد الضغط على زر تأكيد لا يمكن التراجع عن هذه الخطوة!"""
                markup = yobitKB
            elif method_ans == "Visa Token \"تدمج\"":
                price = visam_price
                type = "Visa_M"
                ask_text = "كل 1$ يعادل " + str(price) + """ SP\n
                يرجى إرسال كل بطاقة برسالة منفصلة بالشكل التالي:\n
                XXXX-XXXXXX-XXXX\n
                بعد الانتهاء من إرسال بطاقات يرجى الضغط على زر \"تأكيد\"\n
                ملاحظة: بعد الضغط على زر تأكيد لا يمكن التراجع عن هذه الخطوة!"""
                markup = visatoken_1KB
            elif method_ans == "Visa Token \"لا تدمج\"":
                price = visanonm_price
                type = "Visa_NonM"
                ask_text = "كل 1$ يعادل " + str(price) + """ SP\n
                يرجى إرسال كل بطاقة برسالة منفصلة بالشكل التالي:\n
                XXXX-XXXXXX-XXXX\n
                بعد الانتهاء من إرسال بطاقات يرجى الضغط على زر \"تأكيد\"\n
                ملاحظة: بعد الضغط على زر تأكيد لا يمكن التراجع عن هذه الخطوة!"""
                markup = visatoken_1KB
            code_ask = bot.send_message(message.chat.id, ask_text, reply_markup = markup)
            bot.register_next_step_handler(code_ask, get_codes_2, price, type)
    #---------------------------
    def get_codes_2(message, price, type):
                username = ("@" + message.from_user.username)
                #---------------------
                if ((message.text != "تأكيد") & (message.text != "إلغاء")
                & (message.text != "القائمة الرئيسية") & (message.text != "/start")
                & (message.text != "Visa Token \"تدمج\"")):
                    msg_dt = datetime.now().strftime("%A %d-%b-%Y %H:%M:%S")
                    list.append((username, message.text, type , "yes", msg_dt, "pending", price))
                    code_ask_2 = bot.send_message(message.chat.id,
                    text = """تم استقبال الكود الخاص بك، يمكنك إرسال كود آخر،
                    أو الضغط على زر "تأكيد" لتاكيد العملية.\n
                    اضغط زر "إلغاء" لإلغاء العملية.""")
                    bot.register_next_step_handler(code_ask_2, get_codes_2, price, type)
                elif message.text == "تأكيد":
                    check_ask = bot.send_message(message.chat.id,
                    """***هذه الخطوة لا يمكن التراجع عنها***\n
                    هل تريد بالتأكيد إرسال البطاقات السابقة جميعها؟ """, reply_markup = checkKB)
                    bot.register_next_step_handler(check_ask, get_codes_3)
                elif message.text == "إلغاء":
                    list.clear()
                    # UnSuccess Message
                    bot.send_message(message.chat.id, text = "تم إلغاء العملية.", reply_markup=mainKB)
    #---------------------------
    def get_codes_3(message):
        if message.text == "نعم":
            print("yes", list)
            con = psycopg2.connect(  # Start Database Connection

            host = "localhost",
            database = "db1",
            user = "postgres",
            password = "admin",
            port = 5432
            )
            cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
            for d in list:
                script_insert = "INSERT into payments (source, code, type, exists, receive_dt, status, price) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                script_value = d
                cur.execute(script_insert, script_value)
            con.commit()
            #-----------------------
            # Success Message
            bot.send_message(message.chat.id, text =
            """تم استقبال جميع البطاقات بنجاح !\n
            مدة معالجة الطلب 24 ساعة من تاريخ إرسال البطاقة.""", reply_markup = mainKB)
            #-----------------------
            cur.close()
            con.close() # End Database Connection
        elif message.text == "لا":
            list.clear()
            # UnSuccess Message
            bot.send_message(message.chat.id, text = "تم إلغاء العملية.", reply_markup=mainKB)
#------------------------------------------------
#------------------------------------------------
#------------------------------------------------
    
        
     
#---------------------------------------------------        
    if message.text == "طلب منتج":
        bot.send_message(message.chat.id, "اختر الخدمة أو المنتج الذي تريده", reply_markup = requestKB)
    elif message.text == "لائحة الأسعار":
        bot.send_message(message.chat.id, "لائحة الأسعار", reply_markup = pricesKB)
    elif message.text == "معرفة رصيدي":
        bot.send_message(message.chat.id, "رصيدك الحالي: 0", reply_markup = balanceKB)
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
bot.infinity_polling()
