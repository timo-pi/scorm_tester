from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

sf_url = 'https://hcm12preview.sapsf.eu/login?company=lidlstiftuT3&loginMethod=PWD#/login'
user_name = 'INT-PIECHOTTA'
sf_password = 'Freeway22!'
s = Service('msedgedriver.exe')
SCORM_path = r'C:\Users\timop\Downloads\SK-Test.zip'
SCORM_id = 'Test_310522_2'


def start_upload(media_path):
    driver = webdriver.Edge(service=s)
    driver.get(sf_url)
    print(driver.title)
    # driver.quit()

    # Login
    name_field = driver.find_element(By.ID, '__input1-inner')
    password_field = driver.find_element(By.ID, '__input2-inner')
    name_field.send_keys(user_name)
    password_field.send_keys(sf_password)
    driver.find_element(By.ID, '__button2-inner').click()

    # open Admin-Page
    driver.get('https://lidlstiftu-stage.plateau.com/learning/admin/main.do?fromSF=y')
    driver.get('https://lidlstiftu-stage.plateau.com/learning/admin/tools/import_content/contentAssistantStart.do?adminShellMenuId=importContent')

    # Upload SCORM-File
    driver.find_element(By.ID, 'submitbutton').click()
    browse_btn = driver.find_element(By.ID, 'pickFiles')
    browse_btn.send_keys(SCORM_path)
    #driver.find_element(By.ID, 'nextButton').click()

    driver.execute_script('''
    		$('#buttons2').show();
    		$('#buttons3').show();
    		$('#header2').show();
    		$('#configureSettings').show();
    		$('#breadCrumbStep3').show();
    ''')
    driver.execute_script('document.getElementById("contentDeploymentLocationID").value = "CONTENTTEST";')
    driver.execute_script('document.getElementById("cpdomain").value = "TESTING";')
    driver.execute_script('document.getElementById("contentPackageID").value = "Test_310522_2";')
    driver.find_element(By.ID, 'finishButton').click()

    # Wait until upload is finished
    WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.ID, 'editContentObjectIDIcon')))
    driver.find_element(By.ID, 'schedButton').click()
    driver.find_element(By.ID, 'submitbutton').click()


    '''driver.find_element(By.ID, 'utilityLinksMenuId-inner').click()
    driver.find_element(By.LINK_TEXT, 'Admin-Center').click()
    # driver.implicitly_wait(4)
    admin_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, '__link1')))
    admin_link.click()
    # WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
    # driver.find_element(By.ID, '__link1').click()
    driver.find_element(By.LINK_TEXT, 'Schulungsadministration').click()

    # Content Upload Form
    driver.find_element(By.LINK_TEXT, 'Content').click()
    driver.find_element(By.LINK_TEXT, 'Import Content').click()
    driver.find_element(By.ID, 'submitbutton').click()
    file = driver.find_element(By.ID, 'browseFilesButton')
    file.send_keys('C:\\Users\\timop\\Downloads\\SK-Test.zip')
    driver.find_element(By.ID, 'nextButton').click() '''




start_upload("test")