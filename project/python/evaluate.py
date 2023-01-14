from typing import Sized
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
#import openpyxl
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#class PythonOrgSearch():

# def __init__(self):
        

#path=""
 #workbook=openpyxl.load_workbook(path)
 #sheet=workbook.active
def evaluateCandidate():
   driver = webdriver.Firefox()
   #driver = self.driver
   #driver = webdriver.Firefox() 
   driver.get('https://questionnaire.evalart.com/user/login')
   emaiinput=driver.find_element_by_id('email')
   emaiinput.send_keys('shruthi2602@outlook.com')
   passwordInput=driver.find_element_by_id('password')
   passwordInput.send_keys('shruHR@26021991')
   driver.find_elements(By.XPATH, '//html/body/div[1]/div[2]/div/div/div/div[2]/form/div[3]/div/input')[0].click()
   driver.find_element(By.XPATH, '//html/body/div[1]/div[1]/div/div/div/div[2]/div[3]/div/div[1]/div[1]/div[2]/button[1]').click()
   #driver.execute_script('document.getElementById("btnPeople").click()')
   #driver.find_element_by_css_selector("input#upload-btn-prev.btn.btn-primary.btn-large").click()
   #print(driver.find_element(By.XPATH,("div#bootbox-body")))
   

evaluateCandidate()
sys.exit(0)

   #driver.find_element_by_xpath("//input[@id='upload-btn']").click()

   #driver.execute_script('document.getElementById("upload-btn-prev").click()')
   #driver.find_element_by_xpath('//[@id="upload-btn-prev"]').click()
   #driver.find_element_by_xpath('//upload-btn-previd[@id]').click()
   #driver.find_element_by_css_selector(".button_main").click()
   #driver.close()
   #//*[@id="upload-btn-prev"]
   





   
    #print("error1")
     #WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='modal in' and contains(.,'Security Mode is disabled')]//following::div[1]//button[@id='btnPeople']"))).click()

  
   
   



#  def closeResources(self):
#     self.driver.close()
#     self.driver.exit() 

#pythonOrgSearch=PythonOrgSearch()




