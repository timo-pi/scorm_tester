from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import random

sf_url = 'https://hcm12preview.sapsf.eu/login?company=lidlstiftuT3&loginMethod=PWD#/login'
user_name = '***'
sf_password = '***'
s = Service('msedgedriver.exe')
SCORM_path = r'C:\temp2\dummy-scorm.zip'
# SCORM_id = 'Test_310522_2'
random_prefix = str(random.uniform(1000,9999))

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
    scorm_id = random_prefix + "_Automatisierung"
    driver.execute_script('document.getElementById("contentPackageID").value = "' + scorm_id + '";')
    driver.find_element(By.ID, 'finishButton').click()

    # Wait until upload is finished
    WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.ID, 'editContentObjectIDIcon')))
    driver.find_element(By.ID, 'schedButton').click()
    driver.find_element(By.ID, 'submitbutton').click()

    #driver.get('https://lidlstiftu-stage.plateau.com/learning/admin/main.do?fromSF=y#/learning/itementitymanager@/')
    #print('going to sleep..........................................................................')

    #time.sleep(5)
    #print('Continue................................................................................')
    # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'addNewLink')))
    #driver.find_element(By.XPATH, '//*[@id="addNewLink"]').click()

    driver.get('https://lidlstiftu-stage.plateau.com/learning/admin/main.do?fromSF=y#/learning/itementitymanager@/core/create/item/entity/add-detail')
    #driver.findElement(By.ID, 'item.classification-label)').click()
    print('going to sleep..........................................................................')
    time.sleep(5)
    driver.find_element(By.ID, 'item.classification-label').click()
    # list1 = driver.find_element(By.ID, '__list1')
    driver.find_element(By.ID, '__item7-item.classification-1').click()

    driver.find_element(By.ID, '__item7-item.classification-1').click()
    driver.find_element(By.ID, 'item.componentTypeID_select-arrow').click()
    driver.find_element(By.ID, '__item12').click()
    driver.find_element(By.ID, 'item.title-inner').send_keys('Hallo...')

    #'item.add.online.completionStatus-arrow','__item26-item.add.online.completionStatus-3','item.requirementTypeID_select-arrow','__item371','item.customColumns_30_select-arrow','__item403','item.customColumns_40_select-arrow','__item407','item.customColumns_50_select-arrow','__item411'

    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    print("last_height: ", last_height)

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        print("new_height: ", new_height)




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