import json
from threading import Thread
def ganti(data,x,cat,brp):
    if cat == 1:
        change={'max_wl': brp}
        print(f"Change to {brp}")
    if cat == 2:
        if data["is_premium"]==True:
            change={'is_premium': False}
            print("Change to False")
        if data["is_premium"]==False:
            change={'is_premium': True}
            print("Change to True")

    data.update(change)


    with open("storage.json", "r") as file:
        data2 = json.load(file)
    data2.append(data)
    with open("storage.json", "w") as file:
        del data2[x]
        json.dump(data2, file)

def cari(gid,cat,brp):
    with open("storage.json", 'r') as f:
        data_ke = json.load(f)
    x=0

    while(x<len(data_ke)):
        if data_ke[x]["server"]==gid:
            print(f"Data Found at {x}")
            ganti(data_ke[x],x,cat,brp)
            print("Append Success")
            break
        else:
            x=x+1
            if x==len(data_ke):
                print("No Data")
def mulai():
    cat=int(input("Ganti apa :\n(1)Change watchlist\n(2)Toogle Premium\n"))
    if cat == 1:
        brp=int(input("Change WL to : "))
    else:
        brp=0
    gid=int(input("Search Guild ID : "))
    t1 = Thread(target=cari(gid,cat,brp))
    t1.start()