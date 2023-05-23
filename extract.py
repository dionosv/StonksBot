import glob, os, openpyxl

# os.chdir("C:/Users/ASUS TUF/Desktop/all bot/stonksbot")
def extract():
    os.chdir(".")

    for file in glob.glob("*.xlsx"):
        data=file

    wrkbk = openpyxl.load_workbook(data)
    sh = wrkbk.active

    ticker=[]
    nama=[]
    for row in sh.iter_rows(min_row=3, min_col=2, max_row=888, max_col=2):
        for cell in row:
            txt=str(cell.value)
            if txt == "None":
                break
            else:
                ticker.append(txt)

    for row in sh.iter_rows(min_row=3, min_col=3, max_row=888, max_col=3):
        for cell in row:
            txt=str(cell.value)
            if txt == "None":
                break
            else:
                nama.append(txt)


    new_file = open('saham.py', 'w')
    file_object = open('saham.py', 'a')

    file_object.write("withname={")
    c=1
    while(c<len(nama)):
        masuk=(f'"{ticker[c]}":"{nama[c].replace(".","")}",\n')
        file_object.write(masuk)
        c=c+1
    file_object.write('"IHSG":"Indeks Harga Saham Gabungan"}')
    file_object.close()
    print("Extract Successfull !")