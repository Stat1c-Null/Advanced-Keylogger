# Advanced-Keylogger
Advanced Python Keylogger that records every key pressed by user on the keyboard and takes screenshots, after which it emails it to us.
How to make it work
Step 1: Make sure to install all of the imported libraries. Command: pip install `name of library`. Libraries: smtplib, threading, pyautogui, PIL, functools)
Step 2: Change email to your email in EMAIL field. Make sure you have 2 factor authentication
Step 3: go to your google account profile, security settings, and generate app password, and replace it in PASS field
Step 4: pip3 install pyinstaller | pyinstaller --onefile -w 'filename.py' - to create exe file
Step 5: in dist folder create folders called 'Keylogs' and 'Screenshots'
Step 6: To add a program to startup, Press Windows+R to open the “Run” dialog box. Type “shell:startup” and then hit Enter to open the “Startup” folder. Create a shortcut in the “Startup” folder to any file, folder, or program's executable file. It will open on startup the next time you boot.

TODO: 

1.Allow keylogger to record texts on foreign languages such as Russian
2.Record mouse clicks and take screenshots on mouse click

