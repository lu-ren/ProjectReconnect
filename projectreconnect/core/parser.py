import csv
import numpy as np

def parse23andme(data):
    #load in the 23andme raw data
    raw = []
    for eachLine in data.readlines():
        eachLine = eachLine.decode('ascii')
        eachLine=eachLine.strip().split("\t")
        raw.append(eachLine)
    raw = raw[20:]
    x = sorted(raw, key=lambda x: x[0], reverse=False)

    #load in the reference frequency list
    ref = []    
    with open('scripts/Reference_Frequency_384.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            ref.append(row)

    cur = 0
    result = []
    #do the data extraction
    cur = 0
    for i in range(0,384):
        for j in range(0,len(raw)):
            if ref[i][0] != raw[j][0]:
                continue
            else:
                if raw[j][3][0] == ref[i][1] and raw[j][3][1] == ref[i][1] :
                    result.append('0')
                elif raw[j][3][0] != ref[i][1] and raw[j][3][1] != ref[i][1] :
                    result.append('2')
                elif raw[j][3][0] == ref[i][1] and raw[j][3][1] != ref[i][1] :
                    result.append('1')
                elif raw[j][3][0] != ref[i][1] and raw[j][3][1] == ref[i][1] :
                    result.append('1')
                else:
                    result.append('9')
                break

    result = "".join(result)
    return result
