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

class MyrtaBase:
    """ try to catch any available slot in one particular date """
    #from selenium.webdriver.common.keys import Keys
    pp = pprint.PrettyPrinter()
    tasks = []
    driver = None

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

    def configure(self):
        try:
            self.myrta_homepage = self.config.get("general", "myrta_homepage")
            self.email_address = self.config.get("general", "email_address")
            self.phone_number = self.config.get("general", "phone_number")
    
            self.web_browser_name = str.lower(self.config.get("system", "web_browser_name"))
            self.action_wait_time = self.config.getint("system", "action_wait_time")
            self.session_wait_time = self.config.getint("system", "session_wait_time")
            self.restart_wait_time = self.config.getint("system", "restart_wait_time")
            self.weekday_tri = self.config.get("system", "weekday_tri")
            self.weekdays_vec = str.split(self.weekday_tri, ',')

            self.log_file = os.path.join(self.root_dir, self.config.get("system", "log_file"))
            print(self.log_file)
            self.log_level = self.config.get("system", "log_level")
            logging.basicConfig(filename=self.log_file, filemode='w', level=logging.getLevelName(self.log_level), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.log = logging.getLogger('myrta')
    
            self.task_file = self.config.get("task", "task_file")
    
            self.log.info("read in myrta_homepage: %s" % self.myrta_homepage)
            self.log.info("read in email_address: %s" % self.email_address)
            self.log.info("read in phone_number: %s" % self.phone_number)
            self.log.info("read in action_wait_time: %d" % self.action_wait_time)
            self.log.info("read in session_wait_time: %d" % self.session_wait_time)
            self.log.info("read in weekdays_vec: %s" % self.weekdays_vec)
            self.log.info("read in log_file: %s" % self.log_file)
            self.log.info("read in log_level: %s" % self.log_level)
            self.log.info("read in task_file: %s" % self.task_file)
    
        except configparser.NoOptionError as e:
            self.log.error("Can't read in options: %s, exit." % e)
            sys.exit("Invalid Settings")

    def read_task(self):
        with open(self.task_file) as tf:
            task_reader = csv.reader(tf)
            for task_row in task_reader:
                if len(task_row)<6:
                    err_msg = "[Warning]: task: %s has only %d fields - we need at least 6. this task will be ignored" % (task_row, len(task_row))
                    print("%s" % err_msg)
                    self.log.error(err_msg)
                    continue
                self.tasks.append(task_row)

    def _log_tasks(self):
        if( len(self.tasks) == 0 ):
            self.log.warn("NO task has been read in")
            return
        self.log.info("--------------------------------------------------------------------------------")
        self.log.info("Start to run tasks: %s" % self.tasks )
        for task in self.tasks:
            print ("Read Task: (%s, %s) wants %s/%s/%s %s" % (task[0], task[1], task[2], task[3], task[4], task[5]) )

    def _open_homepage(self):
        """Open Homepage and click "Manage booking" """
        if(self.web_browser_name == "ie"):
            self.driver = webdriver.Ie()
        elif(self.web_browser_name == "chrome"):
            self.driver = webdriver.Chrome()
        elif(self.web_browser_name == "ff"):
            self.driver = webdriver.Firefox()
                
        self.driver.maximize_window()
        self.driver.get(self.myrta_homepage)
        time.sleep(self.action_wait_time)
        booking_btn = self.driver.find_element_by_link_text('Manage booking');
        booking_btn.click();
        time.sleep(self.action_wait_time)

    def _login(self, _task):
        """ Login. enter id and family name """
        input_bookid = self.driver.find_element_by_css_selector('input#widget_input_bookingId')
        input_bookid.clear()
        input_bookid.send_keys(_task[0])
        input_familyname = self.driver.find_element_by_css_selector("input#widget_input_familyName")
        input_familyname.clear()
        input_familyname.send_keys(_task[1])
        time.sleep(self.action_wait_time)
        self.driver.find_element_by_id("submitNoLogin_label").click()
        time.sleep(self.action_wait_time)

    def _change_to_month(self, _task):
        """ click 'change time' button, then switch to month according to config file """
        chgtime = self.driver.find_element_by_css_selector("[widgetid=changeTimeButton]")
        chgtime.click()
        time.sleep(self.action_wait_time)
        
        #Step 3: Change Date / Time
        self.year = str.strip(_task[2])
        self.month = str.strip(_task[3])
        self.day = str.strip(_task[4])
        self.timeslot = str.strip(_task[5])
        self.log.info("choosing Year(%s), Month(%s) and Day(%s) at Timeslot(%s)" % (self.year, self.month, self.day, self.timeslot))
        self.driver.find_element_by_css_selector("a.rms_calendarOpenBtn").click()
        time.sleep(self.action_wait_time)
        #Next 2 month, trick for 'next year'
        #driver.find_element_by_css_selector("img.dijitCalendarIncrementControl.dijitCalendarIncrease").click()
        #time.sleep(action_wait_time)
        #driver.find_element_by_css_selector("img.dijitCalendarIncrementControl.dijitCalendarIncrease").click()
        #time.sleep(action_wait_time)
                
        self.driver.find_element_by_css_selector("div.dijitCalendarMonthLabel.dijitCalendarCurrentMonthLabel").click()
        time.sleep(self.action_wait_time)
        self.driver.find_element_by_css_selector("#dijit_Calendar_0_mdd > div:nth-child(%s)" % self.month).click()
        time.sleep(self.action_wait_time)

    def _book(self):
        available_dates = self.driver.find_elements_by_css_selector("table#dijit_Calendar_0 > tbody td.dijitCalendarCurrentMonth")
        self.log.info("available days: %d", len(available_dates))
        found_day = False
        for current_day in available_dates:
            if current_day.text.strip() == self.day:
                found_day = True
                self.log.info("Found %s in %s" % (self.day, self.month))
                current_day.click()
                break
        if not found_day:
            self.log.warning("Can't find %s in %s, please have a double check. I will continue to do next task." % (self.day, self.month))
            time.sleep(self.action_wait_time)
            self.driver.quit()
            return False
        time.sleep(self.action_wait_time)

        try:
            weekday_index = datetime.date(int(self.year), int(self.month), int(self.day)).weekday()
            self.log.info("%s/%s/%s is %s" % (self.day, self.month, self.year, self.weekdays_vec[weekday_index]))
            ts_sel_str = "td#rms_%s_%s > a.available" % (self.weekdays_vec[weekday_index], self.timeslot)
            self.log.info("selector is: %s", ts_sel_str)
            time_slot = self.driver.find_element_by_css_selector(ts_sel_str)
        except NoSuchElementException as e:
            self.log.error("This time is not available! continue with the next task.")
            time.sleep(self.action_wait_time)
            self.driver.quit()
            return False
            
        time_slot.click()
        time.sleep(self.action_wait_time)
        self.driver.find_element_by_css_selector("span#nextButton_label").click()
        time.sleep(self.action_wait_time)
        return True

    def _confirm(self):
        """ Send confirmation letter """
        try:
            selNew_btn = self.driver.find_element_by_css_selector("input#rms_batCon-selNew")
            selNew_btn.click()
        except NoSuchElementException as e:
            self.log.warning("has no phone input, try to type-in new phone number. Error: %s" % e)
        self.driver.find_element_by_css_selector("input#widget_phoneNumber").send_keys(phone_number)
        self.driver.find_element_by_css_selector("input#checkTerms").click()
        time.sleep(self.action_wait_time)
        self.driver.find_element_by_css_selector("span#nextButton_label").click()
        time.sleep(self.action_wait_time)
        
        #Finish
        self.driver.find_element_by_css_selector("input#widget_inputEmail").send_keys("jim.z.shi@gmail.com")
        time.sleep(self.action_wait_time)
        self.driver.find_element_by_css_selector("span#emailButton").click()
        time.sleep(self.action_wait_time)
        self.driver.find_element_by_css_selector("input#widget_inputEmail").send_keys(self.email_address)
        time.sleep(self.action_wait_time)
        self.driver.find_element_by_css_selector("span#emailButton").click()
        time.sleep(2)
        log.info("task(%s, %s) finished, remove it from task list and begin to handle next one." % (task_items[0], task_items[1]))
        del self.tasks[task_id]
        self.driver.quit()

    def run(self):
        while True:
            try:
                self._log_tasks();
                while len(self.tasks) > 0:
                    tasks_count = len(self.tasks)
                    self.log.info("%d tasks left" % tasks_count)
                    for task_id in range(tasks_count):
                        task_items = self.tasks[task_id]
                        self.log.info("handle task: %s, %s" % (task_items[0], task_items[1]))
                        self.log.info("wait for %d seconds to start a new session ..." % self.session_wait_time)
                        time.sleep(self.session_wait_time)
                        
                        self._open_homepage()
                        self._login(task_items)
                        self._change_to_month(task_items)
                        if(self._book() == False):
                            continue

                        self._confirm()
                        break
                    print ("try next round of tasks ...")
            except KeyboardInterrupt as error:
                msg = "User's keyboard interruption detected. Immediate quit without restart."
                print ("\n", '-'*60)
                print (msg)
                print ('-'*60, "\n")
                self.log.error(msg)
                break
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print ("\n", '-'*60)
                print ("Exception: %s" % exc_type)
                for msg in traceback.format_exception(exc_type, exc_value, exc_traceback):
                    self.log.error(msg)
                rst_msg = "Exception caught, try to recover from the disaster. waiting %d seconds to restart ..." % self.restart_wait_time
                print (rst_msg)
                self.log.error(rst_msg)
                print ('-'*60, "\n")
                if self.driver is not None:
                    try:
                        driver.quit()
                    except:
                        pass
                for sec in range(self.restart_wait_time):
                    time.sleep(1)
                    sys.stdout.write('=')
                sys.stdout.write(">>>")
                print ("\nNow I will try to restart the tasks ...")
                continue

            break #  while True:
            print ("\nPress any key to quit ... ")
            c = sys.stdin.read(1)

if __name__ == '__main__':
    myrta = MyrtaBase()
    myrta.configure()
    myrta.read_task()
    myrta.run()