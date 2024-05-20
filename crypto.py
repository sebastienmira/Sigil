alphabet=list(map(chr,range(97,123)))#creates list with alphabet
print(alphabet)

'''
def get_key(key): #take string and get numerical key as a list of integers
    numkey=[]
    for i in list(key):
        numkey.append(alphabet.index(i))
    return numkey

print(get_key('cat'))
'''

def encrypt(plain,key): #takes plain text and key and returns encrypted text
    ctr=0
    encrypted=[]
    for i in plain:
        if i in alphabet:
            encrypted.append(alphabet[(alphabet.index(i)+alphabet.index(key[ctr%len(key)]))%len(alphabet)])
            ctr+=1

        else:
            encrypted.append(i)
    str=""
    crypt=str.join(encrypted)
    return crypt

print(encrypt('aaaa','ac'))