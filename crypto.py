alphabet=list(map(chr,range(97,123)))#creates list with alphabet

def check_key(key):
    for i in (key):
        if i not in alphabet:
            raise ValueError('Invalid key')

def substitution(plain,key): #takes plain text and key and returns encrypted text using substitution
    check_key(key)
    ctr=0
    encrypted=""
    for i in plain:
        if i in alphabet:
            encrypted=encrypted+alphabet[(alphabet.index(i)+alphabet.index(key[ctr%len(key)]))%len(alphabet)]
            ctr+=1

        else:
            encrypted=encrypted+i
    return encrypted


def desubstitution(encrypted,key): #takes encrypted text and key. Returns Plain text.
    check_key(key)
    ctr=0
    decrypted=""
    for i in encrypted:
        if i in alphabet:
            decrypted=decrypted+alphabet[(alphabet.index(i)-alphabet.index(key[ctr%len(key)]))%len(alphabet)]
            ctr+=1
        else:
            decrypted=decrypted+i
    return decrypted

print(substitution('I am in Dahab','sebas'))
print(desubstitution('I sq jn Dszec','sebas'))