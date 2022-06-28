import csv

def writecsv():#csvファイルをSAVE
    with open("csv.csv","a",newline='') as f: 
        writer = csv.writer(f) 
        writer.writerow(["test2"])
    f.close()

writecsv()