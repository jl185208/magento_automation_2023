'''
Author : Joselito G. Libres
Date : 10/24/2023

ChangeLog : 

1/12/2023 - Joselito Libres - Updated and replaced deprecated codes

Test Steps 
--------------
1.) Login to Magento.
2.) Create a product
3.) Sync product
4.) Update a product
5.) Sync product

Expected Output 
---------------
1.) Must sync newly created and updated products.
'''

from core.core import *
from core.variable import *
from core.pages import *

testcycle = []
logfiles = []
zephyr_report = ""
loggings()


@step('article should be in stockitems endpoint')
def step_impl(context):
    step_result.clear()
    conn = http.client.HTTPConnection("51.20.70.106")
    payload = ""
    headers = {
        'User-Agent': "insomnia/2023.5.8",
        'Authorization': "Bearer ha8xyhroq81oxs5lnwcxtr679m4hg4t1"
        }
    conn.request("GET", "/rest/default/V1/stockItems/"+str(send_sku), payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    data_decode = data.decode("utf-8")
    logging.info('Data in /Article  ' + str(data))
    js_data = json.loads(data_decode)
    data_inside = js_data['qty']
    logging.info(js_data)
    logging.info('qty_inside : ' + str(data_inside))
    logging.info('qty_in_magento : ' + str(send_qty))
    logging.info('*************** SKU QTY ' + str(send_qty) + ' found in Endpoint \n \n \n')
    if str(data_inside) == str(send_qty):
            step_result.append('Pass')
    else:
            step_result.append('Fail')


@step('stocks is updated in eventbridge')
def step_impl(context):
    context.step_name = "stocks is updated in eventbridge"
    logging.info('Starting automation for step: ' + str(context.step_name))
    # remove sh file 
    if os.path.exists("updatestocks-events.json"):
        os.remove("updatestocks-events.json")
        logging.info('updatestocks-events.json removed in current directory.')
    else:
        logging.error("The file does not exist")
    # replace file
    f = open("updatestocks-events.json", "w")
    f.write('[\n\
    {\n\
        "Time": ' + str(ID) + ',\n\
        "Source": "StockLevelEvent",\n\
        "Resources": ["string"],\n\
        "DetailType": "StockLevelEvent",\n\
        "Detail": "{ \\"customer_number\\": \\"abc123\\", \\"sku\\": \\"'+str(send_sku)+'\\", \\"warehouse\\": \\"BERGER\\", \\"unit_of_measurement\\": \\"PCE\\", \\"available_quantity\\": 2000, \\"physical_quantity\\": 1.0, \\"reserved_quantity\\": 1.0, \\"inbound_quantity\\": 1.0 }",\n\
        "EventBusName": "integration-events",\n\
        "TraceHeader": "string"\n\
    }\n]')
    logging.info('JSON for Eventbridge file updated')
    f.close()
    os.system('aws events put-events --entries file://updatestocks-events.json > send_events_eventbridge.txt') 
    logging.info('Waiting for eventbridge to process...')
    time.sleep(90)
    logging.info('\n \n')
    pass


@step('stocks should be in skustockitems endpoint')
def step_impl(context):
    import http.client
    conn = http.client.HTTPConnection("51.20.70.106")
    payload = ""
    headers = {
        'User-Agent': "insomnia/2023.5.8",
        'Authorization': "Bearer ha8xyhroq81oxs5lnwcxtr679m4hg4t1"
        }
    conn.request("GET", "/rest/default/V1/stockItems/" + str(send_sku), payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    response = data.decode("utf-8")
    curr_stock_data = json.loads(response)
    curr_stock_inside = curr_stock_data['qty']
    logging.info('Current stock in stockitem endpoint is ' + str(curr_stock_inside))
    if str(curr_stock_inside) == str(2000):
         step_result.append('Pass')
    else :
         logging.error('Step failed, current stock is not 2000')
         step_result.append('Fail')
    

@step('OCS-T1651 should be updated to Zephyr')
def step_impl(context):
    context.step_name = "OCS-T1641 should be updated to Zephyr"
    logging.info('Starting automation for step: ' + str(context.step_name))
    logging.info('Testcycle2: ' + str(testcycle2))
    logging.info('Testcycle: ' + str(testcycle))
    count_pass = step_result.count('Pass')
    logging.info('Step Results : ' + str(step_result))
    testcycle_key = testcycle2[0]
    if count_pass == 3:
        result = 'Pass'
    else:
        result = 'Fail'
    total_time = round(time.time() - start_time)
    total_time2 = 120000
    logging.info(round(total_time))
    feature_file = '<br><br>Scenario: Validate article creation in Magento\
        <br>   When that article is added in magento\
        <br>   Then article should be in ocs - <b>Pass</b>\
        <br>   And article should be in stockitems endpoint - <b>' + str(step_result[0]) + '</b>\
        <br>   And article should be in dynamodb - <b>' + str(step_result[1]) + '</b>\
        <br>   And OCS-T1633 should be updated in Zephyr - <b>Pass</b>\
        <br>   <b>Total step execution:</b> ' + str(total_time) + 's<br>'
    payload_testcase_execution = "{\n  \"projectKey\": \"OCS\",\n  \"testCaseKey\": \"OCS-T1651\",\n  \"testCycleKey\": \"" + str(testcycle2[0])+ "\",\n  \"statusName\": \"" + str(result) + "\",\n  \"testScriptResults\": [\n    {\n      \"statusName\": \"" + str(result) + "\",\n      \"actualEndDate\": \"2023-05-20T13:15:13Z\",\n      \"actualResult\": \"" + str('Stocks Updated <br> <b>SKU:</b> ' + str(send_sku) + '<br> <b>Article Name :</b> ' + str(send_title) + '<br> <b>Qty : 2000 </b> ' + str(feature_file) + '<br>') + "\"\n    }\n  ],\n  \"actualEndDate\": \"2024-05-20T13:15:13Z\",\n  \"executionTime\": "+str(total_time2)+",\n  \"executedById\": \"712020:787b46ed-42ec-4613-90f5-b0fb137785a0\",\n  \"assignedToId\": \"712020:787b46ed-42ec-4613-90f5-b0fb137785a0\",\n  \"comment\": \"SUCCESS\",\n  \"customFields\": {\n\n  }\n\t\n}\n"
    add_exe_testcases(testcycle_key, payload_testcase_execution, result)
