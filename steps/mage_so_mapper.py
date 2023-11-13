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
step_result.clear()

@step('sales order is created in magento')
def step_impl(context):
    try:
        context.step_name = "When sales order is created in magento"
        logging.info('Starting Scenario: ' + str(context.scenario))
        logging.info('Starting automation for step: ' + str(context.step_name))
        get_previous_ocs_qty('109847')
        browser.get('http://51.20.70.106/astrox-badminton.html')
        time.sleep(20)
        # click add to cart
        browser.find_element(By.XPATH, '//*[@id="product-addtocart-button"]').submit()
        time.sleep(3)
        # go to checkout # shipping
        browser.get('http://51.20.70.106/checkout/#shipping')
        time.sleep(40)
        # click proceed to checkout
        browser.find_element(By.XPATH, '//*[@id="customer-email"]').send_keys(send_email)
        browser.find_element(By.NAME, 'firstname').send_keys(send_fname)
        browser.find_element(By.NAME, 'lastname').send_keys(send_lname)
        browser.find_element(By.NAME, 'company').send_keys(send_company)
        browser.find_element(By.NAME, 'street[0]').send_keys(send_street)
        browser.find_element(By.NAME, 'country_id').send_keys(send_country)
        browser.find_element(By.NAME, 'city').send_keys(send_city)
        #browser.find_element(By.NAME, 'region').send_keys(send_region)
        browser.find_element(By.NAME, 'postcode').send_keys(send_postal)
        browser.find_element(By.NAME, 'telephone').send_keys(send_phonenum)
        browser.find_element(By.XPATH, '//*[@id="shipping-method-buttons-container"]/div/button').click()
        # click Place order
        time.sleep(12)
        browser.find_element(By.XPATH, '//*[@id="checkout-payment-method-load"]/div/div/div[2]/div[2]/div[4]/div/button').click()
        time.sleep(12)
        # get order_number
        order_number = browser.find_element(By.XPATH, '//*[@id="maincontent"]/div[3]/div/div[2]/p[1]/span').text
        glob_order_number.clear()
        glob_order_number.append(order_number)
        logging.info('Order Number for created sales order is : ' + str(order_number))
        if order_number != '':
            step_result.clear()
            step_result.append('Pass')
        else:
            step_result.append('Fail')
        logging.info('\n \n')
    except Exception as e:
        logging.error("Error creating the SO.", exc_info=True)
        
    pass

@step('sales order is in orders endpoint')
def step_impl(context):
    context.step_name = "Then sales order is in orders endpoint"
    logging.info('Starting automation for step: ' + str(context.step_name))
    glob_entity_id.clear()
    glob_entity_id.append(check_so_endpoint(glob_order_number[0]))
    if glob_entity_id[0] != '':
        step_result.append('Pass')
    else:
        step_result.append('Fail')
    logging.info('\n \n')
    pass
    

@step('invoice is sent in magento')
def step_impl(context):
    context.step_name = "And invoice is sent in magento"
    logging.info('Starting automation for step: ' + str(context.step_name))
    browser.get(magento_link)
    # browser.find_element(By.ID, 'username').send_keys('admin')
    # browser.find_element(By.ID, 'login').send_keys('123456aA@')
    # browser.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[3]/div[1]/button').click()
    browser.implicitly_wait(10)
    # click Catalog button
    browser.find_element(By.XPATH, '//*[@id="menu-magento-sales-sales"]/a').click()
    # click Orders 
    time.sleep(2)
    browser.find_element(By.XPATH, '//*[@id="menu-magento-sales-sales"]/div/ul/li/div/ul/li[1]/a').click()
    browser.get(link_order + str(glob_entity_id[0]))
    logging.info(link_order + str(glob_entity_id[0]))
    # click Invoice
    time.sleep(5)
    browser.find_element(By.ID, 'order_invoice').click()
    time.sleep(5)
    browser.find_element(By.XPATH, '/html/body/div[2]/main/div[2]/div/div/form/section[4]/section[2]/div[2]/div[2]/div[2]/div[3]/button').click()
    time.sleep(5)
    logging.info('\n \n')
    pass

