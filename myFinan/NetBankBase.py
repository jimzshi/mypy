from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import sys
import os
import configparser
import pprint
import logging
import csv
import datetime
import traceback
from cryptography.fernet import Fernet

class NetBankBase:
    """ a bridge class to retrieve info from NetBank """
    #from selenium.webdriver.common.keys import Keys
    pp = pprint.PrettyPrinter()

    def __init__(self, setting_file = "settings.ini"):
        if getattr(sys, 'frozen', False):
            # frozen
            self.root_dir = os.path.dirname(sys.executable)
        else:
            # unfrozen
            self.root_dir = os.path.dirname(os.path.realpath(__file__))

        self.settings_file = os.path.join(self.root_dir, setting_file)
        print(self.settings_file)

        self.config = configparser.ConfigParser()
        self.config.read(self.settings_file)
        self._key = b'fcymZAsm4INztFR2wb9ykdN4gnKK8VbHzKu_K5MDz8Y='
        self.cipher_suite = Fernet(self._key)

    def configure(self):
        try:
            self.homepage = self.config.get("general", "netbank_homepage")
            self.username = self.config.get("general", "username")
            self.password = self.cipher_suite.decrypt(str.encode(self.config.get("general", "password"))).decode()
    
            self.web_browser_name = str.lower(self.config.get("system", "web_browser_name"))
            self.action_wait_time = self.config.getint("system", "action_wait_time")
            self.session_wait_time = self.config.getint("system", "session_wait_time")
            self.restart_wait_time = self.config.getint("system", "restart_wait_time")

            self.log_file = os.path.join(self.root_dir, self.config.get("system", "log_file"))
            print(self.log_file)
            self.log_level = self.config.get("system", "log_level")
            logging.basicConfig(filename=self.log_file, filemode='w', level=logging.getLevelName(self.log_level), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.log = logging.getLogger('netbank')
    
            self.log.info("read in netbank_homepage: %s" % self.homepage)
            self.log.info("read in username: %s" % self.username)
            self.log.info("read in password: %s" % self.password)
            self.log.info("read in action_wait_time: %d" % self.action_wait_time)
            self.log.info("read in session_wait_time: %d" % self.session_wait_time)
    
        except configparser.NoOptionError as e:
            self.log.error("Can't read in options: %s, exit." % e)
            sys.exit("Invalid Settings")

    def _open_homepage(self):
        """Open Homepage and click "Manage booking" """
        if(self.web_browser_name == "ie"):
            self.driver = webdriver.Ie()
        elif(self.web_browser_name == "chrome"):
            option = webdriver.ChromeOptions()
            option.add_argument(r'user-data-dir=E:\local\etc\webdriver')
            self.driver = webdriver.Chrome(chrome_options=option)
        elif(self.web_browser_name == "ff"):
            self.driver = webdriver.Firefox()
                
        self.driver.maximize_window()
        self.driver.get(self.homepage)
        time.sleep(self.action_wait_time)

    def _login(self):
        """ Login. enter client number and password"""
        input_number = self.driver.find_element_by_css_selector('#txtMyClientNumber_field')
        input_number.clear()
        input_number.send_keys(self.username)
        input_pw = self.driver.find_element_by_css_selector("#txtMyPassword_field")
        input_pw.clear()
        input_pw.send_keys(self.password)
        time.sleep(self.action_wait_time)
        self.driver.find_element_by_id("btnLogon_field").click()
        time.sleep(self.action_wait_time)

    def _export_mastercard(self):
        """ select dates and export transactions for MasterCard Diamond account"""
        btn_master = self.driver.find_element_by_link_text("MasterCard Diamond")
        btn_master.click()
        time.sleep(self.action_wait_time)

        # press 'Advanced Search'
        self.driver.find_element_by_link_text('Advanced search').click()
        self.driver.find_element_by_css_selector('#ctl00_BodyPlaceHolder_radioSwitchDateRange_field_1_label').click()
        input_from = self.driver.find_element_by_css_selector('#ctl00_BodyPlaceHolder_fromCalTxtBox_field')
        input_from.clear()
        input_from.send_keys('01/10/2016')
        input_to = self.driver.find_element_by_css_selector('#ctl00_BodyPlaceHolder_toCalTxtBox_field')
        input_to.clear()
        input_to.send_keys('01/11/2016')
        btn_search = self.driver.find_element_by_css_selector('#ctl00_BodyPlaceHolder_lbSearch > strong')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn_search)
        time.sleep(self.action_wait_time)
        btn_search.click()
        time.sleep(self.action_wait_time)

        # export to csv
        #self.driver.find_element_by_css_selector('#ctl00_CustomFooterContentPlaceHolder_updatePanelExport1 > div > a').click()
        self.driver.find_element_by_link_text('Export').click()
        time.sleep(self.action_wait_time)
        self.driver.find_element_by_css_selector('#ctl00_CustomFooterContentPlaceHolder_updatePanelExport1 > div > div > fieldset > div.FieldGroup > div.FieldWrapper.Width19 > div > div.FieldElement > span > span > span.icon.ddl_selected').click()
        time.sleep(self.action_wait_time)
        self.driver.find_element_by_partial_link_text('Excel').click()
        time.sleep(self.action_wait_time)
        self.driver.find_element_by_css_selector('#ctl00_CustomFooterContentPlaceHolder_lbExport1').click()



if __name__ == '__main__':
    netbank = NetBankBase()
    netbank.configure()
    netbank._open_homepage()
    netbank._login()
    netbank._export_mastercard()
