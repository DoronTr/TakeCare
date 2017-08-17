# -*- coding: utf-8 -*-
# Import smtplib for the actual sending function
import smtplib
import time,datetime
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from flask import Flask
app = Flask(__name__)

def sendMail(str_param):

  msg = 'Subject: {}\n\n{}'.format("!!!!! MAIL TITLE -" +str_param + "!!!!", "Go to MACCABI !")
  # headers
  TO = '' #mail of contact
  FROM = '' # MyMailAddress

  # SMTP
  smtp_host = 'smtp.gmail.com'
  smtp_port = 587
  server = smtplib.SMTP()
  server.connect(smtp_host, smtp_port)
  server.ehlo()
  server.starttls()
  server.login('#MyMailAddress', '#PASSWORD')
  server.sendmail(FROM, TO, msg)
  server.quit()
#sendMail()

@app.route('/')
def gotoMaccabi():
    print("Hello world")
    if (True):
      driver = webdriver.Chrome(r"chromedriver.exe")
      driver.get("http://guide.maccabi4u.co.il/SearchChapter.aspx?ChapterId=1" )
      print(format( datetime.datetime.now()  , '%H:%M:%S'))
      time.sleep(10)

      wantedDoctorName ="יניב רון".decode('utf-8')
      elem = driver.find_element_by_id("DocName")
      elem.send_keys(wantedDoctorName)

      time.sleep(4);
      elem = driver.find_element_by_id("SearchButton").click()

      time.sleep(4)

      elem = driver.find_element_by_xpath(r"//*[@id='Content']/section[3]/div[1]/section/section[1]")
      f = open('workfile.txt', 'w+')
      f.write(elem.text.encode('utf-8'))
      f.close()
      #print (elem.text.encode('utf-8'))
      # checkAvailableHotel(driver)
      # moveOverResaults(driver, wantedDoctor)
      driver.quit();
      time.sleep(1200)
      return "OK"
    if __name__ == "__main__":
      app.run()
      
def moveOverResaults(driver, wantedDoctor):
  # get all of the rows in the table
  resultTableRows = driver.find_elements_by_xpath(r".// tbody[ @ id = 'tableRows']/tr")
  for row in resultTableRows:
    # Get the columns (all the column 2)
    col3 = row.find_elements_by_tag_name("td")[3]  # note: index start from 0, 1 is col 2
    # print (col3.text)  # prints text from the element

    col2 = row.find_elements_by_tag_name("td")[2]  # note: index start from 0, 1 is col 2
    # print (col2.text)  # prints text from the element

    col5 = row.find_elements_by_tag_name("td")[5]  # note: index start from 0, 1 is col 2
    print(col3.text, col2.text, col5.text)  # prints text from the element

    if (compareDate(str(col3.text))):
      if (col2 == wantedDoctor):
          print("*********************** Im OK ************************")
          sendMail(wantedDoctor)

def checkAvailableHotel(driver, wantedHotel,wantedArea):
  driver.get(r"http://www.hvr.co.il/nofesh_search.aspx")
  time.sleep(1)
  elem = driver.find_element_by_id("main_type")
  goToElemInDropDownList(elem, wantedArea)
  time.sleep(1)
  elem = driver.find_element_by_id("second_type_i")
  goToElemInDropDownList(elem, wantedHotel)
  time.sleep(1)
  driver.find_element_by_xpath('.//td/a').click()
  time.sleep(2)

  
def goToElemInDropDownList(elem, value):
  for option in elem.find_elements_by_tag_name('option'):
    # print(option.text)
    if option.text == value:
      break
    else:
      ARROW_DOWN = u'\ue015'
      elem.send_keys(ARROW_DOWN)

def compareDate(tmpDate):
  date1 = "31/08/2017"

  newdate1 = time.strptime(date1, "%d/%m/%Y")
  newdate2 = time.strptime(tmpDate, "%d/%m/%y")

  if (newdate1 > newdate2):
    return False
  else:
    return True





gotoMaccabi()