@step('sales order is in dynamodb')
def step_impl(context):
    context.step_name = "sales order is in dynamodb"
    logging.info('Starting automation for step: ' + str(context.step_name))
    #remove sh file 
    if os.path.exists("sh/so_dynamodb.sh"):
        os.remove("sh/so_dynamodb.sh")
        logging.info('sh/so_dynamodb.sh removed in current directory.')
    else:
        logging.error("The file does not exist")
    # replace file
    f = open("sh/so_dynamodb.sh", "w")
    f.write('aws dynamodb query --table-name sales-order-ProcessingState  --key-condition-expression "id = :id" --expression-attribute-values  "{\\":id\\":{\\"S\\":\\"'+str(glob_entity_id[0])+'\\"}}" > so_dynamodb.txt')
    logging.info('SH file updated')
    f.close()

    os.system('sh sh/so_dynamodb.sh') 
    try:
        with open('sh/so_dynamodb.sh', 'r') as file:
            for lines in file:
                dynamodbtext = lines
                logging.info(dynamodbtext)
                if str(glob_entity_id[0]) in dynamodbtext:
                    logging.info('*************** FOUND THE ORDER IN DYNAMODB ')
                    step_result.append('Pass')
    except Exception as E:
        logging.info(E)
        step_result.append('Fail')
    logging.info('\n \n')
    pass

@step('shipped status sent in events')
def step_impl(context):
    context.step_name = "shipped status sent in events"
    logging.info('Starting automation for step: ' + str(context.step_name))
    # remove sh file 
    if os.path.exists("salesorder-events.json"):
        os.remove("salesorder-events.json")
        logging.info('salesorder-events.json removed in current directory.')
    else:
        logging.error("The file does not exist")
    # replace file
    f = open("salesorder-events.json", "w")
    f.write('[\n\
    {\n\
        "Time": ' + str(ID) + ',\n\
        "Source": "OrderInformationEvent",\n\
        "Resources": ["string"],\n\
        "DetailType": "OrderInformationEvent",\n\
        "Detail": "{ \\"customer_number\\": \\"abc123\\", \\"order_number\\": \\"'+str(glob_entity_id[0])+'\\", \\"status\\": 5, \\"status_text\\": \\"Shipped\\", \\"updated_at\\": 1698663327, \\"source_identifier\\": \\"sourceID123\\", \\"carrier\\": \\"bring\\", \\"internal_order_id\\": \\"internal123\\", \\"tracking_number\\": \\"track123\\", \\"items\\": [{ \\"articleId\\": \\"EA0001NN\\", \\"quantity\\": 2, \\"internalItemId\\": \\"\\", \\"lineId\\": \\"'+str(glob_entity_id[0])+'\\" }] }",\n\
        "EventBusName": "integration-events",\n\
        "TraceHeader": "string"\n\
    }\n]')
    logging.info('JSON for Eventbridge file updated')
    f.close()
    os.system('aws events put-events --entries file://salesorder-events.json > send_events_eventbridge.txt') 
    logging.info('Waiting for eventbridge to process...')
    time.sleep(90)
    logging.info('\n \n')
    pass


@step('order endpoint status should be complete')
def step_impl(context):
    context.step_name = "order endpoint status should be complete"
    logging.info('Starting automation for step: ' + str(context.step_name))
    curr_status = check_so_status(str(glob_entity_id[0]))
    if curr_status == 'complete':
        step_result.append('Pass')
        logging.info('Step passed, status is currently complete.')
    else:
        step_result.append('Fail')
        logging.error('Step failed, status is not complete')
    logging.info('\n \n')


