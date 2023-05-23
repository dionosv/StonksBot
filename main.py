from dis import Instruction
from email.headerregistry import ContentDispositionHeader
from inspect import isfunction
from ssl import SSL_ERROR_SSL
import discord
import os
import requests
import json
import asyncio
from datetime import datetime
from pytz import timezone
from discord.ext import commands,tasks
from saham import withname
from listnya import lq455,brokerage,admin_utama,premarket,bnfc_admin,loss
from extract import extract
from download import get_coin_list,get_price,get_ticker,find
from scrap import stock,get_ihsg,datapr
from toogle import mulai
from reminder import sign
from time import perf_counter
from chart import create
prefix="t."
client = commands.Bot(command_prefix=prefix, case_insensitive=True, help_command=None)
datalist="listwatchlist/list_server.json"
storage="listwatchlist/storage.json"
m_day=["Mon","Tue","Wed","Thu","Fri"]
rminder="StonksBot___"
personal_max=5

def show_time():
  loc_wib = datetime.utcnow().astimezone(timezone('Asia/tokyo'))
  tgl=str(loc_wib.strftime("%d"))
  bulan=str(loc_wib.strftime("%b"))
  jam=int(loc_wib.strftime("%H"))
  menit=str(loc_wib.strftime("%M"))
  detik=str(loc_wib.strftime("%S"))
  details=f'[{tgl}-{bulan}-2022]\t[{jam}:{menit}:{detik}]'
  return details

def logging(penulis,keterangan):
  f=open("log.txt", "a")
  f.write(f"{show_time()} {str(penulis)} {str(keterangan)}\n")
  f.close()

def lognws(penulis,berita):
  f=open("lognews.txt", "a")
  f.write(f"{show_time()} news by {str(penulis)}\n{str(berita)}\n\n")
  f.close()

@client.event
async def on_ready():
    loc_wib = datetime.utcnow().astimezone(timezone('Asia/jakarta'))
    print(f'{client.user} connected')
    print(f'{client.user} ready to use')
    prv = client.get_channel("Private Channel")
    em=discord.Embed(description=f"{client.user} is ready", timestamp=datetime.utcnow(), color=0x23ff8e)
    await prv.send(embed=em)
    logging("---SYSTEM---",f"{client.user} is ready")
    print(f"\n{client.user} available in :")
    async for guild in client.fetch_guilds(limit=50):
        print(guild.name)
    if loc_wib.strftime("%a") in m_day:
      await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name='% gain war'))
    else:
      while(True):
          price=str(get_price())
          await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{str(get_ticker())} at {price}"))
          await asyncio.sleep(15)

r_title="StonksBot Reminder 🔔"
@tasks.loop(seconds=1)#jam di tambah 6 jam semua
async def market():
    loc_wib = datetime.utcnow().astimezone(timezone('Asia/jakarta'))
    if loc_wib.strftime("%a") in m_day:
      i=0
      if loc_wib.hour==7 and loc_wib.minute==44 and loc_wib.second==1:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name='PRE-OPENING'))
        try: 
          res=get_ihsg()
          indeks=res[1]
          chg=res[2]
          em=discord.Embed(title=r_title,description=f"Pre Opening Market\n\n> IHSG {indeks} {chg}", color=0xFFFFFF)
        except:
          em=discord.Embed(title=r_title,description="Pre Opening Market", color=0xFFFFFF)

        with open(datalist, "r") as file:
          datax = json.load(file)
          while(i<len(datax)):
            prv = client.get_channel(datax[i]["tc"])
            await prv.send(embed=em,delete_after=799)
            i=i+1
        
      elif loc_wib.hour==7 and loc_wib.minute==54 and loc_wib.second==1:
        with open(datalist, "r") as file:
          datax = json.load(file)
          while(i<len(datax)):
            prv = client.get_channel(datax[i]["tc"])
            em=discord.Embed(title=r_title,description="Market sesi 1 akan di mulai dalam 5 menit", color=0xFFFFFF)
            await prv.send(embed=em,delete_after=299)
            i=i+1

      elif loc_wib.hour==7 and loc_wib.minute==59 and loc_wib.second==59:
        with open(datalist, "r") as file:
          datax = json.load(file)
          while(i<len(datax)):
            prv = client.get_channel(datax[i]["tc"])
            em=discord.Embed(title=r_title,description="Market sesi 1 di mulai", color=0xFFFFFF)
            await prv.send(embed=em,delete_after=299)
            i=i+1
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name='SESSION 1'))

      elif loc_wib.hour==10 and loc_wib.minute==20 and loc_wib.second==1:
        with open(datalist, "r") as file:
          datax = json.load(file)
          while(i<len(datax)):
            prv = client.get_channel(datax[i]["tc"])
            em=discord.Embed(title=r_title,description="Sesi 1 akan berahkir dalam 10 menit", color=0xFFFFFF)
            await prv.send(embed=em,delete_after=599)
            i=i+1

      elif loc_wib.hour==10 and loc_wib.minute==29 and loc_wib.second==59:
        with open(datalist, "r") as file:
          datax = json.load(file)
          while(i<len(datax)):
            prv = client.get_channel(datax[i]["tc"])
            em=discord.Embed(title=r_title,description="Sesi 1 selesai", color=0xFFFFFF)
            await prv.send(embed=em,delete_after=599)
            i=i+1
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="chart on break"))

      elif loc_wib.hour==12 and loc_wib.minute==20 and loc_wib.second==1:
        hasil=datapr()
        with open(datalist, "r") as file:
          datax = json.load(file)
          while(i<len(datax)):
            prv = client.get_channel(datax[i]["tc"])
            em=discord.Embed(title=r_title,description="Sesi 2 akan di mulai dalam 10 menit", color=0xFFFFFF)
            await prv.send(embed=em,delete_after=599)
            gain=discord.Embed(title="Daily Gainer 📈",color=0x23ff8e)
            gain.add_field(name="Stock",value=hasil[0],inline=True)
            gain.add_field(name="Gain",value=hasil[2],inline=True)
            gain.add_field(name="Last",value=hasil[1],inline=True)
            gain.set_image(url="https://i.ibb.co/vzZwjFn/sb-header-trans.png")
            # gain.set_footer(text=f"\nDuring trading hours, price action delayed")
            lose=discord.Embed(title="Daily Loser 📉",color=0x23ff8e)
            lose.add_field(name="Stock",value=hasil[3],inline=True)
            lose.add_field(name="Loss",value=hasil[5],inline=True)
            lose.add_field(name="Last",value=hasil[4],inline=True)
            lose.set_image(url="https://i.ibb.co/vzZwjFn/sb-header-trans.png")
            # lose.set_footer(text=f"\nDuring trading hours, price action delayed")
            try:
              await prv.send(embed=gain,delete_after=599)
              await prv.send(embed=lose,delete_after=599)
            except:
              pass
            i=i+1

      elif loc_wib.hour==12 and loc_wib.minute==29 and loc_wib.second==59:
        with open(datalist, "r") as file:
          datax = json.load(file)
          while(i<len(datax)):
            prv = client.get_channel(datax[i]["tc"])
            em=discord.Embed(title=r_title,description="Sesi 2 di mulai", color=0xFFFFFF)
            await prv.send(embed=em,delete_after=599)
            i=i+1
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name='SESSION 2'))

      elif loc_wib.hour==13 and loc_wib.minute==39 and loc_wib.second==59:
        with open(datalist, "r") as file:
          datax = json.load(file)
          while(i<len(datax)):
            prv = client.get_channel(datax[i]["tc"])
            em=discord.Embed(title=r_title,description="Sesi 2 akan berahkir dalam 10 menit", color=0xFFFFFF)
            await prv.send(embed=em,delete_after=599)
            i=i+1

      elif loc_wib.hour==13 and loc_wib.minute==49 and loc_wib.second==59:
        with open(datalist, "r") as file:
          datax = json.load(file)
          while(i<len(datax)):
            prv = client.get_channel(datax[i]["tc"])
            em=discord.Embed(title=r_title,description="Sesi 2 selesai", color=0xFFFFFF)
            await prv.send(embed=em,delete_after=299)
            i=i+1
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name='PRE-CLOSING'))

      elif loc_wib.hour==14 and loc_wib.minute==10 and loc_wib.second==1:
          with open(datalist, "r") as file:
            datax = json.load(file)
            while(i<len(datax)):
              prv = client.get_channel(datax[i]["tc"])
              em=discord.Embed(title=r_title,description="Market akan tutup 5 menit lagi", color=0xFFFFFF)
              await prv.send(embed=em,delete_after=300)
              i=i+1

      elif loc_wib.hour==14 and loc_wib.minute==20 and loc_wib.second==0:
          hasil=datapr()
          with open(datalist, "r") as file:
            datax = json.load(file)
            while(i<len(datax)):
              prv = client.get_channel(datax[i]["tc"])
              gain=discord.Embed(title="Daily Gainer 📈",color=0x23ff8e)
              gain.add_field(name="Stock",value=hasil[0],inline=True)
              gain.add_field(name="Gain",value=hasil[2],inline=True)
              gain.add_field(name="Last",value=hasil[1],inline=True)
              gain.set_image(url="https://i.ibb.co/vzZwjFn/sb-header-trans.png")
              # gain.set_footer(text=f"\nDuring trading hours, price action delayed")
              lose=discord.Embed(title="Daily Loser 📉",color=0x23ff8e)
              lose.add_field(name="Stock",value=hasil[3],inline=True)
              lose.add_field(name="Loss",value=hasil[5],inline=True)
              lose.add_field(name="Last",value=hasil[4],inline=True)
              lose.set_image(url="https://i.ibb.co/vzZwjFn/sb-header-trans.png")
              # lose.set_footer(text=f"\nDuring trading hours, price action delayed")
              try:
                await prv.send(embed=gain,delete_after=5999)
                await prv.send(embed=lose,delete_after=5999)
              except:
                pass
              i=i+1
              
            try:
                os.system("pm2 stop movers")
            except:
                pass

      elif loc_wib.hour==14 and loc_wib.minute==15 and loc_wib.second==0:
          while(True):
            price=str(get_price())
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{str(get_ticker())} at {price}"))
            await asyncio.sleep(10)
      i=0

