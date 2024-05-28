import crypto

dictionary=""
with open("large.txt") as file:
    dictionary=file.read()



freqList=crypto.sortedFreq(dictionary,26)
freqInDict=[]
for i in freqList:
    freqInDict.append(i[0])

print(freqList)





'''
permutations=list(itertools.product(*lista))
print(permutations)
result=[]
for i in range(len(permutations[0])): #lenkey
    prelresult=[]
    for j in permutations: 
        ctr=0
        for k in j:
            if k>i:
                ctr=ctr+1
        if ctr==0:
            prelresult.append(j)
    for k in prelresult:
        permutations.pop(permutations.index(k))
        result.append(k)
print(permutations)
print(result)
'''