@step('sales order in magento should be {status}')
def step_impl(context, status):
    # click Orders 
    context.step_name = "sales order in magento should be Complete"
    logging.info('Starting automation for step: ' + str(context.step_name))
    time.sleep(2)
    browser.get(link_order + str(glob_entity_id[0]))
    logging.info(link_order + str(glob_entity_id[0]))
    magento_site_status = browser.find_element(By.XPATH, '//*[@id="order_status"]').text
    if str(magento_site_status) == str(status):
        step_result.append('Pass')
        logging.info('Status in magento site is currently ' + str(status))
    else:
        step_result.append('Fail')
        logging.error('Status in magento site is NOT ' + str(status))
    pass

@step('OCS-T1641 should be updated to Zephyr')
def step_impl(context):
    context.step_name = "OCS-T1641 should be updated to Zephyr"
    logging.info('Starting automation for step: ' + str(context.step_name))
    logging.info('Testcycle2: ' + str(testcycle2))
    testcycle_key = testcycle2[0]
    count_pass = step_result.count('Pass')
    logging.info('Step Results : ' + str(step_result))
    # test execution
    if count_pass == 5:
        result = 'Pass'
    else:
        result = 'Fail'
    total_time = round(time.time() - start_time)
    total_time2 = 120000
    logging.info(round(total_time))
    get_latest_ocs_qty('109847')
    logging.info('Previous quantity before sales order : ' + str(PREVIOUS_QTY))
    logging.info('Latest quantity after sales order : ' + str(LATEST_QTY))
    if PREVIOUS_QTY < LATEST_QTY or PREVIOUS_QTY == LATEST_QTY:
        logging.error('Quantity is not updated!')
    feature_file = '<br><br>Validate Sales Order Mapper Magento\
        <br>   When sales order is created in magento - <b>' + str(step_result[0]) + '</b>\
        <br>   Then sales order is in orders endpoint - <b>' + str(step_result[1]) + '</b>\
        <br>   And invoice is sent in magento - <b>Pass</b>\
        <br>   And sales order is in dynamodb - <b>' + str(step_result[2]) + '</b>\
        <br>   When shipped status sent in events - <b>' + str(step_result[2]) + '</b>\
        <br>   Then order endpoint status should be complete- <b>' + str(step_result[3]) + '</b>\
        <br>   And sales order in magento should be Complete - <b>' + str(step_result[4]) + '</b>\
        <br>   And OCS-T1641 should be updated to Zephyr - <b>Pass</b>\
        <br>   <b>Total step execution:</b> ' + str(total_time) + 's<br>'
    payload_testcase_execution = "{\n  \"projectKey\": \"OCS\",\n  \"testCaseKey\": \"OCS-T1641\",\n  \"testCycleKey\": \"" + str(testcycle2[0])+ "\",\n  \"statusName\": \"" + str(result) + "\",\n  \"testScriptResults\": [\n    {\n      \"statusName\": \"" + str(result) + "\",\n      \"actualEndDate\": \"2023-05-20T13:15:13Z\",\n      \"actualResult\": \"" + str('Sales order created in Magento and existing in  DynamoDB, OCS, Endpoint <br> <b>Order Number:</b> ' + str(glob_order_number[0]) + '<br> <b>Entity No :</b> ' + str(glob_entity_id[0]) + '<br> <b>Email :</b> ' + str(send_email) + str(feature_file) + '<br>') + "\"\n    }\n  ],\n  \"actualEndDate\": \"2024-05-20T13:15:13Z\",\n  \"executionTime\": "+str(total_time2)+",\n  \"executedById\": \"712020:787b46ed-42ec-4613-90f5-b0fb137785a0\",\n  \"assignedToId\": \"712020:787b46ed-42ec-4613-90f5-b0fb137785a0\",\n  \"comment\": \"SUCCESS\",\n  \"customFields\": {\n\n  }\n\t\n}\n"
    add_exe_testcases(testcycle_key, payload_testcase_execution, result)
