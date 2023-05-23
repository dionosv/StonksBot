import requests
import shutil 
from PIL import Image

def save(ticker):
    image_url = f"https://investor.rti.co.id/kontanweb/stock_dailychart2.jsp?code={ticker}"
    r = requests.get(image_url, stream = True)
    r.raw.decode_content = True
    with open("chart.png",'wb') as f:
        shutil.copyfileobj(r.raw, f)

def watermark():
    temp_image = Image.open('chart.png')
    watermark = Image.open('watermark.png')    

    if watermark.mode!='RGBA':
        alpha = Image.new('L', watermark.size, 15)
        watermark.putalpha(alpha)

    paste_mask = watermark.split()[3].point(lambda i: i)
    temp_image.paste(watermark, (177,240), mask=paste_mask)
    temp_image.save('chart.png')

def create(ticker):
    save(ticker)
    watermark()