import mechanicalsoup
import paramiko
import time

##Aircon Login Credentials
username = "username"
password = "password"
webpage= "http://192.168.9.8"

##Open Aircon Webpage and login

browser = mechanicalsoup.StatefulBrowser(
    soup_config={'features': 'lxml'},
    raise_on_404=True,
    user_agent='MyBot/0.1: mysite.example.com/bot_info',
)

browser.open(webpage)
print("web page opened, the url is:" + browser.url)
browser.select_form() # there is just one form, no need to select
browser["login_username"] = username
browser["login_password"] = password
resp = browser.submit_selected()


## verify we are now logged in

page = browser.page
messages = page.find("div", class_="app-secondary-name")
if messages:
        print ("login successful, the new url is: " + browser.url)

# check the alarm-icon-section division
        alarmcount = page.find("div", id="alarm-icon-section")
        if alarmcount:
                alarmtext=str(alarmcount)
                total_alarms= alarmtext.split('title="')[-1].split("present")[0]
                print (total_alarms)
                if int(total_alarms[0]) > 0:
                        ###
                        #A function to record output to a file when printing to screen also
                        timestr = time.strftime("%Y%m%d-%H%M%S")
                        outputfile= "aircon_critical_alarm.txt"
                        OF = open(outputfile, 'a')

                        def printing(text):
                                print (str(text))
                                if outputfile:
                                        OF.write(text + "\n")
                        ###
                        printing ("-------"+timestr+" "+webpage+"-------")
                        printing (str(total_alarms))
                        browser.select_form('form[name="HashForm1"]')
                        browser.form.set("ClearActiveAlarms",True)
                        print ("--The form values below selected, checkbox tick--")
                        browser.form.print_summary()
                        resp = browser.submit_selected()
                        printing("Alarms Cleared")
