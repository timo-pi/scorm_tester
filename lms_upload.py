import os.path
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from configparser import ConfigParser

import gui
import writeExcel as we

#file_path = r'C:\Users\piechotta\Downloads'
#file_name = r"Testpaket_2.zip"
#sf_url = 'https://hcm12preview.sapsf.eu/login?company=lidlstiftuT3&loginMethod=PWD#/login'

config = ConfigParser()
config.read('.\scormtester.ini')
user_name = config.get('login', 'username')
sf_password = config.get('login', 'password')
wait_time = config.getint('settings', 'wait_time')
# Lidl URLs
login_url = config.get('lidl','login_url')
startpage_url = config.get('lidl', 'startpage_url')
admin_center_url= config.get('lidl', 'admin_center_url')
import_content_url = config.get('lidl','import_content_url')
manage_assignments_url = config.get('lidl', 'manage_assignments_url')
# Schwarz URLs
login_url_s = config.get('schwarz','login_url')
startpage_url_s = config.get('schwarz', 'startpage_url')
admin_center_url_s= config.get('schwarz', 'admin_center_url')
import_content_url_s = config.get('schwarz','import_content_url')
manage_assignments_url_s = config.get('schwarz', 'manage_assignments_url')

testusers = config.get('settings', 'testusers')
testuser_list = testusers.split (',')
email = config.get('settings', 'email')
lms_send_mail = config.getboolean('settings', 'lms_send_mail')
scorm_id = ''
random_prefix = ''
driver = ''

def initialize(lms):
    global driver

    edge = Service('msedgedriver.exe')
    driver = webdriver.Edge(service=edge)
    driver.maximize_window()
    if lms == 'lidl':
        driver.get(login_url)
        # Login
        next_action('__input1-inner', 'wait')
        name_field = driver.find_element(By.ID, '__input1-inner')
        password_field = driver.find_element(By.ID, '__input2-inner')
        name_field.send_keys(user_name)
        password_field.send_keys(sf_password)
        next_action('__button2-inner', 'wait')
        driver.find_element(By.ID, '__button2-inner').click()
    elif lms == 'schwarz':
        # SSO-Link
        driver.get(login_url_s)


