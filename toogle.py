import json
def ganti(data,x,cat,brp):
    if cat == 1:
        change={'max_wl': brp}
        print(f"Change to {brp}")
    if cat == 2:
        if data["is_premium"]==True:
            change={'is_premium': False}
        if data["is_premium"]==False:
            change={'is_premium': True}

    data.update(change)
    with open(storage, "r") as file:
        data2 = json.load(file)
    data2.append(data)
    with open(storage, "w") as file:
        del data2[x]
        json.dump(data2, file)

def cari(gid,cat,brp):
    with open(storage, 'r') as f:
        data_ke = json.load(f)
    x=0
    while(x<len(data_ke)):
        if data_ke[x]["server"]==gid:
            ganti(data_ke[x],x,cat,brp)
            return 1
        else:
            x=x+1
            if x==len(data_ke):
                return 2
                
storage="listwatchlist/storage.json"
def mulai(gid,cat,brp):
    if cat !=1:
        brp=0
    hasil=int(cari(gid,cat,brp))
    return hasil