d=open("reminder.txt", "r")
on_off=d.read()
if on_off == "On":
  market.start()
  try:
    os.system("pm2 restart movers")
  except:
    pass
else:
  logging("---SYSTEM---","Day Off Stock Market Closed Today !")
  try:
    os.system("pm2 stop movers")
  except:
      pass
d.close()
  
@commands.guild_only()
@commands.has_role("ADMIN")
@client.command()
async def plan (ctx,Ticker,entry=0,target=0):
  server_id=ctx.message.guild.id
  filename = f"listwatchlist/{str(server_id)}.json"
  with open(filename, "r") as file:
    datax = json.load(file)
  with open(storage, "r") as file:
    data_max = json.load(file)
  x=0
  in_data=len(datax)
  while(x<len(data_max)):
    if data_max[x]["server"]==server_id:
      max_entries=int(data_max[x]["max_wl"])
      break
    else:
      x=x+1
    
  if in_data>=max_entries:
    red=discord.Embed(title="Watchlist Limit ⚠️",description=f"Watchlist exceeds the limit ``{in_data}/{max_entries}``\nRemove watchlist to add more !",color=0xFF0000)
    await ctx.reply(embed=red,delete_after=20)
    await asyncio.sleep(20)
    await ctx.message.delete()

  elif str(Ticker).upper() not in withname:
    await ctx.send(f'**{Ticker.upper()}** not on the list, please try again !\nWarrant is currently not supported !',delete_after=5)
    await asyncio.sleep(4)
    await ctx.message.delete()
  elif entry>target:
    red=discord.Embed(title="Invalid number !",description='Buy price bigger than Sell price',color=0xFF0000)
    await ctx.reply(embed=red,delete_after=10)
    await asyncio.sleep(10)
    await ctx.message.delete()
  elif entry and target <50:
    await ctx.reply(f'{ctx.author.mention}, Buy or Sell Price cannot be lower than 50\nWarrant is currently not supported !',delete_after=5)
    await asyncio.sleep(5)
  else:
    calc_gain=((target-entry)/entry*100)
    calc_rounded=str(round(calc_gain,2))
    cl=int(entry-(entry*loss/100))
    if cl<=50:
      cl=50
    if Ticker.upper() in premarket:
      emoji="\nPRE-MARKET ☀️"
      sun=True
    else:
      emoji=""
      sun=False
    if Ticker.upper() in lq455:
      emoji2="\nLQ45 🎯"
      lq=True
    else:
      emoji2=""
      lq=False

    cut=str(f'{cl:,}')
    entry=str(f'{entry:,}')
    target=str(f'{target:,}')
    grem=discord.Embed(title=f"{withname[Ticker.upper()]} ({Ticker[0:4].upper()})",description=f"Buy = Rp {str(entry)}\nSell = Rp {str(target)} ({calc_rounded} %)\nCL ({str(loss)} %) ± Rp {str(cut)}\n\n"+emoji+emoji2,color=0x23ff8e)
    grem.set_footer(text=f"Stonksbot - {ctx.author}")
    print(f'{rminder}P [{Ticker.upper()}  buy {entry} | sell {target}] <{ctx.message.guild.name} @{ctx.author}>')
    m=await ctx.send(embed=grem)
    mid=m.id
    
    with open(storage, "r") as file:
      data = json.load(file)
    x=0
    y=len(data)
    while(x<y):
      if data[x]["server"]==server_id:
        chann=int(data[x]["chann_id"])
        msg=int(data[x]["msg_id"])
        req_msg=int(data[x]["req_id"])
        try:
          await client.http.delete_message(chann, req_msg) 
          await client.http.delete_message(chann, msg) 
        except:
          pass
        break
      else:
        x=x+1

    cid=ctx.message.channel.id
    # gid=ctx.message.guild.id
    await ctx.message.delete()
    #storing in json dibawah ini
    shm_data={"name":f'{Ticker.upper()}',"buy":f'Rp {str(entry)}',"sell":f'Rp {str(target)}',"gain":f'{str(calc_rounded.replace(".",","))} %','pm':sun,'lq':lq,"author":f'{ctx.author}',"tc_id":cid,"msg_id":mid}
    with open(filename, "r") as file:
      data = json.load(file)
    data.append(shm_data)
    with open(filename, "w") as file:
      json.dump(data, file)
    logging(ctx.author,f"Set {Ticker.upper()} plan on {ctx.message.guild.name}")
      
@commands.guild_only()
@commands.has_role("ADMIN")
@client.command()
async def note(ctx,title,*,pesan="no notes"):
    whit=discord.Embed(title=str(title).upper(),description=pesan.replace("??","\n"),color=0x23ff8e)
    whit.set_footer(text=f'Note author {ctx.author}')
    await ctx.message.delete()
    await ctx.send(embed=whit)
    logging(ctx.author,f"Set notes on {ctx.message.guild.name} containing '{pesan[:40]}'")

