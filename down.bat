@echo off
curl -s -L -o show.bat https://raw.githubusercontent.com/LilMok/RustDesk-Windows-Github-RDP/refs/heads/main/show.bat
curl -s -L -o loop.bat https://raw.githubusercontent.com/LilMok/RustDesk-Windows-Github-RDP/refs/heads/main/loop.bat
curl -s -L -o loop.py https://raw.githubusercontent.com/LilMok/RustDesk-Windows-Github-RDP/refs/heads/main/loop.py

:: Fetch latest RustDesk version tag
powershell -Command "$latest = (Invoke-WebRequest -Uri 'https://api.github.com/repos/rustdesk/rustdesk/releases/latest' -UseBasicParsing).Content | ConvertFrom-Json | Select-Object -ExpandProperty tag_name; echo $latest > latest_tag.txt"
set /p LATEST_TAG=<latest_tag.txt
del latest_tag.txt

:: Download the latest 64-bit EXE
curl -s -L -o rustdesk.exe https://github.com/rustdesk/rustdesk/releases/download/%LATEST_TAG%/rustdesk-%LATEST_TAG%-x86_64.exe

:: Install silently
rustdesk.exe --silent-install

set PASSWORD=LilMok123
set RUSTDESK_PATH="C:\Program Files\RustDesk\rustdesk.exe"

%RUSTDESK_PATH% --password %PASSWORD%

for /f "tokens=*" %%i in ('%RUSTDESK_PATH% --get-id') do set ID=%%i
echo RustDesk ID: %ID%
echo RustDesk Password: %PASSWORD%

%RUSTDESK_PATH% --install-service
net start rustdesk

echo echo RustDesk ID: %ID% >> show.bat
echo echo RustDesk Password: %PASSWORD% >> show.bat

powershell -Command "Invoke-WebRequest 'https://github.com/chieunhatnang/VM-QuickConfig/releases/download/1.6.1/VMQuickConfig.exe' -OutFile 'C:\Users\Public\Desktop\VMQuickConfig.exe'"

python.exe -m pip install --upgrade pip
pip install requests --quiet
pip install pyautogui --quiet
pip install psutil --quiet

del /f "C:\Users\Public\Desktop\Epic Games Launcher.lnk" >nul 2>&1
del /f "C:\Users\Public\Desktop\Unity Hub.lnk" >nul 2>&1

net user runneradmin LilMok@123
