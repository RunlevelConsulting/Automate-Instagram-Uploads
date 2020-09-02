import os
import sys
import time
from selenium import webdriver

username = sys.argv[1]
password = sys.argv[2]
image = sys.argv[3]
description = sys.argv[4]
cwd = '/home/ubuntu/Desktop'
root_cwd = '/root/Desktop'


################################
# DOWNLOAD IMAGE
################################
if len(image) > 0:
  os.system('wget -q "' + image + '" -O ' + cwd + '/pic.jpg')


################################
# FIREFOX
################################
user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
profile =webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", user_agent)
driver = webdriver.Firefox(profile,service_log_path=os.devnull)
driver.set_window_size(360,640)
driver.set_window_position(0,0)


################################
# LOGIN
################################
driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
time.sleep(8)

field = driver.find_element_by_css_selector("input[type='text']")
field.send_keys(username)
field = driver.find_element_by_css_selector("input[type='password']")
field.send_keys(password)
time.sleep(2)
button=driver.find_elements_by_xpath("//*[contains(text(), 'Log In')]")
button[0].click()

time.sleep(10)
button=driver.find_elements_by_xpath("//*[contains(text(), 'Not Now')]")
if len(button) > 0:
    button[0].click()

time.sleep(10)
button=driver.find_elements_by_xpath("//*[contains(text(), 'Cancel')]")
if len(button) > 0:
    button[0].click()


################################
# SELECT IMAGE
################################
os.system('timeout 30 actiona -e ' + root_cwd + '/selectImage.ascr')
button=driver.find_elements_by_xpath("//*[contains(text(), 'Next')]")
button[0].click()
time.sleep(6)


################################
# ADD DESCRIPTION
################################
if len(description) > 0:
  field = driver.find_elements_by_tag_name('textarea')[0]
  field.click()
  field.send_keys(description)
  time.sleep(2)


################################
# POST!
################################
button=driver.find_elements_by_xpath("//*[contains(text(), 'Share')]")
button[1].click()
time.sleep(5)


################################
# SHUT IT DOWN
################################

# Remove all images
os.system('rm -f ' + cwd + '/*.jpg')

driver.quit()
