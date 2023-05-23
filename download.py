import requests
import json
import os

def baca():
    nmr = open('listwatchlist/nama_koin.txt','r').read()
    return nmr

def req_www():
    r = requests.get('https://api.binance.com/api/v3/ticker/price')
    ticker=json.loads(r.text)
    return ticker

def get_coin_list():
    try:
        os.remove("datacoin_stonksbot.txt")
    except:
        pass

    x=0
    r = requests.get('https://api.binance.com/api/v3/ticker/price')
    ticker=json.loads(r.text)
    f = open("datacoin_stonksbot.txt","a")
    while(x<len(ticker)):
        txt=f"{str(ticker[x]['symbol'])}-{str(x)}\n"
        f.write(txt)
        x=x+1
    x=0
    f.close()
    print("Data succesfully extracted")

def get_price(what):
    if what == "btc":
        angka=11
    else:
        angka=int(baca())
    hrg=req_www()[angka]['price'][:8]
    return hrg
    

def get_ticker():
    angka=int(baca())
    sym=req_www()[angka]['symbol']
    return sym

def find(ticker):
    myfile = open("datacoin_stonksbot.txt", "r")
    v=0
    while myfile:
        line  = myfile.readline()
        if line.startswith(ticker):
            return v
        elif v>=2000:
            return 2222
        v=v+1
    myfile.close() 