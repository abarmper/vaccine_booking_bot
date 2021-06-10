
'''
This code can be used for automated vaccine booking. If you want to be the first, this is the way!
Just fill your credentials below and the python program will take care things for you. You just have
the last word (by accepting the vaccine).

IMPORTANT: this code performs in an automated way all but the last step! So... don't worry.
When in the last step, the vaccine vacancy is "blocked" so that no other person can take it
(at least for 2 minutes). So, making the last step non-automated is not e problem.

This code is for the ages 18-29. In these ages, Astra Zeneca Vaccine is not admissioned. 
Consequently, the code dose not check that. It only checks NOT to select a single-dose vaccine.
In other words, it avoids single dose vaccines (like Johnson) and accepts all the double dose vaccines.
If you want to aply this algorithm in a larger age group where Astra Zeneca is allowd and you want to avoid
Astra Zeneca too, you will have to amend the code and check the date stamps. If the two apointments are
less than 50 days apart, then it is most probably not the Astra Zeneca and you are ok.

The code requires to have been loged in manually for at least one time in the past. 
(Because, the first time you ever log in it is a little different.)

REQUIREMENTS:
python3
pip3 (google search: "install python 3 and pip")
selenium (pip3 install selenium)

USAGE:
python3 auto.py
OR
python3 auto.py 3 0
OR GENERALY
python3 auto.py arg1 arg2

The first argument "arg" ("3" above) determins the prefered date and time of the first and second apointment in the following fassion:
day = arg1 div 4
time = arg1 mod 4
ALL THESE PROVIDED THAT EVERY SLOT IS AVAILABLE

The second argument determins the vaccination senter from which to begin searching.

WHAT THE CODE DOES
The code logins and then checks for vacances. If it finds a vacancy, checks if that vacancy is sigle dose. 
If it is, returns and changes vaccination center to check again. If it scans throw all the vaccination centers and no
double dose vacancy is found, then it repeats and cycles throw all the vaccination centers for the given zip code, again.
This is usefull because one can let the program run before the new vacances for the double dose vaccines open so as as soon
as they become available, the script will automatically reserve one for you to press the final submit button.

Be sure to change the SLEEP_TIME according to your internet connection. You can test the code before to be sure it's ok.
SLEEP_TIME of 2 seconds should be ok for urban internet speeds.
'''

import selenium as se
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

if len(sys.argv) > 1:
    BOOK_NUMBER = int(sys.argv[1])
else:
    BOOK_NUMBER = 0

if len(sys.argv) > 2:
    # Second argument can be the index of the dropdown list (vaccination center order).
    BEGIN_AT_INDEX = int(sys.argv[2])
else:
    BEGIN_AT_INDEX = 0
    

AMKA = "XXXXXXXXXX" # add your AMKA inside the quotes
EPONYMO = "XXXXXXXXXX" # dd your surname inside the quotes in capital greek letters
taxisnet_username = "XXXXXXXXXX" # add your AMKA inside the quotes
taxisnet_password = "XXXXXXXXXX" # dd your surname inside the quotes
SLEEP_TIME = 3 # Adjust it according to your internet connection speed


def try_again(f, arg):
    bt = []
    while bt ==[]:
        try:
            bt = f(arg)
        except se.common.exceptions.ElementClickInterceptedException:
            continue
        except se.common.exceptions.NoSuchElementException:
            continue
    return bt

def try_again_xpath_timer(xpath, secs):
    res = None
    try:    
        res = WebDriverWait(driver, secs).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    except se.common.exceptions.TimeoutException:
        pass
    except se.common.exceptions.ElementClickInterceptedException:
        pass
    return res

if __name__== '__main__':

    driver = webdriver.Firefox()
    # Open the website.
    driver.get('https://emvolio.gov.gr/eligibility')
    sleep(SLEEP_TIME)
    # Scroll to the bottom.
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
    # Find and fill AMKA form.
    AMKA_form = try_again(driver.find_element_by_xpath,'//input[@id="edit-amka"]')
    AMKA_form.send_keys(AMKA)
    try_again(driver.find_element_by_xpath,'//input[@id="edit-validation-method-lastname"]').click()
    EPONIMO_form = try_again(driver.find_element_by_xpath,'//*[@id="edit-value2"]')
    EPONIMO_form.send_keys(EPONYMO)
    driver.find_element_by_xpath('//button[@id="submit-form"]').click()

    # Next page.
    try_again(driver.find_element_by_xpath,'//a[@class="btn btn-success"]').click()

    # Taxis net authentication page.
    #sleep(SLEEP_TIME)
    XRHSTHS_form = try_again(driver.find_element_by_xpath,'//input[@id="v"]')
    XRHSTHS_form.send_keys(taxisnet_username)
    password_form = try_again(driver.find_element_by_xpath,'//input[@id="j_password"]')
    password_form.send_keys(taxisnet_password)
    try_again(driver.find_element_by_xpath,'//button[@id="btn-login-submit"]').click()

    # Next page: agree to give information.
    #sleep(SLEEP_TIME)
    try_again(driver.find_element_by_xpath,'//button[@id="btn-submit"]').click()

    button = try_again(driver.find_element_by_xpath,'//button[@class="btn btn-primary boundMd boundBtMobile appointmentSearch"]')
    driver.execute_script("arguments[0].click();", button)


    # Next page: booking 1st dose.

   
    #sleep(SLEEP_TIME)
    # Loop to find a vaccination center that has 2 doses.
    index=BEGIN_AT_INDEX
    li2 = None
    found2dose = False
    while not found2dose:
        #sleep(SLEEP_TIME) # Add sleep times if not working.
        li1 = driver.find_elements_by_xpath('//*[@data-doses="2"]') # Set 1 if you want johnson & Johnson or set 2 for the rest.
        if li1 != []: # If there are vacances in this vaccination center, check for second dose.
            driver.execute_script("arguments[0].click();", li1[BOOK_NUMBER]) # If you set 1, the code below is not needeed
            sleep(SLEEP_TIME)
            li2 = driver.find_elements_by_xpath('//*[@data-doses="undefined"]')
            if li2 != None:
                found2dose = True
                break
            # single dose vaccine, go back to change vaccination center to get a double-dose
            try_again(driver.find_element_by_xpath,'//button[@data-bind="click: backToSelect"]').click()
        
        # Dropdown menu (change choice).
        index+=1 # increment index. Of course this will break when index out of range and the program will hault.
        sleep(SLEEP_TIME)
        try_again(driver.find_element_by_xpath,'//*[@class="k-widget k-dropdown" and @style="width: 250px; flex-grow: 1;"]').click()
        list_item = try_again_xpath_timer(f'//ul[@class="k-list k-reset"]//li[@data-offset-index="{str(index)}"]', SLEEP_TIME)
        if list_item != None:
            list_item.click()  
        else: 
            index=0
            try_again_xpath_timer(f'//ul[@class="k-list k-reset"]//li[@data-offset-index="{str(index)}"]', SLEEP_TIME).click()
        #sleep(2)
    
    # Next page: booking 2nd dose.
    if found2dose:
        driver.execute_script("arguments[0].click();", li2[BOOK_NUMBER]) # If you set 1, the code below is not needeed
    else:
        print("Nothing Found in this post code.")
    # After this stage, the vacancy is locked so there is no need to rush. You can proceed manually for the final booking.
    # Cool way below to check if second dose vaccine is selected (but I don't know for sure how the UI will be when 2 dose vaccines are open).
    # //*[@class='bs-stepper-label' and starts-with(text(),'2η')]
