'''
Author : Joselito G. Libres
Date : 10/24/2023

ChangeLog : 

1/12/2023 - Joselito Libres - Updated and replaced deprecated codes

Test Steps 
--------------
1.) Login to Shopify.
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


logfiles = []
zephyr_report = ""
loggings()

@step('that article is added in magento')
def step_impl(context):
    context.step_name = "When that article is added in magento"
    logging.info('Starting Scenario: ' + str(context.scenario))
    logging.info('Starting automation for step: ' + str(context.step_name))
    browser.get(magento_link)
    try:
        browser.find_element(By.XPATH, '/html/body/section/div/form/fieldset/div[1]/div/input').send_keys('admin')
        browser.find_element(By.XPATH, '//*[@id="login"]').send_keys('123456aA@')
        browser.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[3]/div[1]/button').click()
        browser.implicitly_wait(10)
    except Exception as e:
        logging.info('Already logged in!')
        pass
    # click Catalog button
    browser.find_element(By.XPATH, '//*[@id="menu-magento-catalog-catalog"]/a').click()
    browser.implicitly_wait(10)
    # click Products 
    time.sleep(2)
    browser.find_element(By.XPATH, '//*[@id="menu-magento-catalog-catalog"]/div/ul/li/div/ul/li[1]/a').click()
    time.sleep(5)
    browser.find_element(By.ID, 'add_new_product-button').click()
    browser.implicitly_wait(160)
    # input SKU details
    browser.find_element(By.NAME, 'product[name]').send_keys(send_title)         # prod_name
    time.sleep(1)
    browser.find_element(By.NAME, 'product[sku]').clear()
    browser.find_element(By.NAME, 'product[sku]').send_keys(send_sku)            # prod_sku
    browser.find_element(By.NAME, 'product[price]').send_keys(send_price)        # prod_sku
    browser.find_element(By.NAME, 'product[quantity_and_stock_status][qty]').send_keys(send_qty)
    browser.find_element(By.NAME, 'product[weight]').send_keys(send_weight)        # prod_sku
    # click save button
    time.sleep(5)
    browser.find_element(By.XPATH, '//*[@id="anchor-content"]/div[1]/div[2]/div/div/div/button[2]').click()
    time.sleep(1)
    browser.find_element(By.ID, 'save_and_close').click()
    logging.info('Created SKU : ' + str(send_sku))
    logging.info('\n \n \n')
    pass
    
    time.sleep(450)
@step('article should be in ocs')
def step_impl(context):
    context.step_name = "article should be in ocs"
    logging.info('Starting automation for step: ' + context.step_name)
    step_result.append(check_article_ocs(str(send_sku)))

@step('article should be in article endpoint')
def step_impl(context):
    context.step_name = "article should be in article endpoint"
    logging.info('Starting automation for step: ' + context.step_name)
    step_result.append(check_aricle_endpoint(send_qty, send_sku))

@step('article should be in dynamodb')
def step_impl(context):
    context.step_name = "article should be in dynamodb"
    logging.info('Starting automation for step: ' + context.step_name)
    output_sku = []
    os.system('aws dynamodb query --table-name article-master-sync-ProcessingState  --key-condition-expression "id = :id" --expression-attribute-values  "{\\":id\\":{\\"S\\":\\"'+str(send_sku)+'\\"}}" > dynamodb.txt') 
    with open('dynamodb.txt', 'r') as file:
         for lines in file:
             dynamodbtext = lines
             logging.info(dynamodbtext)
             if str(send_sku) in dynamodbtext:
                 logging.info('*************** FOUND THE SKU IN DYNAMODB ')
                 output_sku.clear()
                 output_sku.append('Pass')
    if str(output_sku[0]) == str('Pass'):
        step_result.clear
        step_result.append('Pass')
        logging.info('Step Passed')
        logging.info('\n \n')
    else:
        step_result.clear
        step_result.append('Fail')
        logging.info('Step Failed')
        logging.info('\n \n')

@step('OCS-T1633 should be updated to Zephyr')
def step_impl(context):
    context.step_name = "OCS-T1633 should be updated to Zephyr"
    logging.info('Starting automation for step: ' + context.step_name)
    # create testcycle
    payload = "{\n  \"projectKey\": \"OCS\",\n  \"name\": \"Magento BBI Functional Testing\",\n  \"description\": \"\",\n  \"plannedStartDate\": \"2023-03-15T13:15:13Z\",\n  \"plannedEndDate\": \"2024-03-20T13:15:13Z\",\n  \"jiraProjectVersion\": 10000,\n  \"statusName\": \"Not Executed\",\n  \"folderId\": 8474767,\n\t\t\"ownerId\": \"712020:787b46ed-42ec-4613-90f5-b0fb137785a0\",\n  \"customFields\": {}\n}"
    testcycle_key = create_testcycle_func_test(payload)
    testcycle2.clear()
    testcycle2.append(testcycle_key)
    testcycle.append(testcycle_key)
    count_pass = step_result.count('Pass')
    # test execution
    if count_pass == 3:
        result = 'Pass'
    else:
        result = 'Fail'
    logging.info(step_result)
    total_time = round(time.time() - start_time)
    total_time2 = 120000
    #total_time2 = int(total_time)
    # f = open("bdd-actual- 1698757343.txt", "r")
    # prints = f.read()
    # logging.info('logdump : ' + str(prints))
    logging.info(round(total_time))
    feature_file = '<br><br>Scenario: Validate article creation in Magento\
        <br>   When that article is added in magento\
        <br>   Then article should be in ocs - <b>' + str(step_result[0]) + '</b>\
        <br>   And article should be in article endpoint - <b>' + str(step_result[1]) + '</b>\
        <br>   And article should be in dynamodb - <b>' + str(step_result[2]) + '</b>\
        <br>   And OCS-T1633 should be updated in Zephyr - <b>Pass</b>\
        <br>   <b>Total step execution:</b> ' + str(total_time) + 's<br>'
    payload_testcase_execution = "{\n  \"projectKey\": \"OCS\",\n  \"testCaseKey\": \"OCS-T1640\",\n  \"testCycleKey\": \"" + str(testcycle[0])+ "\",\n  \"statusName\": \"" + str(result) + "\",\n  \"testScriptResults\": [\n    {\n      \"statusName\": \"" + str(result) + "\",\n      \"actualEndDate\": \"2023-05-20T13:15:13Z\",\n      \"actualResult\": \"" + str('Article created in DynamoDB, OCS, Endpoint and Magento <br> <b>SKU:</b> ' + str(send_sku) + '<br> <b>Article Name :</b> ' + str(send_title) + '<br> <b>Qty :</b> ' + str(send_qty) + str(feature_file) + '<br>') + "\"\n    }\n  ],\n  \"actualEndDate\": \"2024-05-20T13:15:13Z\",\n  \"executionTime\": "+str(total_time2)+",\n  \"executedById\": \"712020:787b46ed-42ec-4613-90f5-b0fb137785a0\",\n  \"assignedToId\": \"712020:787b46ed-42ec-4613-90f5-b0fb137785a0\",\n  \"comment\": \"SUCCESS\",\n  \"customFields\": {\n\n  }\n\t\n}\n"
    #payload_testcase_execution = "{\n  \"projectKey\": \"OCS\",\n  \"testCaseKey\": \"OCS-T1640\",\n  \"testCycleKey\": \"" + str(testcycle[0])+ "\",\n  \"statusName\": \"" + str(result) + "\",\n  \"testScriptResults\": [\n    {\n      \"statusName\": \"" + str(result) + "\",\n      \"actualEndDate\": \"2023-05-20T13:15:13Z\",\n      \"actualResult\": \"" + str('Article created! <br> Qty is updated.') + "\"\n    }\n  ],\n  \"actualEndDate\": \"2018-05-20T13:15:13Z\",\n  \"executionTime\": 120000,\n  \"executedById\": \"712020:787b46ed-42ec-4613-90f5-b0fb137785a0\",\n  \"assignedToId\": \"712020:787b46ed-42ec-4613-90f5-b0fb137785a0\",\n  \"comment\": \"SUCCESS\",\n  \"customFields\": {\n\n  }\n\t\n}\n"
    add_exe_testcases(testcycle_key, payload_testcase_execution, result)