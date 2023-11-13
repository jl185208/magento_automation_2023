from behave import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from zipfile import ZipFile
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import logging
import requests
import http.client
import json
import os
import subprocess

start_time = time.time()
PREVIOUS_QTY = []
PREVIOUS_SKU = []
LATEST_SKU = []
LATEST_QTY = []

# OCS
TOKEN_URL = 'https://u3q285bjnj.execute-api.eu-north-1.amazonaws.com/dev/auth/token'
CLIENT_ID = '1dcsna8jq4pbi9otc16b6sgpq'
CLIENT_SECRET = '9hkqk3c2utpua7patjber5a370ob6buo788n1q7oce2idgj7rcn'
ID = str(int(time.time()))
get_log_file = []

def loggings():
    #today = date.today()
    ''''timestamp'''
    ID = str(int(time.time()))
    file_name_output = 'bdd-actual- ' + ID + '.txt'
    get_log_file.clear()
    get_log_file.append(file_name_output)
    logging.basicConfig(filename=file_name_output, filemode='a', format='%(asctime)s - [%(levelname)s] - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    #logging.basicConfig(filename='bdd-' + ID + '.log')
    logging.info('Starting Automation')  
    logging.info('Current time stamp : ' + ID)  


def check_article_ocs(sku):
    try: 
        def get_access_token(url, client_id, client_secret):
            response = requests.post(
                url,
                data={"grant_type": "client_credentials"},
                auth=(client_id, client_secret),
            )
            #print(response.json()["access_token"])
            return response.json()["access_token"]
        logging.info('Looking for SKUs : ' + str(sku))
        conn = http.client.HTTPSConnection("u3q285bjnj.execute-api.eu-north-1.amazonaws.com")
        payload = ""
        headers = { 'Authorization': "Bearer " + get_access_token(TOKEN_URL, CLIENT_ID, CLIENT_SECRET) }
        conn.request("GET", "/dev/master-data/article/" + str(sku), payload, headers)
        res = conn.getresponse()
        data = res.read()
        logging.info('Data in /Article  ' + str(data))
        data_decode = data.decode("utf-8")
        js_data = json.loads(data_decode)
        data_inside = js_data['article_master']
        print(data_inside)
        logging.info('Data Inside: ' + str(data_inside))
        logging.info('SKU in OCS : ' + data_inside['article_number'])
        logging.info('*************** SKU ' + str(sku) + ' is found in OCS \n \n \n')
        if str(data_inside['article_number']) == str(sku):
            return 'Pass'
        else:
            return 'Fail'
    except Exception as e:
        logging.error("SKU not found in OCS", exc_info=True)
        assert False

def check_article_dynamodb():
    os.system('sh sh/dynamodb.sh') 
    pass

def check_so_dynamodb():
    pass

def check_aricle_endpoint(qty, sku):
    conn = http.client.HTTPConnection("51.20.70.106")
    payload = ""
    headers = {
        'User-Agent': "insomnia/2023.5.8",
        'Authorization': "Bearer ha8xyhroq81oxs5lnwcxtr679m4hg4t1"
        }
    conn.request("GET", "/rest/default/V1/stockItems/" + str(sku), payload, headers)
    res = conn.getresponse()
    data = res.read()
    data_decode = data.decode("utf-8")
    logging.info('Data in /Article  ' + str(data))
    js_data = json.loads(data_decode)
    data_inside = js_data['qty']
    logging.info(js_data)
    logging.info('qty_inside : ' + str(data_inside))
    logging.info('qty_in_magento : ' + str(qty))
    logging.info('*************** SKU QTY ' + str(qty) + ' found in Endpoint \n \n \n')
    if str(data_inside) == str(qty):
            logging.info('Step Passed')
            return 'Pass'
    else:
            logging.info('Step Failed')
            return 'Fail'



def create_testcycle_func_test(payloads):
    conn = http.client.HTTPSConnection("api.zephyrscale.smartbear.com")
    payload = payloads
    headers = {
    'Content-Type': "application/json",
    'Authorization': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjb250ZXh0Ijp7ImJhc2VVcmwiOiJodHRwczovL3Bvc3Rlbm5vcmdlYXMuYXRsYXNzaWFuLm5ldCIsInVzZXIiOnsiYWNjb3VudElkIjoiNzEyMDIwOjc4N2I0NmVkLTQyZWMtNDYxMy05MGY1LWIwZmIxMzc3ODVhMCJ9fSwiaXNzIjoiY29tLmthbm9haC50ZXN0LW1hbmFnZXIiLCJzdWIiOiI1MzQ0YjRjOC1mNTljLTM5MmEtYjA0NC0yMzM0MTA4MjcwYjciLCJleHAiOjE3Mjk3Nzc2NzcsImlhdCI6MTY5ODI0MTY3N30.nmFxOhiai4HY98hA-vr5F3cBN02FuC4WlAj1Gnuboh0"
    }
    conn.request("POST", "/v2/testcycles", payload, headers)
    res = conn.getresponse()
    data = res.read()
    response = data.decode("utf-8")
    testcycle_key_data = json.loads(response)
    testcycle_key_inside = testcycle_key_data['key']
    logging.info('Testcycle # : ' + str(testcycle_key_inside))
    return testcycle_key_inside

def add_exe_testcases(key, payloads, result):
    conn = http.client.HTTPSConnection("api.zephyrscale.smartbear.com")
    payload = payloads
    headers = {
            'Content-Type': "application/json",
            'Authorization': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjb250ZXh0Ijp7ImJhc2VVcmwiOiJodHRwczovL3Bvc3Rlbm5vcmdlYXMuYXRsYXNzaWFuLm5ldCIsInVzZXIiOnsiYWNjb3VudElkIjoiNzEyMDIwOjc4N2I0NmVkLTQyZWMtNDYxMy05MGY1LWIwZmIxMzc3ODVhMCJ9fSwiaXNzIjoiY29tLmthbm9haC50ZXN0LW1hbmFnZXIiLCJzdWIiOiI1MzQ0YjRjOC1mNTljLTM5MmEtYjA0NC0yMzM0MTA4MjcwYjciLCJleHAiOjE3Mjk3Nzc2NzcsImlhdCI6MTY5ODI0MTY3N30.nmFxOhiai4HY98hA-vr5F3cBN02FuC4WlAj1Gnuboh0"}
    conn.request("POST", "/v2/testexecutions", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

def get_previous_ocs_qty(sku):
    PREVIOUS_SKU.clear()
    PREVIOUS_QTY.clear()
    def get_access_token(url, client_id, client_secret):
        response = requests.post(
            url,
            data={"grant_type": "client_credentials"},
            auth=(client_id, client_secret),
        )
        #print(response.json()["access_token"])
        return response.json()["access_token"]

    conn = http.client.HTTPSConnection("u3q285bjnj.execute-api.eu-north-1.amazonaws.com")
    payload = ""
    headers = { 'Authorization': "Bearer " + get_access_token(TOKEN_URL, CLIENT_ID, CLIENT_SECRET) }
    conn.request("GET", "/dev/article?sku=" + str(sku), payload, headers)
    res = conn.getresponse()
    data = res.read()
    logging.info('Data in /Article  ' + str(data))
    data_decode = data.decode("utf-8")
    js_data = json.loads(data_decode)
    data_inside = js_data['data'][0]
    print(data_inside)
    print(data_inside['available_quantity'])
    PREVIOUS_SKU.append(data_inside['sku'])
    PREVIOUS_QTY.append(data_inside['available_quantity'])
    logging.info('Previous quantity for ' + str(PREVIOUS_SKU) + ' is ' + str(PREVIOUS_QTY))

def get_latest_ocs_qty(sku):
    LATEST_SKU.clear()
    LATEST_QTY.clear()
    def get_access_token(url, client_id, client_secret):
        response = requests.post(
            url,
            data={"grant_type": "client_credentials"},
            auth=(client_id, client_secret),
        )
        #print(response.json()["access_token"])
        return response.json()["access_token"]
    conn = http.client.HTTPSConnection("u3q285bjnj.execute-api.eu-north-1.amazonaws.com")
    payload = ""
    headers = { 'Authorization': "Bearer " + get_access_token(TOKEN_URL, CLIENT_ID, CLIENT_SECRET) }
    conn.request("GET", "/dev/article?sku=" + str(sku), payload, headers)
    res = conn.getresponse()
    data = res.read()
    logging.info('Data in /Article  ' + str(data))
    data_decode = data.decode("utf-8")
    js_data = json.loads(data_decode)
    data_inside = js_data['data'][0]
    print(data_inside)
    print(data_inside['available_quantity'])
    LATEST_SKU.append(data_inside['sku'])
    LATEST_QTY.append(data_inside['available_quantity'])
    logging.info('Latest quantity for ' + str(LATEST_SKU) + ' is ' + str(LATEST_QTY))
    

def check_so_endpoint(son):
    conn = http.client.HTTPConnection("51.20.70.106")
    payload = ""
    headers = {
        'User-Agent': "insomnia/2023.5.8",
        'Authorization': "Bearer ha8xyhroq81oxs5lnwcxtr679m4hg4t1"
        }
    conn.request("GET", "/rest/default/V1/orders?searchCriteria%5Bfilter_groups%5D%5B0%5D%5Bfilters%5D%5B0%5D%5Bfield%5D=status&searchCriteria%5Bfilter_groups%5D%5B0%5D%5Bfilters%5D%5B0%5D%5Bvalue%5D=pending&searchCriteria%5BsortOrders%5D%5B0%5D%5Bfield%5D=increment_id&fields=items%5Bincrement_id%2Centity_id%5D", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    data_decode = data.decode("utf-8")
    js_data = json.loads(data_decode)
    data_inside = js_data['items'][0]
    logging.info('Data inside order endpoint \n' + str(data_inside) )
    logging.info('Latest sales order entity number is : ' + str(data_inside['entity_id']))
    if str(son) == data_inside['increment_id']:
        logging.info('Order number '+ son +' is found in order endpoint.')
        return data_inside['entity_id']
    else:
        logging.error('Order number '+ son +' is NOT found in order endpoint.')

def check_so_status(order_ent):
    conn = http.client.HTTPConnection("51.20.70.106")
    payload = ""
    headers = {
        'User-Agent': "insomnia/2023.5.8",
        'Authorization': "Bearer ha8xyhroq81oxs5lnwcxtr679m4hg4t1"
        }
    conn.request("GET", "/rest/default/V1/orders/" + str(order_ent), payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    data_decode = data.decode("utf-8")
    logging.info('Data inside /rest/default/V1/orders/ : ' + str(data_decode))
    js_data = json.loads(data_decode)
    data_inside = js_data['status']
    logging.info('Orders endpoint status is : ' + str(data_inside))
    return data_inside