@client.command()
async def priv (ctx,Ticker,entry=0,target=0):
  auth=ctx.author.id
  filename = f"listwatchlist/private/{str(auth)}.json"
  if os.path.exists(filename)==False:
    with open(filename, 'x') as f:
        f.write("[]")
  with open(filename, "r") as file:
    datax = json.load(file)      
  max_entries=personal_max
  in_data=len(datax)
    
  if in_data>=max_entries:
    red=discord.Embed(title="Watchlist Limit ⚠️",description=f"Watchlist exceeds the limit ``{in_data}/{max_entries}``\nRemove watchlist to add more !",color=0xFF0000)
    await ctx.reply(embed=red,delete_after=20)
    await asyncio.sleep(20)
    await ctx.message.delete()

  elif str(Ticker).upper() not in withname:
    await ctx.send(f'**{Ticker.upper()}** not on the list, please try again !\nWarrant is currently not supported !',delete_after=5)
    await asyncio.sleep(4)
    await ctx.message.delete()
  elif entry>target:
    red=discord.Embed(title="Invalid number !",description='Buy price bigger than Sell price',color=0xFF0000)
    await ctx.reply(embed=red,delete_after=10)
    await asyncio.sleep(10)
    await ctx.message.delete()
  elif entry and target <50:
    await ctx.reply(f'{ctx.author.mention}, Buy or Sell Price cannot be lower than 50\nWarrant is currently not supported !',delete_after=5)
    await asyncio.sleep(5)
    await ctx.message.delete()
  else:
    calc_gain=((target-entry)/entry*100)
    calc_rounded=str(round(calc_gain,2))
    if Ticker.upper() in premarket:
      sun=True
    else:
      sun=False
    if Ticker.upper() in lq455:
      lq=True
    else:
      lq=False
    entry=str(f'{entry:,}')
    target=str(f'{target:,}')
    # grem=discord.Embed(title=f"{withname[Ticker.upper()]} ({Ticker[0:4].upper()})",description=f"Buy = Rp {str(entry)}\nSell = Rp {str(target)} ({calc_rounded} %)\nCL ({str(loss)} %) ± Rp {str(cut)}\n\n"+emoji+emoji2,color=0x23ff8e)
    # grem.set_footer(text=f"Stonksbot - {ctx.author}")
    grem=discord.Embed(description=f"**{Ticker.upper()}** stored",color=0x23ff8e)
    grem.set_footer(text=f"Stonksbot - {ctx.author}")
    print(f'{rminder}PP [{Ticker.upper()}  buy {entry} | sell {target}] <{ctx.author}>')
    await ctx.send(embed=grem,delete_after=15)
    try:
      await ctx.message.delete()
    except:
      pass
    #storing in json dibawah ini
    shm_data={"name":f'{Ticker.upper()}',"buy":f'Rp {str(entry)}',"sell":f'Rp {str(target)}',"gain":f'{str(calc_rounded.replace(".",","))} %','pm':sun,'lq':lq,"author":f'{ctx.author}'}
    with open(filename, "r") as file:
      data = json.load(file)
    data.append(shm_data)
    with open(filename, "w") as file:
      json.dump(data, file)
    logging(ctx.author,f"Set {Ticker.upper()} private plan")

@commands.guild_only()
@commands.has_role("ADMIN")
@client.command()
async def wl(ctx,tag='c'):
  if tag=="p":
      hit=0
      auth=ctx.author.id
      filename = f"listwatchlist/private/{str(auth)}.json"
      if os.path.exists(filename)==False:
        whit=discord.Embed(description=f"No Private Watchlist",color=0xFF0000)
        await ctx.reply(embed=whit,delete_after=10)
        await asyncio.sleep(10)
        await ctx.message.delete()
      else:
        with open(filename, "r") as file:
          datax = json.load(file)
        nomer=1
        string=""
        string2=""
        string3=""
        for apa in datax:
            if apa["pm"]==True:
              emoji=" :sunny:"
              hit=hit+1
            else:
              emoji=""
            if apa["lq"]==True:
              emoji2=" 🎯"
              hit=hit+1
            else:
              emoji2=""

            panjang=withname[apa["name"].upper()]
            string +=f'{nomer}. {panjang} **({str(apa["name"])})**{emoji}{emoji2}\n'
            string2+=f'{apa["buy"]}\n'
            string3+=f'{apa["sell"]} **({apa["gain"]})**\n'
            nomer=nomer+1

        wktu=show_time()
        if hit==0:
          inform=f"``{str(nomer-1)}/{personal_max}``\nUpdated on {wktu}"
        else:
          inform=f"``{str(nomer-1)}/{personal_max}``\nUpdated on {wktu}\n☀️ = [Pre-Market](https://www.idx.co.id/media/10745/20220131_saham_yang_dapat_diperdagangkan_melalui_sesi_pra-pembukaan_di_pasar_reguler.zip)\n🎯 = [LQ45](https://www.kontan.co.id/indeks-lq45)"        
        em=discord.Embed(title=f'``{ctx.author}`` Private Watchlist',color=0x23ff8e)
        em.add_field(name="Stock Name",value=string,inline=True)
        em.add_field(name="Buy",value=string2,inline=True)
        em.add_field(name="Sell",value=string3,inline=True)
        em.add_field(name="⠀",value=inform,inline=False)
        em.set_image(url="https://i.ibb.co/vzZwjFn/sb-header-trans.png")
        await ctx.reply(embed=em)
        logging(ctx.author,f"Displaying private watchlist on {ctx.message.guild.name}")
        print(f'{rminder}PW <{ctx.message.guild.name} @{ctx.author}>')
  else:
      new_req=ctx.message.id
      hit=0
      server_id=ctx.message.guild.id
      server_name=str(ctx.message.guild.name)
      filename = f"listwatchlist/{str(server_id)}.json"
      cek=int(sign(int(server_id)))
      if cek!=1:
        pesan=f"\n**server reminder required**"
        logo=""
      else:
        pesan=""
        logo="  ⏰"
  
      with open(filename, "r") as file:
          datax = json.load(file)
      if (len(datax)) == 0:
        whit=discord.Embed(description=f"No Watchlist in ``{server_name}``",color=0xFF0000)
        await ctx.reply(embed=whit,delete_after=10)
        await asyncio.sleep(10)
        await ctx.message.delete()
      else:
        with open(storage, "r") as file:
            data_max = json.load(file)
        x=0
        while(x<len(data_max)):
          if data_max[x]["server"]==server_id:
              max_entries=int(data_max[x]["max_wl"])
              status=(data_max[x]["is_premium"])
              if status==True:
                subs="``Prime``"
              elif status==False:
                subs=""
              break
          else:
              x=x+1
        nomer=1
        string=""
        string2=""
        string3=""
        for apa in datax:
            if apa["pm"]==True:
              emoji=" :sunny:"
              hit=hit+1
            else:
              emoji=""
            if apa["lq"]==True:
              emoji2=" 🎯"
              hit=hit+1
            else:
              emoji2=""

            panjang=withname[apa["name"].upper()]
            string +=f'{nomer}. {panjang} **({str(apa["name"])})**{emoji}{emoji2}\n'
            string2+=f'{apa["buy"]}\n'
            string3+=f'{apa["sell"]} **({apa["gain"]})**\n'
            nomer=nomer+1

        wktu=show_time()
        if hit==0:
          inform=f"{subs} ``{str(nomer-1)}/{max_entries}``{logo}\nUpdated on {wktu}\n{pesan}\n"
        else:
          inform=f"{subs} ``{str(nomer-1)}/{max_entries}``{logo}\nUpdated on {wktu}\n☀️ = [Pre-Market](https://www.idx.co.id/media/10745/20220131_saham_yang_dapat_diperdagangkan_melalui_sesi_pra-pembukaan_di_pasar_reguler.zip)\n🎯 = [LQ45](https://www.kontan.co.id/indeks-lq45)\n{pesan}"        
        
        em=discord.Embed(title=f'{str(len(datax))} Watchlist in ``{server_name}``',color=0x23ff8e)
        em.add_field(name="Stock Name",value=string,inline=True)
        em.add_field(name="Buy",value=string2,inline=True)
        em.add_field(name="Sell",value=string3,inline=True)
        em.add_field(name="⠀",value=inform,inline=False)
        em.set_image(url="https://i.ibb.co/vzZwjFn/sb-header-trans.png")
        kirim_wl=await ctx.reply(embed=em)
        new_msg=kirim_wl.id
        new_chan=ctx.message.channel.id

        with open(storage, "r") as file:
            data = json.load(file)
        x=0
        y=len(data)
        while(x<y):
            if data[x]["server"]==server_id:
              chann=int(data[x]["chann_id"])
              msg=int(data[x]["msg_id"])
              req_msg=int(data[x]["req_id"])
              try:
                await client.http.delete_message(chann, req_msg) 
                await client.http.delete_message(chann, msg) 
              except:
                pass
              package=data[x]
              break
            else:
                x=x+1
        edit1={"chann_id":f"{new_chan}"}
        edit2={"msg_id":f"{new_msg}"}
        edit3={"req_id":f"{new_req}"}
        package.update(edit1)
        package.update(edit2)
        package.update(edit3)
        with open(storage, "r") as file:
            data2 = json.load(file)
        data2.append(package)
        with open(storage, "w") as file:
            del data2[x]
            json.dump(data2, file)
          
        logging(ctx.author,f"Displaying watchlist on {ctx.message.guild.name}")
        print(f'{rminder}W <{ctx.message.guild.name} @{ctx.author}>')
  
