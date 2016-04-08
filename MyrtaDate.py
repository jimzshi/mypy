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

class MyrtaDate:
    """ try to catch any available slot in one particular date """
    #from selenium.webdriver.common.keys import Keys
    pp = pprint.PrettyPrinter()
    candidates = []
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
            self.refresh_wait_time = self.config.getint("system", "refresh_wait_time")
            self.weekday_tri = self.config.get("system", "weekday_tri")
            self.weekdays_vec = str.split(self.weekday_tri, ',')

            self.log_file = os.path.join(self.root_dir, self.config.get("system", "log_file"))
            print(self.log_file)
            self.log_level = self.config.get("system", "log_level")
            logging.basicConfig(filename=self.log_file, filemode='w', level=logging.getLevelName(self.log_level), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.log = logging.getLogger('myrta')
    
            self.year = self.config.get("task", "year")
            self.month = self.config.get("task", "month")
            self.day = self.config.get("task", "day")
            self.time_slots = str.split(self.config.get("task", "time_slots"), ',')
            self.candidate_file = self.config.get("task", "candidate_file")
    
            self.log.info("read in myrta_homepage: %s" % self.myrta_homepage)
            self.log.info("read in email_address: %s" % self.email_address)
            self.log.info("read in phone_number: %s" % self.phone_number)
            self.log.info("read in action_wait_time: %d" % self.action_wait_time)
            self.log.info("read in session_wait_time: %d" % self.session_wait_time)
            self.log.info("read in weekdays_vec: %s" % self.weekdays_vec)
            self.log.info("read in log_file: %s" % self.log_file)
            self.log.info("read in log_level: %s" % self.log_level)
            self.log.info("read in candidate_file: %s" % self.candidate_file)
    
        except configparser.NoOptionError as e:
            self.log.error("Can't read in options: %s, exit." % e)
            sys.exit("Invalid Settings")

    def read_task(self):
        with open(self.candidate_file) as tf:
            candidate_reader = csv.reader(tf)
            for task_row in candidate_reader:
                if len(task_row)!=2:
                    err_msg = "[Warning]: task: %s has only %d fields - we need at least 2. this task will be ignored" % (task_row, len(task_row))
                    print("%s" % err_msg)
                    self.log.error(err_msg)
                    continue
                self.candidates.append(task_row)
        if(len(self.candidates) < 1):
            self.log.error("invalid task file, there're at least one candidate's info")
            sys.exit("Invalid Tasks")

    def _log_tasks(self):
        if( len(self.candidates) == 0 ):
            self.log.warn("NO task has been read in")
            return
        self.log.info("--------------------------------------------------------------------------------")
        self.log.info("Start to run tasks: %s" % self.candidates )
        for task in self.candidates:
            print ("Read Candidate: (%s, %s)" % (task[0], task[1]) )

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

    def _change_to_date(self):
        """ click 'change time' button, then switch to month according to config file """
        chgtime = self.driver.find_element_by_css_selector("[widgetid=changeTimeButton]")
        chgtime.click()
        time.sleep(self.action_wait_time)
        
        #Step 3: Change Date / Time
        self.log.info("choosing Year(%s), Month(%s) and Day(%s)" % (self.year, self.month, self.day))
        self.driver.find_element_by_css_selector("a.rms_calendarOpenBtn").click()
        time.sleep(self.action_wait_time)
                
        self.driver.find_element_by_css_selector("div.dijitCalendarMonthLabel.dijitCalendarCurrentMonthLabel").click()
        time.sleep(self.action_wait_time)
        self.driver.find_element_by_css_selector("#dijit_Calendar_0_mdd > div:nth-child(%s)" % self.month).click()
        time.sleep(self.action_wait_time)

        available_dates = self.driver.find_elements_by_css_selector("table#dijit_Calendar_0 > tbody td.dijitCalendarCurrentMonth")
        self.log.info("available days: %d", len(available_dates))
        found_day = False
        for current_day in available_dates:
            #self.log.info("check %s , %s" % (current_day.text, self.day))
            if current_day.text.strip() == self.day:
                found_day = True
                self.log.info("Found %s in %s" % (self.day, self.month))
                current_day.click()
                break
        if not found_day:
            self.log.warning("Can't find %s in %s, please have a double check. I will continue to do next task." % (self.day, self.month))
            time.sleep(self.action_wait_time)
            return False
        time.sleep(self.action_wait_time)

    def _book(self):
        weekday_index = datetime.date(int(self.year), int(self.month), int(self.day)).weekday()
        self.log.info("%s/%s/%s is %s, time slots: %s" % (self.day, self.month, self.year, self.weekdays_vec[weekday_index], self.time_slots))
        time_slot = None
        for self.timeslot in self.time_slots:
            ts_sel_str = "td#rms_%s_%s > a.available" % (self.weekdays_vec[weekday_index], self.timeslot)
            try:
                #self.log.info("selector is: %s", ts_sel_str)
                time_slot = self.driver.find_element_by_css_selector(ts_sel_str)
            except NoSuchElementException as e:
                #self.log.error("%s/%s/%s:%s is not available! continue with the next slot." %(self.year, self.month, self.day, self.timeslot))
                continue
        
        if(time_slot is None):
            return False        
            
        time_slot.click()
        time.sleep(self.action_wait_time)
        self.driver.find_element_by_css_selector("span#nextButton_label").click()
        time.sleep(self.action_wait_time)
        return True

    def _confirm(self, _task_id):
        """ Send confirmation letter """
        try:
            selNew_btn = self.driver.find_element_by_css_selector("input#rms_batCon-selNew")
            selNew_btn.click()
        except NoSuchElementException as e:
            self.log.warning("has no phone input, try to type-in new phone number. Error: %s" % e)
        self.driver.find_element_by_css_selector("input#widget_phoneNumber").send_keys(self.phone_number)
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
        self.log.info("task(%s, %s) finished, remove it from task list and begin to handle next one." % (self.candidates[_task_id][0], self.candidates[_task_id][1]))
        del self.candidates[_task_id]
        self.driver.quit()

    def run(self):
        while True:
            try:
                self._log_tasks();
                while len(self.candidates) > 0:
                    tasks_count = len(self.candidates)
                    self.log.info("%d tasks left" % tasks_count)
                    for task_id in range(tasks_count):
                        task_items = self.candidates[task_id]
                        self.log.info("handle task: %s, %s" % (task_items[0], task_items[1]))
                        self.log.info("wait for %d seconds to start a new session ..." % self.session_wait_time)
                        time.sleep(self.session_wait_time)
                        
                        self._open_homepage()
                        self._login(task_items)
                        self._change_to_date()
                        while(self._book() == False):
                            time.sleep(self.refresh_wait_time)
                            self.driver.refresh()

                        self._confirm(task_id)
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
    myrta = MyrtaDate(setting_file = 'settings2.ini')
    myrta.configure()
    myrta.read_task()
    myrta.run()