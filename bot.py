import telebot
import const
import commands
import lists
import functions.functions
import functions.handlerFunctions

bot = telebot.TeleBot(const.telegram_api)
functions.functions.get_top_prod(const.top_products)
functions.functions.create_categiries_dic(const.categories)
functions.functions.get_all_products(const.all_products)


@bot.message_handler(commands=["start", "Main"])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/Products', '/TopProducts')
    user_markup.row('/FAQ', '/AboutUs')
    user_markup.row('/Tracking', '/Partners')
    bot.send_message(message.chat.id,
                     'Hi, nice to see you there!' if message.text == '/Start' or "/start" else 'Chose what you like!',
                     reply_markup=user_markup)


@bot.message_handler(commands=["Products", "AllProducts"])
def handler(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    functions.functions.get_commands_products(const.categories, user_markup)
    bot.send_message(message.chat.id, 'There is our products. Chose what you like!', reply_markup=user_markup)


@bot.message_handler(commands=["Category"])
def handler(message):
    try:
        category = message.text.replace('/Category ', '')
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        functions.functions.get_categories_products(const.categories, category, user_markup)
        user_markup.row('/Main', "/Products")
        bot.send_message(message.chat.id, 'There is our products from ' + category + "category. Chose what you like!",
                         reply_markup=user_markup)
    except:
        user_mar = telebot.types.ReplyKeyboardMarkup(True, False)
        user_mar.row('/Products', '/Main')
        bot.send_message(message.chat.id, 'No such category, try again', reply_markup=user_mar)


@bot.message_handler(commands=["FAQ"])
def handle_faq(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    functions.functions.find_responce_two(commands.faq, user_markup)
    user_markup.row('/Main')
    bot.send_message(message.chat.id, 'Chose what you need', reply_markup=user_markup)


@bot.message_handler(commands=["AboutUs"])
def handle_start(message):
    bot.send_message(message.chat.id, const.about_us)


@bot.message_handler(commands=["Product"])
def product_handler(message):
    category = message.text.replace('/Product ', '')
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/Products', '/TopProducts', '/Buy ' + category)
    top_products = functions.functions.get_desk_all(const.all_products, category)
    img = open(top_products[0])
    bot.send_photo(message.chat.id, img)

    return bot.send_message(message.chat.id, top_products[1], reply_markup=user_markup)


@bot.message_handler(commands=["Partners"])
def partners(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    functions.functions.find_responce_one(commands.shops, user_markup)
    user_markup.row('/Main')
    bot.send_message(message.chat.id, 'Chose what you need', reply_markup=user_markup)


@bot.message_handler(commands=["Tracking"])
def partners(message):
    bot.send_message(message.chat.id, 'Set your order id')


@bot.message_handler(commands=["TopProducts"])
def top_products(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    functions.functions.get_commands_for_top(const.top_products, user_markup)
    bot.send_message(message.chat.id, 'There is our products. Chose what you like!', reply_markup=user_markup)


@bot.message_handler(commands=["Buy"])
def partners(message):
    # User part

    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/TopProducts', '/Main')
    bot.send_message(message.chat.id, 'Cool, our manager will call u soon and ask you about delivery and dosage.',
                     reply_markup=user_markup)
    # Order chat part
    Product = message.text.replace('/Buy ', '')
    try:
        desk = functions.functions.get_top_chat(const.top_products, Product, message.chat.username, message.date)
        img = open(desk[1])
        bot.send_photo('-1001275580320', img)
        bot.send_message('-1001275580320', desk[0] + "\n" + desk[2])
        # Main order chat
        main_chat = functions.functions.get_top_main_chat(const.top_products, Product, message.chat.username,
                                                          message.date)
        img = open(desk[1])
        bot.send_photo('-1001342855121', img)
        bot.send_message('-1001342855121', main_chat[0] + "\n" + main_chat[2])
    except:
        desk = functions.functions.get_top_chat(const.all_products, Product, message.chat.username, message.date)
        img = open(desk[1])
        bot.send_photo('-1001275580320', img)
        bot.send_message('-1001275580320', desk[0] + "\n" + desk[2])
        # Main order chat
        main_chat = functions.functions.get_top_main_chat(const.all_products, Product, message.chat.username,
                                                          message.date)
        img = open(desk[1])
        bot.send_photo('-1001342855121', img)
        bot.send_message('-1001342855121', main_chat[0] + "\n" + main_chat[2])


@bot.message_handler(content_types=["text"])
def partners(message):
    try:
        shops = lists.shops.get(message.text)
        if shops != None:
            return bot.send_message(message.chat.id, shops)

        list = lists.faq.get(message.text)
        if list != None:
            return bot.send_message(message.chat.id, list)

        order_status = functions.handlerFunctions.getStatus(message.text)
        if len(message.text) == 7 and message.text.isdigit() or len(message.text) == 14 and message.startswith("mpf_"):
            return bot.send_message(message.chat.id, functions.functions.returnStatus(order_status))

        top_products = functions.functions.get_desk_top(const.top_products, message.text)
        if (top_products != None):
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('/Products', '/TopProducts', '/Buy ' + message.text)
            img = open(top_products[0])
            bot.send_photo(message.chat.id, img)
            return bot.send_message(message.chat.id, top_products[1], reply_markup=user_markup)

    except:
        bot.send_message(message.chat.id, 'And what is this?')


bot.polling(none_stop=True, interval=0)