@commands.guild_only()
@commands.has_role("ADMIN")
@client.command(aliases=["del","delete"])
async def clear(ctx,amount=5):
    clr=discord.Embed(title="Clear Requests",description=f'{amount} messages deleted',color=0x23ff8e)
    await ctx.channel.purge(limit=amount)
    await ctx.send(embed=clr,delete_after=5)
    logging(ctx.author,f"Delete {amount} messages on {ctx.message.guild.name}")
    print(f"{rminder}CLR [{amount}] <{ctx.message.guild.name} @{ctx.author}>")
  
@commands.guild_only()
@client.command(aliases=["help"])
async def info(ctx):
  whit=discord.Embed(title="How to Use Stonks Bot",color=0x23ff8e)
  whit.add_field(name="command info",value=f"add tradeplan^\nshow tradeplan^\nremove tradeplan^\nstocks in LQ45\nreset tradeplan^\nask ticker\nask brokercode\nar calculator\nask price\nbot invite\nassign channel for reminder^^",inline=True)
  whit.add_field(name="command",value=f"{prefix}``[plan/priv]``^^^ ``[ticker]`` ``[buy]`` ``[sell]``\n{prefix}wl\n{prefix}remove ``[ticker]``\n{prefix}lq45\n{prefix}reset ``[c/p]``^^^\n{prefix}ask ``[ticker]``\n{prefix}br ``[broker code]``\n{prefix}ar ``[price]``\n{prefix}price ``[ticker]``\n{prefix}invite\n{prefix}assign",inline=True)
  whit.set_footer(text=f"Note :\nParameter inside [ ] is required\n^ADMIN role only (set up ADMIN role <CAPSLOCK ON !>)\n^First things to do after inviting bot (^)\n^^^priv is for private watchlist, c is for channel watchlist Default choices is channel")
  whit.set_image(url="https://i.ibb.co/vzZwjFn/sb-header-trans.png")
  await ctx.reply(embed=whit)
  print(f"{rminder}INFO <{ctx.message.guild.name} @{ctx.author}>")
  logging(ctx.author,f"Requesting info in {ctx.message.guild.name}")

@commands.guild_only()
@commands.has_role("ADMIN")
@client.command(aliases=["rst","rs"])
async def reset(ctx,tag='c'):
  if tag=="p":
    try:
      auth=ctx.author.id
      filename = f"listwatchlist/private/{str(auth)}.json"
      os.remove(filename)
      clr=discord.Embed(title="Watchlist Reset Success",description=f"Private watchlist deleted",color=0x23ff8e)
      await ctx.reply(embed=clr,delete_after=5)
      await asyncio.sleep(5)
      await ctx.message.delete()
    except:
      clr=discord.Embed(title="Watchlist Reset Failed",description=f"Private watchlist not found",color=0xFF0000)
      await ctx.reply(embed=clr,delete_after=5)
      await asyncio.sleep(5)
      await ctx.message.delete()
  else:
    usr=ctx.author
    server_id=ctx.message.guild.id
    server_name=str(ctx.message.guild.name)
    filename = f"listwatchlist/{str(server_id)}.json"
    with open(filename,"r") as file:
      baca=json.load(file)
    
    jml=len(baca)
    if jml == 0:
      await ctx.reply(f"No Watchlist in ``{server_name}``",delete_after=15)
      await asyncio.sleep(15)
      await ctx.message.delete()

    else :
      prompt=discord.Embed(title="Reset confirmation",description=f"Do you want to delete {str(jml)} watchlist ?\n(yes/no)", color=0xFF0000)
      msg = await ctx.send(embed=prompt)

      mid = msg.id
      tid = ctx.message.channel.id

      while True:
        message=await client.wait_for('message', check=lambda message: message.author==usr)
        if "yes" in message.content:
          menu1=discord.Embed(title="Watchlist Reset",description="Watchlist Reset On Process",color=0xFF0000)
          await ctx.send(embed=menu1,delete_after=2)
          x=0
          while(x!=jml):
            chan=int(baca[x]["tc_id"])
            msid=int(baca[x]["msg_id"])
            try:
              await client.http.delete_message(chan, msid) 
            except:
              pass
            x=x+1
          file.close()
          save=json.dumps([])
          file2=open(filename,'w')
          file2.write(save)
          file2.close()

          with open(storage, "r") as file:
            data = json.load(file)
          x=0
          y=len(data)
          while(x<y):
            if data[x]["server"]==server_id:
              chann=int(data[x]["chann_id"])
              msg=int(data[x]["msg_id"])
              req_msg=int(data[x]["req_id"])
              try:
                await client.http.delete_message(chann, req_msg) 
                await client.http.delete_message(chann, msg) 
              except:
                pass
              break
            else:
              x=x+1

          clr=discord.Embed(title="Watchlist Reset Successful",description=f"{ctx.author} deleted {str(jml)} watchlist",color=0xFF0000)
          await ctx.reply(embed=clr)
          print(f"{rminder}W-RST <{ctx.message.guild.name} @{ctx.author}>")
          logging(ctx.author,f"Reset watchlist on {ctx.message.guild.name}")
          try:
              await client.http.delete_message(tid, mid) 
          except:
              pass
          break

        if "no" in message.content:
          await ctx.reply("Watchlist reset canceled",delete_after=15)
          try:
              await client.http.delete_message(tid, mid) 
          except:
              pass
          break

        else:
          await ctx.reply(f"{ctx.author.mention}, only type in yes / no",delete_after=9)