def start_upload(file_path, lms):
    global scorm_id
    global random_prefix

    random_prefix = str(random.uniform(0, 1))[2:6]
    scorm_id = random_prefix + "_" + str(os.path.basename(file_path))[:-4]

    # open Admin-Page
    if lms == 'lidl':
        driver.get(admin_center_url)
        time.sleep(wait_time)
        driver.get(import_content_url)
    elif lms == 'schwarz':
        driver.get(admin_center_url_s)
        time.sleep(wait_time)
        driver.get(import_content_url_s)

    time.sleep(wait_time)
    # Upload SCORM-File
    driver.find_element(By.ID, 'submitbutton').click()
    browse_btn = driver.find_element(By.ID, 'pickFiles')
    browse_btn.send_keys(file_path)

    driver.execute_script('''
            $('#buttons2').show();
            $('#buttons3').show();
            $('#header2').show();
            $('#configureSettings').show();
            $('#breadCrumbStep3').show();
    ''')
    ###driver.execute_script('document.getElementById("contentDeploymentLocationID").value = "CONTENTTEST";')
    ###driver.execute_script('document.getElementById("cpdomain").value = "TESTING";')

    driver.execute_script('document.getElementById("contentPackageID").value = "' + scorm_id + '";')

    # **************************************************************
    # CREATE ITEM
    # **************************************************************

    driver.find_element(By.ID, 'addNewItem').click()
    time.sleep(2)
    driver.find_element(By.ID, 'componentTypeID').send_keys("ELEARNING")
    driver.find_element(By.ID, 'autoGenCompID').click()
    driver.find_element(By.ID, 'componentID').send_keys(scorm_id)
    driver.find_element(By.ID, 'componentIDPrefix').send_keys(random_prefix)

    driver.find_element(By.ID, 'componentTitle').send_keys(scorm_id)
    driver.find_element(By.ID, 'requirementType').send_keys("Optional")

    # LMS-Spezifische Settings
    if lms == 'lidl':
        driver.execute_script('document.getElementById("contentDeploymentLocationID").value = "CONTENTTEST";')
        driver.execute_script('document.getElementById("cpdomain").value = "TESTING";')
        driver.find_element(By.ID, 'domain1').send_keys("Domain for Testing")
        next_action('onlineCompletionStatus', 'TEST_COMPL')
    elif lms == 'schwarz':
        #driver.execute_script('document.getElementById("contentDeploymentLocationID").value = "Anbindung an Q-SFTP EContent Testing (Q-SFTP-SDL_EContent-Testing)";')
        next_action('contentDeploymentLocationID', 'Anbindung an Q-SFTP EContent Testing (Q-SFTP-SDL_EContent-Testing)')
        driver.execute_script('document.getElementById("cpdomain").value = "TST";')
        #driver.find_element(By.ID, 'domain1').send_keys("TST")
        time.sleep(2)
        next_action('onlineCompletionStatus', 'E_LEARNING_Abgeschlossen (E-Learning completed) - For Credit')

    driver.find_element(By.ID, 'reviewable').click()
    driver.find_element(By.ID, 'markCompleteUI').click()
    driver.find_element(By.ID, 'skipContentStructurePage').click()
    driver.find_element(By.ID, 'recordWhenLastObjectPassed').click()
    time.sleep(2)

    #driver.find_element(By.ID, 'componentID').send_keys(scorm_id)
    driver.find_element(By.ID, 'finishButton').click()

    time.sleep(2)
    # Wait until upload is finished
    next_action('editContentObjectIDIcon', 'wait')
    time.sleep(2)
    next_action('editContentObjectIDIcon', 'click')
    driver.switch_to.window(driver.window_handles[1])

    time.sleep(wait_time)
    next_action('contentModuleID', 'clear')
    next_action('contentModuleID', scorm_id)
    driver.find_element(By.NAME, 'applyChanges_bottom').click()

    driver.switch_to.window(driver.window_handles[0])

    driver.find_element(By.ID, 'schedButton').click()

    #email Notification
    if lms_send_mail == True:
        next_action('emailAddress', 'clear')
        next_action('emailAddress', email)
    else:
        next_action('emailNotificationEnabled', 'click')

    driver.find_element(By.ID, 'submitbutton').click()

    # Wait until Successfully Deployed
    time.sleep(wait_time)
    try:
        while True:
            deployment_status = driver.execute_script('''return document.querySelector('[id*="jobStatus"]').innerHTML''')
            if str(deployment_status) == 'Succeeded':
                break
            else:
                time.sleep(3)
                print(deployment_status)
        print("finished")
    except:
        print('Warning: Unable to read deployment status.')

    print(scorm_id)
    we.add_items_to_upload_sheet(os.path.dirname(file_path), scorm_id)

    if lms == 'lidl':
        driver.get(manage_assignments_url)
    elif lms == 'schwarz':
        driver.get(manage_assignments_url_s)

    # Manage User Learning - Form
    # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, 'studentNeedsForm')))

    time.sleep(wait_time)

    next_action('addCpnt', 'click')
    next_action('submitbutton', 'click')
    next_action('studentId', 'click')

    # Assign Testusers

    for user in testuser_list:
        next_action('studentId', user)
        next_action('submitbutton', 'click')
        time.sleep(2)

    next_action('nextButton', 'click')
    time.sleep(2)
    next_action('addOneCpntType', 'ELEARNING')
    next_action('id', scorm_id)
    time.sleep(2)
    next_action('submitbutton', 'click')
    time.sleep(2)
    next_action('nextButton', 'click')
    time.sleep(2)
    next_action('nextButton', 'click')
    time.sleep(2)
    next_action('runOnline', 'click')
    time.sleep(2)

    if lms == 'lidl':
        driver.get(startpage_url)
    elif lms == 'schwarz':
        driver.get(startpage_url_s)


def next_action(id, action):
    if action == 'click':
        driver.find_element(By.ID, id).click()
    elif action == 'wait':
        WebDriverWait(driver, 1200).until(EC.presence_of_element_located((By.ID, id)))
    elif action == 'clear':
        driver.find_element(By.ID, id).clear()
    else:
        driver.find_element(By.ID, id).send_keys(action)

def read_upload_sheet(path):
    print("report_path: ", path)
    upload_files = we.lms_upload_sheet(path)

    # check wich LMS System(s)
    if gui.checkbox_lidl_lms.get():
        initialize('lidl')
        for file in upload_files:
            start_upload(file, 'lidl')

    if gui.checkbox_schwarz_lms.get():
        initialize('schwarz')
        for file in upload_files:
            start_upload(file, 'schwarz')

    gui.clearLabels()
    gui.setLabelStatus('LMS-Upload succsessful!', '#00ff00')