import json
data="./listwatchlist/list_server.json"
def sign(gid):
    with open(data, 'r') as f:
        data_ke = json.load(f)
    x=0
    y=len(data_ke)
    while(x<y):
        if data_ke[x]["guild_id"]==gid:
            return 1
        else:
            x=x+1
            if x==y:
                return 2