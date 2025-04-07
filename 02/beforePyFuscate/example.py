import ctypes
import time
import winsound
import os
import subprocess

time.sleep(60)

# Create the ransom note file
ransom_note_content = """>> What happened?
Important files on your network was ENCRYPTED and now they have "wragz12" extension. In order to recover your files you need to follow instructions below.
>> Sensitive Data
Sensitive data on your network was DOWNLOADED.
If you DON'T WANT your sensitive data to be PUBLISHED you have to act quickly.
Data includes:
Employees personal data, CVs, DL, SSN.
Complete network map including credentials for local and remote services.
Private financial information including: clients data, bills, budgets, annual reports, bank statements.
Manufacturing documents including: datagrams, schemas, drawings in solidworks format And more...
Samples are available on your User Panel.
>> CAUTION
DO NOT MODIFY ENCRYPTED FILES YOURSELF.
DO NOT USE THIRD PARTY SOFTWARE TO RESTORE YOUR DATA.
YOU MAY DAMAGE YOUR FILES, IT WILL RESULT IN PERMANENT DATA LOSS.
>> What should I do next?
1) Download and install Tor Browser from: https://torproject.org/"""

note_filename = "RECOVER-wragz12-FILES.txt"
with open(note_filename, "w") as f:
    f.write(ransom_note_content)

# Show first alert
alert1_title = "CRITICAL SYSTEM ALERT"
alert1_text = """
WARNING: Your system has been compromised !
YOUR FILES HAVE BEEN ENCRYPTED! 
by Black Cat ransomware
"""
winsound.Beep(1500, 500)
ctypes.windll.user32.MessageBoxW(0, alert1_text, alert1_title, 0x10)
time.sleep(3)

# Show second alert
alert2_title = "CRITICAL SYSTEM ALERT"
alert2_text = """
WARNING: You have been hacked!
We have cleared all logs
"""
winsound.Beep(1000, 1000)
ctypes.windll.user32.MessageBoxW(0, alert2_text, alert2_title, 0x30)

# Open the ransom note file after alerts
try:
    if os.name == 'nt':  # Windows
        os.startfile(note_filename)
except Exception as e:
    # Fallback if automatic opening fails
    alert3_title = "INSTRUCTIONS"
    alert3_text = f"Please open the file '{note_filename}' for recovery instructions"
    ctypes.windll.user32.MessageBoxW(0, alert3_text, alert3_title, 0x40)