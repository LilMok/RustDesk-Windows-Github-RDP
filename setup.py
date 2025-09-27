import pyautogui as pag
import time
import requests
import os

# Start RustDesk GUI to show ID
os.system('start "" "C:\\Program Files\\RustDesk\\rustdesk.exe"')

# Give time for the app to launch
time.sleep(10)

# Take screenshot of the whole screen (includes console and GUI for debugging)
img_filename = 'rustdesk_debug.png'
pag.screenshot().save(img_filename)

# Upload to Gofile.io
def upload_image_to_gofile(img_filename):
    url = 'https://store1.gofile.io/uploadFile'
    try:
        with open(img_filename, 'rb') as img_file:
            files = {'file': img_file}
            response = requests.post(url, files=files)
            response.raise_for_status()
            result = response.json()
            if result['status'] == 'ok':
                download_page = result['data']['downloadPage']
                with open('show.bat', 'a') as bat_file:
                    bat_file.write(f'\necho Debug Screenshot: {download_page}')
                print(f"Image uploaded successfully. Link: {download_page}")
                return download_page
            else:
                print("Upload error:", result.get('status'))
                return None
    except Exception as e:
        print(f"Failed to upload image: {e}")
        return None

gofile_link = upload_image_to_gofile(img_filename)
if gofile_link:
    print(f"Debug screenshot uploaded: {gofile_link}")
else:
    print("Failed to upload the debug screenshot.")

time.sleep(10)
print('Done!')