@commands.guild_only()
@client.command()
async def mkt(ctx,name):
  if(len(name)>4):
    await ctx.reply(f'**{name.upper()}** not on the list',delete_after=20)
    await asyncio.sleep(19)
    await ctx.message.delete()
  elif(str(name).upper() not in withname):
    await ctx.reply(f'**{name.upper()}** not on the list',delete_after=10)
    await asyncio.sleep(9)
    await ctx.message.delete()
  else:
    promp1 = await ctx.reply(f'Please wait while <@!865074463922192414> preparing **{str(name).upper()}** price')
    #linknya="https://cdn.statically.io/screenshot/mobile/finance.yahoo.com/quote/"+str(name)+".JK?p="+str(name)+".JK&ncid=stockrec"
    linknya="https://image.thum.io/get/iphone6/crop/666/maxAge/1/noanimate/https://finance.yahoo.com/quote/"+str(name)+".JK?p="+str(name)+".JK&ncid=stockrec"
    response = requests.get(linknya)
    file = open("saham_req.png", "wb")
    file.write(response.content)
    file.close()
    print(f'{rminder}CHART-REQ {str(name).upper()} <{ctx.message.guild.name} @{ctx.author}>')
    await promp1.edit(content=f'**{str(name).upper()}** price\n*this message will automatically deleted within a minute*',delete_after=59)
    await ctx.reply(file=discord.File('saham_req.png'),delete_after=60)
    await asyncio.sleep(59)
    await ctx.message.delete()

@commands.guild_only()
@client.command()
async def ask (ctx,Ticker):
  if str(Ticker).upper() not in withname:
    await ctx.reply(f'**{Ticker.upper()}** not on the list, please try again !',delete_after=5)
    await asyncio.sleep(4)
    await ctx.message.delete()

  else:
    await ctx.reply(f'{withname[Ticker.upper()]} ('+Ticker[0:4].upper()+")",delete_after=325)
    logging(ctx.author,f"Ask {Ticker.upper()} on {ctx.message.guild.name}")
    print(f'{rminder}A {Ticker.upper()} <{ctx.message.guild.name} @{ctx.author}>')
    await asyncio.sleep(324)
    await ctx.message.delete()

@commands.guild_only()
@client.command()
async def lq45(ctx):
  embed2=discord.Embed(title="LQ45 🎯 list",description="[Indeks LQ45](https://www.kontan.co.id/indeks-lq45)", color=0x23ff8e)
  await ctx.send(embed=embed2)

@commands.guild_only()
@client.command()
async def br (ctx,Broker_code):
  if str(Broker_code).upper() not in brokerage:
    await ctx.send(f'**{Broker_code.upper()}** not on the list, please try again !',delete_after=5)
    await asyncio.sleep(5)
    await ctx.message.delete()

  else:
    logging(ctx.author,f"Ask broker {Broker_code.upper()} {ctx.message.guild.name}")
    await ctx.reply(f'{brokerage[Broker_code.upper()]} ('+Broker_code[0:2].upper()+")",delete_after=100)
    print(f'{rminder}BR[<{ctx.message.guild.name} @{ctx.author}> {str(Broker_code).upper()}')
    await asyncio.sleep(100)
    await ctx.message.delete()

@commands.guild_only()
@client.command()
async def ar (ctx,harga=-5):
  if harga==-5 or harga<49:
    white=discord.Embed(description=f"Please enter [price]\n```{prefix}ar [price>=50]```",color=0x23ff8e)
    await ctx.reply(embed=white,delete_after=15)
    await asyncio.sleep(15)
    await ctx.message.delete()
  else:
    if harga>=50 and harga<=200:
      ara=harga+(harga*35/100)
      arb=harga-(harga*7/100)
      if arb<50:
        arb=50
      bulat_ara=1*round(ara/1)
      bulat_arb=1*round(arb/1)
      embed=discord.Embed(title="Auto Reject Calculator",description=f'Rp {harga}', color=0x23ff8e)
      embed.add_field(name="ARA", value="Rp "+str(bulat_ara), inline=True)
      embed.add_field(name="ARB", value="Rp "+str(bulat_arb), inline=True)
      embed.set_footer(text="Stonksbot")
      await ctx.reply(embed=embed)

    elif harga>=201 and harga<=5000:
      ara=harga+(harga*25/100)
      arb=harga-(harga*7/100)
      if ara>=200 and ara<=500:
        bulat_ara=2*round(ara/2)
      elif ara>=501 and ara<=2000:
        bulat_ara=5*round(ara/5)
      elif ara>=2001 and ara<=5000:
        bulat_ara=10*round(ara/10)
      elif ara>=5001:
        bulat_ara=25*round(ara/25)

      if arb<200:
        bulat_arb=1*round(arb/1)
      if arb>=200 and arb<=500:
        bulat_arb=2*round(arb/2)
      elif arb>=501 and arb<=2000:
        bulat_arb=5*round(arb/5)
      elif arb>=2001 and arb<=5000:
        bulat_arb=10*round(arb/10)
      embed=discord.Embed(title="Auto Reject Calculator",description=f'Rp {harga}', color=0x23ff8e)
      embed.add_field(name="ARA", value="Rp "+str(bulat_ara), inline=True)
      embed.add_field(name="ARB", value="Rp "+str(bulat_arb), inline=True)
      embed.set_footer(text="Stonksbot")
      await ctx.reply(embed=embed)

    elif harga>=5001:
      ara=harga+(harga*20/100)
      arb=harga-(harga*7/100)
      if ara>=5001:
        bulat_ara=25*round(ara/25)
      if arb<=5000:
        bulat_arb=10*round(arb/10)
      elif arb>=5001:
        bulat_arb=25*round(arb/25)
      embed=discord.Embed(title="Auto Reject Calculator",description=f'Rp {harga}', color=0x23ff8e)
      embed.add_field(name="ARA", value="Rp "+str(bulat_ara), inline=True)
      embed.add_field(name="ARB", value="Rp "+str(bulat_arb), inline=True)
      embed.set_footer(text="Stonksbot")
      await ctx.reply(embed=embed)

#maintenance commands
@commands.guild_only()
@client.command()
async def main(ctx):
  i=0
  if ctx.author.id in admin_utama:
      with open(datalist, "r") as file:
          datax = json.load(file)
      while(i<len(datax)):
            prv = client.get_channel(datax[i]["tc"])
            em=discord.Embed(description="test", color=0x23ff8e)
            await prv.send(embed=em,delete_after=30)
            i=i+1
      await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name='maintenance'))
      print(f'{rminder}Maintenance Mode')

@commands.guild_only()
@client.command(aliases=['inv'])
async def invite(ctx):
  red_em=discord.Embed(title="Stonks Bot Invite",description="[INVITE LINK](https://discord.com/api/oauth2/authorize?client_id=865074463922192414&permissions=8&scope=bot)",color=0x23ff8e)
  await ctx.reply(embed=red_em)
  logging(ctx.author,f"Request bot invitation link on {ctx.message.guild.name}")

@commands.guild_only()
@commands.has_role("ADMIN")
@client.command()
async def assign(ctx):
  channid=ctx.channel.id
  guildid=ctx.message.guild.id
  v=0
  condition=False
  with open(datalist, "r") as file:
      datax = json.load(file)
  while(v<len(datax)):
    if guildid==datax[v]["guild_id"]:
      em=discord.Embed(title=r_title,description=f'{ctx.author.mention}, this server have already assigned a text channel for reminder,\n checkout <#{datax[v]["tc"]}> for reminder !\n\n``if you want to change the text channel for reminder, simply re-invite this bot and type {prefix}assign in selected text channel``\n\nnote : to re-invite <@!865074463922192414> type ``{prefix}invite`` and then kick <@!865074463922192414>\n⚠️** re-invite can causes watchlist reset !**',color=0xFF0000)
      await ctx.reply(embed=em)
      condition=True
      break
    v=v+1
  if condition==False:
    if ctx.author.id in admin_utama:
        datanya={"guild_id" : guildid,"tc" : channid}
        with open(datalist, "r") as file:
          data = json.load(file)
        data.append(datanya)
        with open(datalist, "w") as file:
          json.dump(data, file)
        await ctx.reply(f'<#{channid}> assigned for '+r_title,delete_after=15)
        await asyncio.sleep(15)
        await ctx.message.delete()
        logging(ctx.author,f"Assign {channid} on {guildid} server")
    
