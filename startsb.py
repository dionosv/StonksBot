import os
os.system('pm2 start main.py --name "sb" --interpreter python3 --cron-restart="35 2 * * *"')
os.system('pm2 start logger.py --name "logger" --interpreter python3')