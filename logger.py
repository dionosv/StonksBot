import requests
import json
import time
import os.path
from datetime import datetime
from pytz import timezone
info="DATA FROM BINANCE\nCOLLECTED BY StonksBot#2363\n\n"

if os.path.exists('bnb_price.txt')==False:
    with open('bnb_price.txt', 'x') as f:
        f.write(info)

if os.path.exists('btc_price.txt')==False:
    with open('btc_price.txt', 'x') as f:
        f.write(info)

if os.path.exists('eth_price.txt')==False:
    with open('eth_price.txt', 'x') as f:
        f.write(info)

if os.path.exists('sol_price.txt')==False:
    with open('sol_price.txt', 'x') as f:
        f.write(info)

print("Stonksbot Logger is now online !\n"+info)

def show_time():
  loc_wib = datetime.utcnow().astimezone(timezone('Asia/tokyo'))
  tgl=str(loc_wib.strftime("%d"))
  bulan=str(loc_wib.strftime("%b"))
  jam=int(loc_wib.strftime("%H"))
  menit=str(loc_wib.strftime("%M"))
  # logi=jam+2
  # if logi>=24:
  #   logi=logi-24
  #   tgl=str(tgl+1)

  details=f"[{tgl}-{bulan}-2022]\t[{str(jam)}:{menit}]"
  return details

def logging_btc(harga):
  f=open("btc_price.txt", "a")
  f.write(f"StonksBot#2363 {show_time()} BTC ${str(harga)}\n")
  f.close()

def logging_eth(harga):
  f=open("eth_price.txt", "a")
  f.write(f"StonksBot#2363 {show_time()} ETH ${str(harga)}\n")
  f.close()

def logging_bnb(harga):
  f=open("bnb_price.txt", "a")
  f.write(f"StonksBot#2363 {show_time()} BNB ${str(harga)}\n")
  f.close()

def logging_sol(harga):
  f=open("sol_price.txt", "a")
  f.write(f"StonksBot#2363 {show_time()} SOL ${str(harga)}\n")
  f.close()

def req_www():
    r = requests.get('https://api.binance.com/api/v3/ticker/price')
    ticker=json.loads(r.text)
    return ticker

while True:
    loc_wib = datetime.utcnow().astimezone(timezone('Asia/jakarta'))


    if loc_wib.minute%15==0:
        all=req_www()
        hrg_btc=all[11]['price'][:8]
        hrg_eth=all[12]['price'][:7]
        hrg_bnb=all[98]['price'][:6]
        hrg_sol=all[779]['price'][:5]
        logging_btc(hrg_btc)
        logging_eth(hrg_eth)
        logging_bnb(hrg_bnb)
        logging_sol(hrg_sol)
        print("Logged !")
        time.sleep(60)
    else:
        time.sleep(45)