@commands.guild_only()
@commands.has_role("ADMIN")
@client.command(aliases=["rm","rmv"])
async def remove(ctx,Ticker):
  server_id=ctx.message.guild.id
  filename = f"listwatchlist/{str(server_id)}.json"
  with open(filename, 'r') as f:
    data_ke = json.load(f)
  cap=Ticker.upper()
  angka=len(data_ke)
  if angka>0:
    if "," in Ticker:
      nol=0
      hit=int(Ticker.count(","))
      pick=Ticker.split(",")
      with open(filename, 'r') as f:
          data_ke = json.load(f)

      while(nol<hit+1):
        dt=pick[nol].upper()
        dt2=dt.replace(" ","")
        loop=0
        while(loop<angka):
          
          if data_ke[loop]["name"]==dt2:
            chan=int(data_ke[loop]["tc_id"])
            msid=int(data_ke[loop]["msg_id"])
            nama=str(data_ke[loop]["name"])
            
            del data_ke[loop]
            with open(filename, 'w') as f:
              json.dump(data_ke, f)

            whit = discord.Embed(title="Watchlist Removal ❌",description=f"**{nama}** deleted by {ctx.author}",color=0xFF0000)
            await ctx.reply(embed=whit)
            print(f'{rminder}Rmv-W {str(nama).upper()} on <{ctx.message.guild.name} @{ctx.author}>')
            try:
              await client.http.delete_message(chan, msid) 
            except:
              pass

            with open(storage, "r") as file:
                data = json.load(file)
            x=0
            y=len(data)
            while(x<y):
                if data[x]["server"]==server_id:
                  chann=int(data[x]["chann_id"])
                  msg=int(data[x]["msg_id"])
                  req_msg=int(data[x]["req_id"])
                  try:
                    await client.http.delete_message(chann, req_msg) 
                    await client.http.delete_message(chann, msg) 
                  except:
                    pass
                  break
                else:
                    x=x+1
            logging(ctx.author,f"Removing {str(nama).upper()} on {ctx.message.guild.name}")
            break
            
          else:
            loop=loop+1
            if loop==angka-1:
              break
        nol=nol+1
        
    else:
      loop=0
      with open(filename, 'r') as f:
        data_ke = json.load(f)
      while(loop<angka):
        if data_ke[loop]["name"]==cap:
          chan=int(data_ke[loop]["tc_id"])
          msid=int(data_ke[loop]["msg_id"])
          nama=str(data_ke[loop]["name"])
          
          del data_ke[loop]
          with open(filename, 'w') as f:
            json.dump(data_ke, f)

          whit = discord.Embed(title="Watchlist Removal ❌",description=f"**{nama}** deleted by {ctx.author}",color=0xFF0000)
          await ctx.reply(embed=whit)
          print(f'{rminder}Rmv-W {str(nama).upper()} on <{ctx.message.guild.name} @{ctx.author}>')
          try:
            await client.http.delete_message(chan, msid) 
          except:
            pass
          logging(ctx.author,f"Removing {str(nama).upper()} on {ctx.message.guild.name}")
          break
        if loop==angka-1:
          whit = discord.Embed(title="Watchlist Removal ❌",description=f"{ctx.author.mention} **{cap}** Not found !",color=0xFF0000)
          await ctx.reply(embed=whit,delete_after=10)
          await asyncio.sleep(10)
          await ctx.message.delete()
          break
        else:
          loop=loop+1

      with open(storage, "r") as file:
          data = json.load(file)
      x=0
      y=len(data)
      while(x<y):
          if data[x]["server"]==server_id:
            chann=int(data[x]["chann_id"])
            msg=int(data[x]["msg_id"])
            req_msg=int(data[x]["req_id"])
            try:
              await client.http.delete_message(chann, req_msg) 
              await client.http.delete_message(chann, msg) 
            except:
              pass
            break
          else:
              x=x+1

  else:
      whit = discord.Embed(title="Watchlist Removal ❌",description=f"{ctx.author.mention} Error No Watchlist !",color=0xFF0000)
      await ctx.reply(embed=whit,delete_after=10)
      await asyncio.sleep(10)
      await ctx.message.delete()

@commands.guild_only()
@client.command()
async def price(ctx,Ticker):
    cap=Ticker.upper()
    try:
      if str(cap) == "IHSG":
        res=get_ihsg()
        hrg=res[1]
        chg=res[2]
        waktu=show_time()
        details=discord.Embed(title=f"{withname[cap]} ({cap})",description=f'Rp {hrg}\n\n> Change : {chg}\n', color=0x23ff8e)
        details.set_footer(text=f"{waktu}\nDuring trading hours, price action delayed\n")
        await ctx.reply(embed=details)
        logging(ctx.author,f"Request {cap} price")

      elif str(cap) not in withname:
        details=discord.Embed(description=f"**{cap}** not on the list, please try again !", color=0xFF0000)
        await ctx.reply(embed=details,delete_after=10)
        await asyncio.sleep(10)
        await ctx.message.delete()
      
      else:
        t1=perf_counter()
        waktu=show_time()
        prompt1=discord.Embed(title=f"{withname[cap]} ({cap})",description="Loading data",color=0x23ff8e)
        prompt1.set_footer(text=f"\nDuring trading hours, price action delayed\nRequest Time : {waktu}\nResponse Time : 0.00 s\nSource : RTI Infokom")
        msg1=await ctx.reply(embed=prompt1)
        try:
          create(cap)
          f=discord.File("chart.png")
        except:
          pass
        res=stock(cap)
        hrg=res[1]
        chg=res[2]
        prv_close=res[4]
        open=res[5]
        vol=res[6]
        turnover=res[7]
        day_range=res[8]
        t2=perf_counter()
        tcount=round(t2-t1,3)
        details=discord.Embed(title=f"{withname[cap]} ({cap})",description=f'Rp {hrg}\n\n> Change : {chg}\n> Previous : {prv_close}\n> Open : {open}\n> 1D Range : {day_range}\n> Volume : {vol}\n> Turnover : {turnover}\n', color=0x23ff8e)
        details.set_footer(text=f"\nDuring trading hours, price action delayed\nRequest Time : {waktu}\nResponse Time : {tcount} s\nSource : RTI Infokom")
        await msg1.edit(embed=details,delete_after=200)
        try :
          await ctx.reply(file=f,delete_after=200)
        except:
           pass
        logging(ctx.author,f"Request {cap} price")
        await asyncio.sleep(200)
        await ctx.message.delete()

    except:
      details=discord.Embed(description="Sorry, this feature not available right now !", color=0xFF0000)
      await ctx.reply(embed=details,delete_after=10)
      await asyncio.sleep(10)
      await ctx.message.delete()

@commands.dm_only()
@client.command()
async def see(ctx,server_id=147):
  filename = f"listwatchlist/{str(server_id)}.json"
  if ctx.author.id in admin_utama and server_id!=147:
    with open(filename, "r") as file:
        datax = json.load(file)
    if (len(datax)) == 0:
      await ctx.send("No watchlist available right now !",delete_after=15)
    else:
      nomer=1
      string=""
      string2=""
      string3=""
      for apa in datax:
          if apa["pm"]==True:
            emoji=" :sunny:"
          else:
            emoji=""
          panjang=withname[apa["name"].upper()]
          string +=f'{nomer}. {panjang} **({apa["name"]})**{emoji}\n'
          string2+=f'{apa["buy"]}\n'
          string3+=f'{apa["sell"]} **({apa["gain"]})**\n'
          nomer=nomer+1
      em=discord.Embed(title="👀",color=0x23ff8e)
      em.add_field(name="Stock Name",value=string,inline=True)
      em.add_field(name="Buy",value=string2,inline=True)
      em.add_field(name="Sell",value=string3,inline=True)
      em.set_footer(text=f"Watchlist from {str(server_id)}")
      dm = await ctx.author.create_dm()
      await dm.send(embed=em)


