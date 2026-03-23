import time
from datetime import datetime, timedelta
from seleniumbase import SB
import json


loaded_cookies = {}


def get_cookies(jobQuery):
    
    global loaded_cookies
    with SB(uc=True, test=True, headed=True, incognito=True) as sb:
        sb.uc_open_with_reconnect(f"https://www.upwork.com/nx/search/jobs/?q={jobQuery}", 4)
        sb.uc_gui_click_captcha()
        sb.wait_for_element('div[data-test="Tabs"]', timeout=20)  
        sb.sleep(3)
        cookies = sb.get_cookies()
        loaded_cookies = {c['name']: c['value'] for c in cookies}        
    with open("cookies.json", "w") as file:
        json.dump(loaded_cookies, file, indent=4)
