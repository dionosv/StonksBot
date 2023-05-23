import time
import os
from datetime import datetime
from pytz import timezone
m_day=["Mon","Tue","Wed","Thu","Fri"]
time.sleep(5)
print("PNL ready")
cooldown=600
hit=1
while(True):  
    loc_wib = datetime.utcnow().astimezone(timezone('Asia/jakarta'))
    if loc_wib.hour>=6 and loc_wib.hour<14:
      if loc_wib.strftime("%a") in m_day:
        while(True):
          print(f"Auto Movers Update <{hit}>")
          os.system("node data.js")
          print(f"Waiting for {str(cooldown)} seconds")
          time.sleep(cooldown)
          hit=hit+1
    else:
      print("Wrong Time, waiting...")
      time.sleep(cooldown)