@commands.cooldown(2, 60, commands.BucketType.user)
@commands.dm_only()
@client.command()
async def restart(ctx):
  dm = await ctx.author.create_dm()
  if ctx.author.id in admin_utama:
    user=discord.Embed(description="Restart on process", color=0x23ff8e)
    await dm.send(embed=user)
    prv = client.get_channel("Private Channel")
    em=discord.Embed(description=f"Stonksbot received a restart command from {ctx.author}", timestamp=datetime.utcnow(), color=0x23ff8e)
    await prv.send(embed=em)
    print(f'{rminder}Restart {ctx.author}')
    os.system("pm2 restart sb")
    logging(ctx.author,"Restarting Bot")
    await asyncio.sleep(15)
    user=discord.Embed(description="Restart Failed", color=0xFF0000)
    await dm.send(embed=user)
  else:
    await dm.send(f'Sorry, this command not available for {ctx.author.mention} !')

@commands.dm_only()
@client.command()
async def cset(ctx,name):
  dm = await ctx.author.create_dm()
  if ctx.author.id in admin_utama:
    result=int(find(name.upper()))
    if result == 2222:
      user=discord.Embed(description=f"{name.upper()} this pair is not found, please try again !", color=0xFF0000)
      await dm.send(embed=user)
    else:
      user=discord.Embed(description=f"Coin display set to {name.upper()}", color=0x23ff8e)
      await dm.send(embed=user)
      f=open("listwatchlist/nama_koin.txt", "w")
      f.write(f"{result}")
      f.close()
      logging(ctx.author,f"Set coin to {name.upper()}")
  else:
    await dm.send(f'Sorry, this command not available for {ctx.author.mention} !')

@commands.dm_only()
@client.command()
async def status(ctx,condition=0):
  dm = await ctx.author.create_dm()
  if ctx.author.id in admin_utama:
    if condition==1:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name='SESSION 1'))
    elif condition==2:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name='SESSION 2'))
    elif condition==3:        
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='chart on break'))
    elif condition==4:
      while(True):
        price=str(get_price())
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{str(get_ticker())} at {price}"))
        await asyncio.sleep(10)
    else:
      instruction=discord.Embed(title="Status Details",description="1.Session 1\n2.Session 2\n3.Chart on break\n4.Crypto Price\nElse. This Status Details",color=0x23ff8e)
      instruction.set_image(url="https://i.ibb.co/vzZwjFn/sb-header-trans.png")
      await dm.send(embed=instruction)

    if condition!=0:
      logging(ctx.author,f"Status {condition} displayed") 

@commands.dm_only()
@client.command()
async def admin(ctx):
  dm = await ctx.author.create_dm()
  if ctx.author.id in admin_utama:
      instruction=discord.Embed(title="Admin Command List Details",color=0x23ff8e)
      instruction.add_field(name="Command",value=f"{prefix}news *[news]\n{prefix}broadcast\n{prefix}status [0]\n{prefix}cset [crypto]\n{prefix}download [log]\n{prefix}receive",inline=True)
      instruction.add_field(name="Command",value=f"{prefix}upload *required xlsx file\n{prefix}restart\n{prefix}change\n{prefix}see\n{prefix}reminder [on/off]",inline=True)
      instruction.set_image(url="https://i.ibb.co/vzZwjFn/sb-header-trans.png")
      await dm.send(embed=instruction)

@commands.dm_only()
@client.command()
async def news(ctx,*,berita):
  dm = await ctx.author.create_dm()
  if ctx.author.id in admin_utama:
    user=discord.Embed(description="News Saved", color=0x23ff8e)
    await dm.send(embed=user)
    f=open("berita.txt", "w")
    f.write(berita)
    f.close()

    prv = client.get_channel("Private Channel")
    em=discord.Embed(description=f"{ctx.author} set a news", timestamp=datetime.utcnow(), color=0x23ff8e)
    await prv.send(embed=em)
    logging(ctx.author,"Set news '"+berita[:50]+"....'")
    lognws(ctx.author,berita)
  else:
    await dm.send(f'Sorry, this command not available for {ctx.author.mention} !')

@commands.dm_only()
@client.command()
async def broadcast(ctx):
  dm = await ctx.author.create_dm()
  if ctx.author.id in admin_utama:
    f=open("berita.txt", "r")
    msg=f.read()
    if msg != "":
      print(f"{str(rminder)}{str(ctx.author)} broadcasted a message")
      ser=discord.Embed(description=f"News Broadcasted", color=0x23ff8e)
      p=0
      with open(datalist, "r") as file:
        datax = json.load(file)
        while(p<len(datax)):
          prv = client.get_channel(datax[p]["tc"])
          em=discord.Embed(title="Stonksbot News 📰",description=msg, color=0x23ff8e)
          await prv.send(embed=em)
          p=p+1
      p=0
      f.close()
      r=open("berita.txt","w")
      r.write("")
      r.close
      logging(ctx.author,"Broadcast news")
    else:
      ser=discord.Embed(description=f"No news", color=0xFF2D00)
    await dm.send(embed=ser)

@commands.dm_only()
@client.command()
async def reminder(ctx,toggle):
  dm = await ctx.author.create_dm()
  if ctx.author.id in admin_utama:
    if toggle=="on" or toggle == "On":
      user=discord.Embed(description=f"Reminder Turned on !\nPlease restart with ``{prefix}restart``", color=0x23ff8e)
      await dm.send(embed=user)
      f=open("reminder.txt", "w")
      f.write("On")
      f.close()
      logging(ctx.author,"Turned On Reminder")

    elif toggle=="off" or toggle=="Off":
      user=discord.Embed(description=f"Reminder Turned off !\nPlease restart with ``{prefix}restart``", color=0xFF0000)
      await dm.send(embed=user)
      f=open("reminder.txt", "w")
      f.write("Off")
      f.close()
      logging(ctx.author,"Turned Off Reminder")
  else:
    await dm.send(f'Sorry, this command not available for {ctx.author.mention} !')

@commands.dm_only()
@client.command()
async def download(ctx,series):
  dm = await ctx.author.create_dm()
  if ctx.author.id in admin_utama:
    if series=="list":
      get_coin_list()
      await dm.send(f"Data Provided by Binance at {show_time()}",file=discord.File("datacoin_stonksbot.txt"))
      logging(ctx.author,"Downloading Binance Coin List")
    elif series=="btc":
      await dm.send(f"Data Provided by Binance",file=discord.File("btc_price.txt"))
      logging(ctx.author,"Downloading BTC price")
    elif series == "eth":
      await dm.send(f"Data Provided by Binance",file=discord.File("eth_price.txt"))
      logging(ctx.author,"Downloading ETH price")
    elif series == "bnb":
      await dm.send(f"Data Provided by Binance",file=discord.File("bnb_price.txt"))
      logging(ctx.author,"Downloading BNB price")
    elif series == "sol":
      await dm.send(f"Data Provided by Binance",file=discord.File("sol_price.txt"))
      logging(ctx.author,"Downloading SOL price")
    elif series == "log":
      a_file = open("log.txt", "r")
      lines = a_file.readlines()
      last_lines = lines[-10:]
      x=0
      hsl=""
      while(x<10):
          hsl=hsl+last_lines[x]
          x=x+1
      # log=discord.Embed(title="Stonksbot Log",description=f"Data Provided at {show_time()}\n```{hsl}```",color=0x23ff8e)
      await dm.send(f"**Stonksbot User Log**\nLast 10 lines\n```{hsl}```\nData Provided at {show_time()}")
      logging(ctx.author,"Downloading Bot Log")
    else:
      await dm.send("Command error please try again!")

  else:
    await dm.send(f'Sorry, this command not available for {ctx.author.mention} !')

