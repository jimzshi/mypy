from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import sys
import os
import ConfigParser
import pprint
import string
import logging
import csv
import datetime
import traceback

#from selenium.webdriver.common.keys import Keys
pp = pprint.PrettyPrinter()

if getattr(sys, 'frozen', False):
    # frozen
    root_dir = os.path.dirname(sys.executable)
else:
    # unfrozen
    root_dir = os.path.dirname(os.path.realpath(__file__))
    
settings_file = os.path.join(root_dir, "settings.ini")
print settings_file

config = ConfigParser.ConfigParser()
config.read(settings_file)

try:
    myrta_homepage = config.get("general", "myrta_homepage")
    email_address = config.get("general", "email_address")
    phone_number = config.get("general", "phone_number")
    
    action_wait_time = config.getint("system", "action_wait_time")
    session_wait_time = config.getint("system", "session_wait_time")
    restart_wait_time = config.getint("system", "restart_wait_time")
    weekday_tri = config.get("system", "weekday_tri")
    weekdays_vec = string.split(weekday_tri, ',')
#     pp.pprint(weekdays_vec)
    log_file = os.path.join(root_dir, config.get("system", "log_file"))
    print log_file
    log_level = config.get("system", "log_level")
    logging.basicConfig(filename=log_file, filemode='w', level=logging._levelNames.get(log_level), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log = logging.getLogger('myrta')
    
    task_file = config.get("task", "task_file")
    
    log.info("read in myrta_homepage: %s" % myrta_homepage)
    log.info("read in email_address: %s" % email_address)
    log.info("read in phone_number: %s" % phone_number)
    log.info("read in action_wait_time: %d" % action_wait_time)
    log.info("read in session_wait_time: %d" % session_wait_time)
    log.info("read in weekdays_vec: %s" % weekdays_vec)
    log.info("read in log_file: %s" % log_file)
    log.info("read in log_level: %s" % log_level)
    log.info("read in task_file: %s" % task_file)
    
except ConfigParser.NoOptionError as e:
    log.error("Can't read in options: %s, exit." % e)
    sys.exit("Invalid Settings")


tasks = []
print
with open(task_file, 'rb') as tf:
    task_reader = csv.reader(tf)
    for task_row in task_reader:
        if len(task_row)<6:
            err_msg = "[Warning]: task: %s has only %d fields - we need at least 6. this task will be ignored" % (task_row, len(task_row))
            print "%s" % err_msg
            log.error(err_msg)
            continue
        tasks.append(task_row)

while True:
    try:
        log.info("--------------------------------------------------------------------------------")
        log.info("Start to run tasks: %s" % tasks )
        for task in tasks:
            print "Read Task: (%s, %s) wants %s/%s/%s %s" % (task[0], task[1], task[2], task[3], task[4], task[5])

        #while False:
        while len(tasks) > 0:
            tasks_count = len(tasks)
            log.info("%d tasks left" % tasks_count)
            for task_id in range(tasks_count):
                task_items = tasks[task_id]
                log.info("handle task: %s, %s" % (task_items[0], task_items[1]))
                log.info("wait for %d seconds to start a new session ..." % session_wait_time)
                time.sleep(session_wait_time)
                #Homppage
                driver = webdriver.Firefox()
                #driver = webdriver.Chrome(port=9515)
                #driver = webdriver.Ie()
                driver.maximize_window()
                driver.get(myrta_homepage)
                time.sleep(action_wait_time)
                booking_btn = driver.find_element_by_link_text('Manage booking');
                booking_btn.click();
                time.sleep(action_wait_time)
        
                input_bookid = driver.find_element_by_css_selector('input#widget_input_bookingId')
                input_bookid.clear()
                input_bookid.send_keys(task_items[0])
                input_familyname = driver.find_element_by_css_selector("input#widget_input_familyName")
                input_familyname.clear()
                input_familyname.send_keys(task_items[1])
                time.sleep(action_wait_time)
                driver.find_element_by_id("submitNoLogin_label").click()
                time.sleep(action_wait_time)
        
                #Step 1: View Booking
                chgtime = driver.find_element_by_id('changeTimeButton_label')
                chgtime.click()
                time.sleep(action_wait_time)
        
                #Step 3: Change Date / Time
                year = string.strip(task_items[2])
                month = string.strip(task_items[3])
                day = string.strip(task_items[4])
                timeslot = string.strip(task_items[5])
                log.info("choosing Year(%s), Month(%s) and Day(%s) at Timeslot(%s)" % (year, month, day, timeslot))
                driver.find_element_by_css_selector("a.rms_calendarOpenBtn").click()
                time.sleep(action_wait_time)
                #Next 2 month, trick for 'next year'
                #driver.find_element_by_css_selector("img.dijitCalendarIncrementControl.dijitCalendarIncrease").click()
                #time.sleep(action_wait_time)
                #driver.find_element_by_css_selector("img.dijitCalendarIncrementControl.dijitCalendarIncrease").click()
                #time.sleep(action_wait_time)
                
                driver.find_element_by_css_selector("div.dijitCalendarMonthLabel.dijitCalendarCurrentMonthLabel").click()
                time.sleep(action_wait_time)
                driver.find_element_by_css_selector("#dijit_Calendar_0_mdd > div:nth-child(%s)" % month).click()
                time.sleep(action_wait_time)
                available_dates = driver.find_elements_by_css_selector("table#dijit_Calendar_0 > tbody td.dijitCalendarCurrentMonth")
                log.info("available days: %d", len(available_dates))
                found_day = False
                for current_day in available_dates:
                    if current_day.text.strip() == day:
                        found_day = True
                        log.info("Found %s in %s" % (day, month))
                        current_day.click()
                        break
                if not found_day:
                    log.warning("Can't find %s in %s, please have a double check. I will continue to do next task." % (day, month))
                    time.sleep(action_wait_time)
                    driver.close()
                    continue
                time.sleep(action_wait_time)

                try:
                    weekday_index = datetime.date(int(year), int(month), int(day)).weekday()
                    log.info("%s/%s/%s is %s" % (day, month, year, weekdays_vec[weekday_index]))
                    ts_sel_str = "td#rms_%s_%s > a.available" % (weekdays_vec[weekday_index], timeslot)
                    log.info("selector is: %s", ts_sel_str)
                    time_slot = driver.find_element_by_css_selector(ts_sel_str)
                except NoSuchElementException as e:
                    log.error("This time is not available! continue with the next task.")
                    time.sleep(action_wait_time)
                    driver.close()
                    continue
            
                time_slot.click()
                time.sleep(action_wait_time)
                driver.find_element_by_css_selector("span#nextButton_label").click()
                time.sleep(action_wait_time)
        
                #Step 4: confirm
                try:
                    selNew_btn = driver.find_element_by_css_selector("input#rms_batCon-selNew")
                    selNew_btn.click()
                except NoSuchElementException as e:
                    log.warning("has no phone input, try to type-in new phone number. Error: %s" % e)
                driver.find_element_by_css_selector("input#widget_phoneNumber").send_keys(phone_number)
                driver.find_element_by_css_selector("input#checkTerms").click()
                time.sleep(action_wait_time)
                driver.find_element_by_css_selector("span#nextButton_label").click()
                time.sleep(action_wait_time)
        
                #Finish
                driver.find_element_by_css_selector("input#widget_inputEmail").send_keys("jim.z.shi@gmail.com")
                time.sleep(action_wait_time)
                driver.find_element_by_css_selector("span#emailButton").click()
                time.sleep(action_wait_time)
                driver.find_element_by_css_selector("input#widget_inputEmail").send_keys(email_address)
                time.sleep(action_wait_time)
                driver.find_element_by_css_selector("span#emailButton").click()
        
                log.info("task(%s, %s) finished, remove it from task list and begin to handle next one." % (task_items[0], task_items[1]))
                del tasks[task_id]
                driver.close()
                break
    except KeyboardInterrupt as error:
        msg = "User's keyboard interruption detected. Immediate quit without restart."
        print "\n", '-'*60
        print msg
        print '-'*60, "\n"
        log.error(msg)
        break
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "\n", '-'*60
        print "Exception: %s" % exc_type
        for msg in traceback.format_exception(exc_type, exc_value, exc_traceback):
            log.error(msg)
        rst_msg = "Exception caught, try to recover from the disaster. waiting %d seconds to restart ..." % restart_wait_time
        print rst_msg
        log.error(rst_msg)
        print '-'*60, "\n"
        if driver is not None:
            try:
                driver.close()
            except:
                pass
        for sec in range(restart_wait_time):
            time.sleep(1)
            sys.stdout.write('=')
        sys.stdout.write(">>>")
        print "\nNow I will try to restart the tasks ..."
        continue

    break

print "\nPress any key to quit ... "
c = sys.stdin.read(1)



# continue_btn = driver.find_element_by_id('submitNoLogin_label')
# if continue_btn is None:
#     print "Error"
# if continue_btn.is_enabled():
#     bgcolor = continue_btn.value_of_css_property('color');
#     print "Not Enabled: ", bgcolor.red, " ", bgcolor.green, " ", bgcolor.blue
#     time.sleep(10)
# continue_btn.click()
# time.sleep(action_wait_time)
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source

