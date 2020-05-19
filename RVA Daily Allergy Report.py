#! python3
#Author: Joe DeFilippo
# Get today's allergy forecast in Richmond, using Geckodriver/Firefox and email it to distribution list

import datetime, smtplib, ssl
from selenium import webdriver

def formatTime(dt):
    return dt.strftime('%I:%M')

def formatDay(dt):
    return dt.strftime('%m/%d')

def sendEmail(content):
    currentTime = datetime.datetime.now()
    port = 587  # For starttls
    smtp_server = 'smtp.gmail.com'
    sender_email = 'pythonjoed@gmail.com'
    receiver_email = ['distribution_list@distro.com']
    password = input('Type your password and press enter:')
    message = 'Subject: {}\n\n{}'.format('RVA Allergy Report '+formatDay(currentTime), content)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

browser = webdriver.Firefox()
browser.get('https://www.accuweather.com/en/us/richmond-va/23225/allergies-weather/331252')

output = ''
#ragweed pollen
elem = browser.find_element_by_class_name('cond')
elem2 = browser.find_element_by_class_name('value-text')
output += '-' + elem.text + ' ' + elem2.text + '/10 \n'

#grass pollen
elem =browser.find_element_by_xpath("//span[contains(text(),'Grass Pollen')]/..")
elem.click()
elem = browser.find_element_by_class_name('cond')
elem2 = browser.find_element_by_class_name('value-text')
output += '-' + elem.text + ' ' + elem2.text + '/10 \n'

#tree pollen
elem =browser.find_element_by_xpath("//span[contains(text(),'Tree Pollen')]/..")
elem.click()
elem = browser.find_element_by_class_name('cond')
elem2 = browser.find_element_by_class_name('value-text')
output += '-' + elem.text + ' ' + elem2.text + '/10 \n'

#mold
elem =browser.find_element_by_xpath("//span[contains(text(),'Mold')]/..")
elem.click()
elem = browser.find_element_by_class_name('cond')
elem2 = browser.find_element_by_class_name('value-text')
output += '-' + elem.text + ' ' + elem2.text + '/10 \n'

#Dust and Dander
elem = browser.find_element_by_xpath("//span[contains(text(),'Dust & Dander')]/..")
elem.click()
elem = browser.find_element_by_class_name('cond')
elem2 = browser.find_element_by_class_name('value-text')
output += '-' + elem.text + ' ' + elem2.text + '/10'

browser.close()
print(output)
sendEmail(output)


