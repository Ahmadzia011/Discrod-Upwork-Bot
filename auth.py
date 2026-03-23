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


MTQ3NjA5NzQ0MTc4MTY0OTUxMA.Gb3vXx.Ef8E8FCDiHBZNZhjIzZeNCDc6r_ZgEBMzd8KJ0
MTQ3NjA5NzQ0MTc4MTY0OTUxMA.GsaUqT.oLGS-k-VuJUYy3Q9n5lwH4D2_UJkyr0A637eLk