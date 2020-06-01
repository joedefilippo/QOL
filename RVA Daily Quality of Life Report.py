#! python3
#Author: Joe DeFilippo
# Get today's hourly weather and allergy forecast in Richmond, VA
# using Geckodriver/Firefox and email it to distribution list

import datetime, smtplib, ssl, time
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
    receiver_email = ['seema.defilippo@gmail.com', 'joseph.j.defilippo@gmail.com']

    password = open('C:\\Users\\User\\Desktop\\pw.txt').read()

    message = 'Subject: {}\n\n{}'.format('RVA Daily Quality of Life Report '+formatDay(currentTime), content)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()

browser = webdriver.Firefox()
browser.get('https://www.accuweather.com/en/us/richmond-va/23225/allergies-weather/331252')

output = '-----Allergy Report-----\n'
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

#Navigate to Richmond / Today / Hourly
elem = browser.find_element_by_class_name("recent-location-display")
elem.click()

elem = browser.find_element_by_xpath("//span[contains(text(),'Hourly')]/..")
elem.click()


output += '\n\n-----Hourly Forecast-----\n'

time.sleep(3)
today = browser.find_elements_by_class_name('date')
temp = browser.find_elements_by_class_name('temp')
precip = browser.find_elements_by_class_name('precip')

for i in range(len(today)):
    output += (today[i].find_element_by_xpath(".//p").text + ' ' + temp[i].text + ' ' + precip[i].text + '\n')

output = output.replace("°"," F")

browser.close()
print(output)
sendEmail(output)



