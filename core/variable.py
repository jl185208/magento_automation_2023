from core.core import *

binary_location = 'C://Users//TLibres//Desktop//Automations//BBIMagento//bbi_magento//chrome-win32//chrome.exe'
driver_location = 'C://Users//TLibres//Desktop//Automations//BBIMagento//bbi_magento//chromedriver//chromedriver.exe'


service = Service(executable_path=driver_location)
options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--window-size=1920,1080")

browser = webdriver.Chrome(service=service, options=options)

# new article
send_sku  =  'TEST' + ID 
send_title  =  "Automated Title v" + ID
send_description  =  "This is a sample Automated Article Creation Timestamp :  " + ID
send_price  =  12 
send_barcode  =  "12300" 
send_weight  =  1 
send_coo  =  "Norway"
send_hscode  =  61051000  
send_qty = 1500

# sales order
send_email = 'T' + ID + '@test.com'
send_fname = 'Johnny'
send_lname = 'Test'
send_company = 'Test Company'
send_street = 'Sandakarveien 23'
send_country = 'Norway'
send_region = 'Oslo'
send_city = 'Oslo'
send_postal = '1012'
send_phonenum = '+47 923 29 442' 

glob_order_number = []
glob_entity_id = []
step_result = []
testcycle = []
testcycle2 = []
cwd = os.getcwd()
logdump = []
