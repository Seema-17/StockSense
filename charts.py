from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import requests
import json
import pyotp
import time
import yfinance as yf
from PIL import Image


bot_token = '5946827015:AAE68lwUtZpgtlAw-o4pfTF2BIG3Jr_uCC0'
chat_id = '1001836603765'
totp_key = ''
totp = pyotp.TOTP(totp_key)
userid = ""
password = ""
displayXPath = "/html/body/cq-context/div[1]/div[2]/div[1]/cq-menu[3]/span/translate"
radioXPath = "/html/body/cq-context/div[1]/div[2]/div[1]/cq-menu[3]/cq-menu-dropdown/cq-item[17]/div/span/span"
settingsXPath = "/html/body/cq-context/div[1]/div[2]/div[1]/cq-menu[3]/cq-menu-dropdown/cq-item[17]/span"
brickXPath = "/html/body/cq-context/cq-dialog[2]/cq-aggregation-dialog/div[2]/div[2]/p/input"
closeXPath = "/html/body/cq-context/cq-dialog[2]/cq-aggregation-dialog/div[1]"
base_link = "https://kite.zerodha.com/chart/ext/ciq/NSE/"
base_path = 'C:/Users/jaimu/OneDrive/Desktop/smg/test/' 
f = 1.5


ticker_list = {'ITC': 424961, 'LT' : 2939649, 'WHIRLPOOL' : 4610817 }

for key, value in ticker_list.items(): 
 driver = webdriver.Chrome(r'C:\Users\jaimu\OneDrive\Desktop\smg\chromedriver.exe') 
 driver.maximize_window()
 driver.get("https://kite.zerodha.com/")

 driver.find_element_by_id("userid").send_keys(userid + Keys.RETURN)
 driver.find_element_by_id("password").send_keys(password + Keys.RETURN)
 time.sleep(1)
 driver.find_element_by_xpath(xpath="//input[@placeholder='••••••']").send_keys(totp.now())
 driver.find_element(By.XPATH, '//button[normalize-space()="Continue"]').click()
 time.sleep(1)
 
 link = base_link + key + "/" + str(value)
 path = base_path + key + ".png"
 #get current price
 brickSize = 5
 driver.get(link)
 
 time.sleep(3)

 driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
 time.sleep(3)

 element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, displayXPath)))
 element.click();

 element = driver.find_element_by_xpath(xpath=settingsXPath)
 actions = ActionChains(driver)
 actions.move_to_element(element).perform()

 element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, settingsXPath)))
 element.click();

 element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, brickXPath)))
 element.send_keys(str(brickSize)+Keys.RETURN)

 element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, closeXPath)))
 element.click();
 
 driver.save_screenshot(path)
 driver.close()
 
 
for key, value in ticker_list.items(): 

 file = base_path + key + ".PNG"

 files = {
     'photo': open(file, 'rb')
 }

 message = ('https://api.telegram.org/bot'+ bot_token + '/sendPhoto?chat_id=' 
           + chat_id)
 send = requests.post(message, files = files)
 
 url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
 data = {'chat_id': chat_id, 'text': key}
 requests.post(url, data)
  
 




