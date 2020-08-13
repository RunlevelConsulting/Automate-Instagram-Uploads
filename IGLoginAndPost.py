import os
import sys
import time
from selenium import webdriver

username = sys.argv[1]
password = sys.argv[2]
image = sys.argv[3]
description = sys.argv[4]
cwd = '/home/ubuntu/Desktop'


################################
# DOWNLOAD IMAGE
################################
if len(image) > 0:
  os.system('wget -q "' + image + '" -O ' + cwd + '/pic.jpg')


################################
# SET UP ACTIONA
################################
actiona = '<?xml version="1.0" encoding="UTF-8"?><scriptfile><settings program="actiona" version="3.9.2" scriptVersion="1.1.0" os="GNU/Linux"/><actions><action name="ActionPause" version="1.0.0"/><action name="ActionClick" version="1.0.0"/><action name="ActionEndProcedure" version="1.0.0"/></actions><parameters/><resources/><script pauseBefore="0" pauseAfter="0"><action name="ActionClick"><exception id="2" action="1" line=""/><exception id="1" action="0" line=""/><exception id="0" action="0" line=""/><exception id="33" action="0" line=""/><exception id="32" action="0" line=""/><parameter name="action"><subParameter name="value" code="0">pressRelease</subParameter></parameter><parameter name="amount"><subParameter name="value" code="0">1</subParameter></parameter><parameter name="positionOffset"><subParameter name="value" code="0"></subParameter><subParameter name="unit" code="0">0</subParameter></parameter><parameter name="position"><subParameter name="value" code="0">207:636</subParameter><subParameter name="unit" code="0">0</subParameter></parameter><parameter name="button"><subParameter name="value" code="0">left</subParameter></parameter></action><action name="ActionPause"><exception id="2" action="1" line=""/><exception id="1" action="0" line=""/><exception id="0" action="0" line=""/><parameter name="duration"><subParameter name="value" code="0">1</subParameter></parameter><parameter name="unit"><subParameter name="value" code="0">seconds</subParameter></parameter></action><action name="ActionClick"><exception id="2" action="1" line=""/><exception id="1" action="0" line=""/><exception id="0" action="0" line=""/><exception id="33" action="0" line=""/><exception id="32" action="0" line=""/><parameter name="action"><subParameter name="value" code="0">pressRelease</subParameter></parameter><parameter name="amount"><subParameter name="value" code="0">2</subParameter></parameter><parameter name="positionOffset"><subParameter name="value" code="0"></subParameter><subParameter name="unit" code="0">0</subParameter></parameter><parameter name="position"><subParameter name="value" code="0">233:107</subParameter><subParameter name="unit" code="0">0</subParameter></parameter><parameter name="button"><subParameter name="value" code="0">left</subParameter></parameter></action></script></scriptfile>'
f = open(cwd + '/selectImage.ascr', 'w+')
f.write(actiona)
f.close()



################################
# FIREFOX
################################
user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
profile =webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", user_agent)
driver = webdriver.Firefox(profile)
driver.set_window_size(360,640)
driver.set_window_position(0,0)


################################
# LOGIN
################################
url = 'https://www.instagram.com/accounts/login/?source=auth_switcher'
driver.get(url)
time.sleep(4)

field = driver.find_element_by_css_selector("input[type='text']")
field.send_keys(username)
field = driver.find_element_by_css_selector("input[type='password']")
field.send_keys(password)
time.sleep(2)
button=driver.find_elements_by_xpath("//*[contains(text(), 'Log In')]")
button[0].click()

time.sleep(5)
button=driver.find_elements_by_xpath("//*[contains(text(), 'Not Now')]")
if len(button) > 0:
    button[0].click()

time.sleep(5)
button=driver.find_elements_by_xpath("//*[contains(text(), 'Cancel')]")
if len(button) > 0:
    button[0].click()


################################
# SELECT IMAGE
################################
os.system('timeout 8 actiona -e ' + cwd + '/selectImage.ascr')
button=driver.find_elements_by_xpath("//*[contains(text(), 'Next')]")
button[0].click()
time.sleep(3)


################################
# ADD DESCRIPTION
################################
if len(description) > 0:
  field = driver.find_elements_by_tag_name('textarea')[0]
  field.click()
  field.send_keys(description)


################################
# POST!
################################
time.sleep(3)
button=driver.find_elements_by_xpath("//*[contains(text(), 'Share')]")
button[1].click()
time.sleep(2)


################################
# SHUT IT DOWN
################################

# Remove all images
os.system('rm -f /home/ubuntu/Desktop/*.jpg')

driver.quit()
