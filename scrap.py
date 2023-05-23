import requests
from bs4 import BeautifulSoup
import csv
def stock(ticker):
    cap=ticker.upper()
    URL=f"https://www.cnbcindonesia.com/market-data/quote/{cap}.JK/{cap}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    hsl = soup.find(class_="mark_val")
    hsl3 = list(soup.find_all("ul", {"class":"market_table mt10 mb5"}))
    data=list(hsl3[0].find_all("span"))
    data1=list(hsl3[1].find_all("span"))

    prev=data[0].text
    open=data[1].text
    volume=data[2].text
    turnover=data1[0].text
    dayrange=data1[1].text
    res=list((hsl.text).split("\n"))
    res.append(prev)
    res.append(open)
    res.append(volume)
    res.append(turnover)
    res.append(dayrange)
    return res

def get_ihsg():
    URL="https://www.cnbcindonesia.com/market-data/quote/.JKSE"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    hsl = soup.find(class_="mark_val")
    res=(hsl.text).split("\n")    
    return res


def datapr():
    response=[]
    gainstring1=""
    # gainstring2=""
    gainstring3=""
    gainstring4=""

    ticker=[]
    nama=[]
    last=[]
    persen=[]
    loop=0
    m1=0
    with open('gain.csv', newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for row in data:
            ticker.append(row[0])
            nama.append(row[1])
            last.append(row[2])
            persen.append(row[4])
            m1=m1+1

    while(loop<m1):
        gainstring1=gainstring1+f"{nama[loop]} **({ticker[loop]})**\n"
        gainstring3=gainstring3+f"Rp {last[loop]}\n"
        gainstring4=gainstring4+f"{persen[loop]} %\n"
        loop=loop+1
    
    response.append(gainstring1)#0
    response.append(gainstring3)#1
    response.append(gainstring4)#2
    

    losestring1=""
    # losestring2=""
    losestring3=""
    losestring4=""
    loop=0
    ticker=[]
    nama=[]
    last=[]
    persen=[]
    m2=0
    with open('lose.csv', newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for row in data:
            ticker.append(row[0])
            nama.append(row[1])
            last.append(row[2])
            persen.append(row[4])
            m2=m2+1

    while(loop<m2):
        losestring1=losestring1+f"{nama[loop]} **({ticker[loop]})**\n"
        losestring3=losestring3+f"Rp {last[loop]}\n"
        losestring4=losestring4+f"{persen[loop]} %\n"
        loop=loop+1

    response.append(losestring1)#3
    response.append(losestring3)#4
    response.append(losestring4)#5
    m1=m2=0
    return response