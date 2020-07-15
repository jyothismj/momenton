from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv, time

timeout = 30

output=''
url = "https://www.tobydealsau.com/"
itemsfile = "test_webui.csv"

chrome_driver_path = "C:/PY/b2bsvt/drivers/chromedriver.exe"
options = webdriver.ChromeOptions()
# options.add_argument('headless') 
options.add_argument("--start-maximized")
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
driver=webdriver.Chrome(options=options, executable_path=chrome_driver_path)

def searchProduct(item):
    print ("Searching %s" % str(item))
    try:
        element = wait(driver, timeout).until(EC.presence_of_element_located((By.ID, 'search')))
        element.clear()
        element.send_keys(item)
    
        scrollViewToElementAndClick("//button[@title='Search']")

        wait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//h1[contains(.,'Search results for')]")))
        print ("{} found".format(item))
    except TimeoutException as e:
        print ("{} not found".format(item))
        return

def acceptCookies():
    try:
        scrollViewToElementAndClick("//span[text()='Accept & Close']")
    except TimeoutException as e:
        pass

def addToCart():
    try:
        elem = driver.find_elements_by_xpath("//button[@title='Add to Cart']")
        elem[0].click()

       elem = wait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Continue Shopping']")))
        print ("Item added to cart...")
    except TimeoutException as e:
        print ("failed to addToCart")
        return

def checkoutItem():
    try:
        elem = wait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//button/span/span[text()='Checkout']")))
        elem.click()

        # Checkout Method
        wait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Order Summary']")))
        scrollViewToElementAndClick("//input[@id='login:guest']")
        elem = driver.find_elements_by_xpath("//span[text()='Continue']")
        elem[0].click()
        print ("Checking out as Guest user...")

        # Billing/Shipping Information
        scrollViewToElementAndInputText("//input[@id='billing:firstname']", "Jyothis")
        scrollViewToElementAndInputText("//input[@id='billing:lastname']", "Jose")
        scrollViewToElementAndInputText("//input[@id='billing:email']", "jyo123@gmail.com")
        scrollViewToElementAndInputText("//input[@id='billing:street1']", "19A Gardiner Street, Berwick")
        scrollViewToElementAndInputText("//input[@id='billing:city']", "Melbourne")
        scrollViewToElementAndClick("//select[@id='billing:region_id']/option[@title='Victoria']")
        scrollViewToElementAndInputText("//input[@id='billing:postcode']", "3806")
        scrollViewToElementAndClick("//select[@id='billing:country_id']/option[@value='AU']")
        scrollViewToElementAndInputText("//input[@id='billing:telephone']", "0452299999")
        elem[1].click()
        wait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Order Summary']")))
        print ("Entered billing details...")

        # Shipping Method
        scrollViewToElementAndClick("//label[contains(text(),'Standard Shipping Method')]")
        elem[3].click()
        print ("Selected shipping method...")

        # Payment Information
        print ("Waiting for payment...")
        time.sleep(5)

    except TimeoutException as e:
        print ("failed to checkout")
        return

def scrollViewToElement(elem_xpath, count=1):
    '''
    Scroll view to the element
    @param elem_xpath: element to scrollview to 
    '''
    scroll = 0
    elem = wait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, elem_xpath)))
    while scroll < count: # scroll count times
        driver.execute_script('arguments[0].scrollIntoView({block: "center"});', elem)
        time.sleep(2)
        scroll += 1
    time.sleep(2)

def scrollViewToElementAndClick(elem_xpath, count=1):
    '''
    Scroll view to the element and click
    @param elem_xpath: element to scrollview to 
    '''
    scroll = 0
    elem = wait(driver, 5).until(EC.presence_of_element_located((By.XPATH, elem_xpath)))
    while scroll < count: # scroll count times
        driver.execute_script('arguments[0].scrollIntoView({block: "center"});', elem)
        time.sleep(2)
        scroll += 1
    time.sleep(2)
    elem.click()

def scrollViewToElementAndInputText(elem_xpath, input_text, count=1):
    '''
    Scroll view to the element and click
    @param elem_xpath: element to scrollview to 
    '''
    scroll = 0
    elem = wait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, elem_xpath)))
    while scroll < count: # scroll count times
        driver.execute_script('arguments[0].scrollIntoView({block: "center"});', elem)
        time.sleep(2)
        scroll += 1
    elem.clear()
    elem.send_keys(input_text)

def exitBrowser():
    driver.close()
    driver.quit()


if __name__ == "__main__":

    driver.get(url)
    acceptCookies()
    with open(itemsfile, 'r') as readfile:
        csv_reader = csv.reader(readfile, delimiter=',')
        for row in csv_reader:      # ['Item1', 'Item2']
            product = str(row[0])
            searchProduct(product)
            addToCart()
    checkoutItem()
    readfile.close()
    exitBrowser()
