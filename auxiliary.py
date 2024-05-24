import crypto

dictionary=""
with open("large.txt") as file:
    dictionary=file.read()



freqList=crypto.sortedFreq(dictionary,26)
freqInDict=[]
for i in freqList:
    freqInDict.append(i[0])

print(freqList)