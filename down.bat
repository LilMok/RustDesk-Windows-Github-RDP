@echo off
curl -s -L -o show.bat https://raw.githubusercontent.com/LilMok/RustDesk-Windows-Github-RDP/refs/heads/main/show.bat
curl -s -L -o loop.bat https://raw.githubusercontent.com/LilMok/RustDesk-Windows-Github-RDP/refs/heads/main/loop.bat
curl -s -L -o rustdesk.exe https://github.com/rustdesk/rustdesk/releases/latest/download/rustdesk.exe
rustdesk.exe --silent-install
set PASSWORD=LilMok123
"C:\Program Files\RustDesk\rustdesk.exe" --password %PASSWORD%
for /f "tokens=*" %%i in ('"C:\Program Files\RustDesk\rustdesk.exe" --get-id') do set ID=%%i
echo RustDesk ID: %ID%
echo RustDesk Password: %PASSWORD%
"C:\Program Files\RustDesk\rustdesk.exe" --install-service
net start "RustDesk Service"
echo echo RustDesk ID: %ID% >> show.bat
echo echo RustDesk Password: %PASSWORD% >> show.bat
powershell -Command "Invoke-WebRequest 'https://github.com/chieunhatnang/VM-QuickConfig/releases/download/1.6.1/VMQuickConfig.exe' -OutFile 'C:\Users\Public\Desktop\VMQuickConfig.exe'"
python.exe -m pip install --upgrade pip
pip install requests --quiet
pip install pyautogui --quiet
pip install psutil --quiet
del /f "C:\Users\Public\Desktop\Epic Games Launcher.lnk"
del /f "C:\Users\Public\Desktop\Unity Hub.lnk"
net user runneradmin LilMok
