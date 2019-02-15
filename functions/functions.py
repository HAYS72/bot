import sqlite3
from bs4 import BeautifulSoup
import time
from pprint import pprint


# find responce on command
def find_responce_one(arr, key, main=False):
    i = 0
    while i < len(arr):
        key.row(arr[i])
        i += 1


# the same, but commands will be it 2 lines
def find_responce_two(arr, key):
    i = 0
    while i < len(arr):
        key.row(arr[i], arr[i + 1])
        i += 2


# respoce on getStatus command
def returnStatus(status):
    if (status == 'no_order'):
        return 'Sorry, no such order.'
    else:
        return 'Your status: ' + status.get("status")


# create dict with top products
def get_top_prod(var):
    connection = sqlite3.connect('database.sqlite')
    c = connection.cursor()
    c.execute("select name, min_price, description, product_id from products where status_id = 2 and locale = 'en'")
    query_products = c.fetchall()
    c.close()
    i = 0
    while i < len(query_products):
        var.update({query_products[i][0]: {"Price": query_products[i][1], "Desk": query_products[i][2],
                                           "Id": query_products[i][3]}})
        i += 1
    return var


def get_all_products(var):
    connection = sqlite3.connect('database.sqlite')
    c = connection.cursor()
    c.execute("select name, min_price, description, product_id from products where  locale = 'en'")
    query_products = c.fetchall()
    c.close()
    i = 0
    while i < len(query_products):
        var.update({query_products[i][0]: {"Price": query_products[i][1], "Desk": query_products[i][2],
                                           "Id": query_products[i][3]}})
        i += 1
    return var


def create_categiries_dic(var):
    connection = sqlite3.connect('database.sqlite')
    c = connection.cursor()
    c.execute("""
    select categories.name  as category, products.name
    from products
       join categories on (products.category_id = categories.category_id)
    where products.locale = 'en'
       and categories.locale = 'en'
    """)
    query_products = c.fetchall()
    c.close()
    i = 0
    while i < len(query_products):
        if var.get(query_products[i][0]) == None:
            var.update({query_products[i][0]: [query_products[i][1]]})
        else:
            var[query_products[i][0]].append(query_products[i][1])
        i += 1
    return var


# responce on command TopProducts
def get_commands_for_top(dic, key):
    i = 0
    while i < len(dic.keys()):
        key.row(dic.keys()[i], dic.keys()[i + 1])
        i += 2
    key.row("/Main")


def get_commands_products(dic, key):
    i = 0
    while i < len(dic.keys()) - 1:
        key.row("/Category " + dic.keys()[i], "/Category " + dic.keys()[i + 1])
        i += 2
    key.row("/Category " + dic.keys()[i], "/Main")


def get_categories_products(dic, key, keyboard):
    i = 0
    while i < len(dic.get(key)):
        keyboard.row("/Product " + dic.get(key)[i])
        i += 1


def get_desk_top(arr, key):
    try:
        text = BeautifulSoup(arr.get(key).get("Desk")).text
        return ["products/" + str(arr.get(key).get("Id")) + '.jpg', "Name: " + key +
                "\nMin price in euro: " + str(arr.get(key).get("Price")) +
                "\nDescription: \n" + text]
    except:
        return False

    # send order to orderChat


def get_top_chat(arr, key, username, date):
    try:
        text = BeautifulSoup(arr.get(key).get("Desk")).text
        return ["Hi, new order from user @" + username,
                "products/" + str(arr.get(key).get("Id")) + '.jpg',
                "Date: " + time.ctime(date) +
                "\nName: " + key +
                "\nMin price in euro: " + str(arr.get(key).get("Price")) +
                "\nDescription:\n" + text]
    except:
        return False

    # send order to main prder tracking chat


def get_top_main_chat(arr, key, username, date):
    try:
        text = BeautifulSoup(arr.get(key).get("Desk")).text
        return ["Hi, new order from telegram shop. \nUser: @" + username,
                "\nproducts/" + str(arr.get(key).get("Id")) + '.jpg',
                "Date: " + time.ctime(date) +
                "\nName: " + key +
                "\nMin price in euro: " + str(arr.get(key).get("Price")) +
                "\nDescription: \n" + text]
    except:
        return False


def get_desk_all(arr, key):
    try:
        text = BeautifulSoup(arr.get(key).get("Desk")).text
        return ["products/" + str(arr.get(key).get("Id")) + '.jpg', "Name: " + key +
                "\nMin price in euro: " + str(arr.get(key).get("Price")) +
                "\nDescription: \n" + text]
    except:
        return False