@commands.dm_only()
@client.command()
async def upload(ctx):
  dm = await ctx.author.create_dm()
  if ctx.author.id in admin_utama:
    if ctx.message.attachments[0].filename.endswith(".xlsx"):
      await ctx.message.attachments[0].save(fp="datasaham.xlsx")
      notif=discord.Embed(title="File Upload Success",description="File Accepted !", color=0x23ff8e)
      await dm.send(embed=notif)
      await asyncio.sleep(2)
      try:
        extract()
        notif2=discord.Embed(description="Data Extraction Success !", color=0x23ff8e)
        await dm.send(embed=notif2)
        await asyncio.sleep(2)
        await dm.send(file=discord.File("saham.py"))
        logging(ctx.author,"Updated Stock List")
      except:
        await dm.send("Extraction Failed, try again !",delete_after=5)
    else:
      notif=discord.Embed(title="File Rejected ❌",description=f"`{ctx.message.attachments[0].filename}` rejected !\nReason : Potential dangerous file", color=0xFF0000)
      await dm.send(embed=notif)

@commands.dm_only()
@client.command()
async def change(ctx,cat=0,gid=0,brp=8):
  dm = await ctx.author.create_dm()
  if ctx.author.id in admin_utama:
    if cat == 1 or cat == 2:
      back=int(mulai(gid,cat,brp))
      if back==1:
        notif=discord.Embed(description="JSON Successfully updated !",color=0x23ff8e)
      elif back==2:
        notif=discord.Embed(title="Error Occured !",description=f"``Guild {gid}`` not found !", color=0xFF0000)
    else:
      notif=discord.Embed(title="Change Database",description=f"(1) Watchlist ``{prefix}change 1 [guild id] [wl]``\n(2) Premium ``{prefix}change 2 [guild id]``",color=0x23ff8e)
    await dm.send(embed=notif)
    logging(ctx.author,f"Update Database on {gid}")
  else:
    await dm.send(f'Sorry, this command not available for {ctx.author.mention} !')

@commands.guild_only()
@client.command(aliases=["performance","gain","gainer","gainers","lose","loser","losers"])
async def perf(ctx):
  hasil=datapr()
  gain=discord.Embed(title="Daily Gainer 📈",color=0x23ff8e)
  gain.add_field(name="Stock",value=hasil[0],inline=True)
  gain.add_field(name="Gain",value=hasil[2],inline=True)
  gain.add_field(name="Last",value=hasil[1],inline=True)
  gain.set_image(url="https://i.ibb.co/vzZwjFn/sb-header-trans.png")
  gain.set_footer(text=f"\nDuring trading hours, price action delayed\nRequest Time : {show_time()}")
  
  lose=discord.Embed(title="Daily Loser 📉",color=0x23ff8e)
  lose.add_field(name="Stock",value=hasil[3],inline=True)
  lose.add_field(name="Loss",value=hasil[5],inline=True)
  lose.add_field(name="Last",value=hasil[4],inline=True)
  lose.set_image(url="https://i.ibb.co/vzZwjFn/sb-header-trans.png")
  lose.set_footer(text=f"\nDuring trading hours, price action delayed\nRequest Time : {show_time()}")
  try:
    await ctx.send(embed=gain)
    await ctx.send(embed=lose)
    logging(ctx.author,"Requesting Daily Movers")
  except:
    details=discord.Embed(description="Sorry, this feature not available right now !", color=0xFF0000)
    await ctx.reply(embed=details,delete_after=10)
    await asyncio.sleep(10)
    await ctx.message.delete()
  
@commands.dm_only()
@client.command()
async def receive(ctx):
    dm = await ctx.author.create_dm()
    ose=discord.Embed(title="Movers data update",color=0x23ff8e)
    msg1= await dm.send(embed=ose)
    os.system("node data.js")
    ose2=discord.Embed(title="Movers data update",description="Done succesfully",color=0x23ff8e)
    await msg1.edit(embed=ose2)

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
        await ctx.reply("Command not found !",delete_after=5)
        await asyncio.sleep(5)
        await ctx.message.delete()
  if isinstance(error,commands.CommandOnCooldown):
	      await ctx.send(f"{ctx.author.mention} this commands are on cooldown, please try again in the next `{round(error.retry_after, 2)} seconds`")
  if isinstance(error,commands.MissingRequiredArgument):
        parameter_name = error.param.name
        whit=discord.Embed(title="Error Occurred !", description=f"⚠ Required parameter ``{parameter_name}`` is missing", color=0xFF0000)
        await ctx.reply(embed=whit)
  if isinstance(error, commands.MissingRole):
        await ctx.reply("You don't have the permissions to use this command",delete_after=10)
        await asyncio.sleep(10)
        await ctx.message.delete()

@client.event
async def on_raw_reaction_add(payload):
  chann=payload.channel_id
  msid=payload.message_id
  emot=str(payload.emoji)
  if emot == '🗑️':
    await client.http.delete_message(chann, msid)
  else:
    return

@client.event
async def on_guild_join(guild):
  server=guild.id
  filename = f"listwatchlist/{str(server)}.json"  
  with open(filename,'w') as jsonFile:
      json.dump([], jsonFile)
  new_wl={"server":server,"chann_id":"0","msg_id":"0","req_id":"0","max_wl":8,"is_premium":False}
  with open(storage, "r") as file:
    data = json.load(file)
  data.append(new_wl)
  with open(storage, "w") as file:
    json.dump(data, file)
  prv = client.get_channel("Private Channel")
  em=discord.Embed(description=f"Stonksbot invited to {str(guild.name)}", timestamp=datetime.utcnow(), color=0x23ff8e)
  await prv.send(embed=em)
  logging("ADMIN",f"Stonksbot invited to {str(guild.name)}")
  print(f'{rminder}Invited to <{str(guild.name)}>')

@client.event
async def on_guild_remove(guild):
  server=guild.id
  filename = f"listwatchlist/{str(server)}.json"
  os.remove(filename)
  prv = client.get_channel("Private Channel")

  #delete list_server
  with open(datalist, 'r') as f:
    data_ke = json.load(f)
  p=0
  q=len(data_ke)
  while(p<q):
    if data_ke[p]["guild_id"]==server:
      del data_ke[p]
      with open(datalist, 'w') as f:
        json.dump(data_ke, f)
      break
    else:
      p=p+1

  #delete storage
  with open(storage, 'r') as f:
    data_ke = json.load(f)
  p=0
  q=len(data_ke)
  while(p<q):
    if data_ke[p]["server"]==server:
      del data_ke[p]
      with open(storage, 'w') as f:
        json.dump(data_ke, f)
      break
    else:
      p=p+1

  em=discord.Embed(description=f"Stonksbot got kick from {str(guild.name)}", timestamp=datetime.utcnow(), color=0xFF0000)
  await prv.send(embed=em)
  print(f'{rminder}Kicked <{str(guild.name)}>')
  logging("ADMIN",f"Stonksbot kicked from {str(guild.name)}")
  
client.run("TOKEN HERE")