import re
import matplotlib.pyplot as plt
import itertools
import numpy as np

freq_in_dict=['e', 'i', 's', 'a', 'r', 'n', 't', 'o', 'l', 'c', 'u', 'd', 'm', 'p', 'g', 'h', 'b', 'y', 'f', 'v', 'z', 'k', 'w', 'x', 'j', 'q']#most common letters in large.txt



alphabet=list(map(chr,range(97,123)))#creates list with alphabet

def check_key(key):#key validity check
    for i in (key):
        if i not in alphabet:
            raise ValueError('Invalid key')

def substitution(plain,key): #takes plain text and key and returns encrypted text using substitution
    plain=plain.lower()
    key=key.lower()
    
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
    encrypted=encrypted.lower()
    key=key.lower()

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

def frequencyAnalysis(encrypted,normalize=False): #analyzes frequency of each letter in text
    frequencies = {letter: 0 for letter in alphabet}
    for letter in alphabet:
        frequencies[letter]=len(re.findall(letter,encrypted))
    if normalize==True:
        frequencies.values={i/sum(frequencies.values()) for i in frequencies.values()}
    return frequencies
        

def histFreqAnalysis(encrypted, normalize=False): #histogram for frquency analysis
    freqAnalysis=frequencyAnalysis(encrypted)
    frequencies=[]
    for i in alphabet:
       frequencies.append(freqAnalysis[i])
    if normalize==True:
        frequencies=[i/sum(frequencies) for i in frequencies]
    fig=plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(alphabet,frequencies, linestyle='',marker='')
    ax.stairs(frequencies, color='black')
    return fig


def splitRows(text,period): #split text into rows to perform vigenere frequency analysis or permutation ciphers
    rows=[]
    ctr=0
    for i in range(period):#intialize rows
        rows.append("")
    for i in text:
        if i in alphabet:
            rows[ctr%(period)]=rows[ctr%(period)]+i
            ctr+=1
    return rows

def frequencyAnalysisVigenere(text, period): #period is key length
    frequencyList=[] #list of dictionaries
    for i in splitRows(text,period):
        frequencyList.append(frequencyAnalysis(i))
    return frequencyList

def sortedFreq(text, n=5): #n most common letters in text
    freq=frequencyAnalysis(text)
    sortedFreq=sorted(freq.items(),key=lambda x:x[1], reverse=True)
    return sortedFreq[:n]


def guessCaeser(text, attempts=1, show_message=True):#compares frequency with dictionary to decrypt caeser encryption
    mostfreq=sortedFreq(text,attempts)
    possibilities=[]
    for i in mostfreq:
        key=alphabet[alphabet.index(i[0])-alphabet.index(freq_in_dict[0])]
        if show_message:
            message=desubstitution(text,key)
            possibilities.append([key,message])
        else:
            possibilities.append(key)

    return possibilities
    

def guessVigenere(text, key_length, attempts=1):
    rows=splitRows(text, key_length)
    keyguess=[] #list of lists with the most frequent words in each row
    for i in rows:
        mostfreq=sortedFreq(i,attempts)
        keyletter=[]
        for i in range(attempts):
            keyletter.append(alphabet[alphabet.index(mostfreq[i][0])-alphabet.index(freq_in_dict[0])])
        keyguess.append(keyletter)
    
    possiblekeys=[] #list of strings possible keys resulting of the permutation of keyguess
    possibilities=list(itertools.product(*keyguess)) #all possible permutations
    for i in possibilities:
        key=""
        for j in range(key_length):
            key=key+i[j]
        possiblekeys.append(key)
    return possiblekeys


def permutation(lista):
    result=[]
    for i in range(len(lista[0])): #lenkey
        prelresult=[]
        for j in lista: 
            ctr=0
            for k in range(len(j)):
                if k>i:
                    ctr=ctr+1
            if ctr==0:
                prelresult.append(j)
        for k in prelresult:
            lista.pop(lista.index(k))
            result.append(k)
    return result
             
'''
texto='The Rosetta Stone is a stele composed of granodiorite inscribed with three versions of a decree issued in Memphis, Egypt, in 196 BC during the Ptolemaic dynasty on behalf of King Ptolemy V Epiphanes. The top and middle texts are in Ancient Egyptian using hieroglyphic and Demotic scripts respectively, while the bottom is in Ancient Greek. The decree has only minor differences between the three versions, making the Rosetta Stone key to deciphering the Egyptian scripts. The stone was carved during the Hellenistic period and is believed to have originally been displayed within a temple, possibly at Sais. It was probably moved in late antiquity or during the Mamluk period, and was eventually used as building material in the construction of Fort Julien near the town of Rashid (Rosetta) in the Nile Delta. It was found there in July 1799 by French officer Pierre-François Bouchard during the Napoleonic campaign in Egypt. It was the first Ancient Egyptian bilingual text recovered in modern times, and it aroused widespread public interest with its potential to decipher this previously untranslated hieroglyphic script. Lithographic copies and plaster casts soon began circulating among European museums and scholars. When the British defeated the French they took the stone to London under the Capitulation of Alexandria in 1801. Since 1802, it has been on public display at the British Museum almost continuously and it is the most visited object.'

text=substitution(texto,'ghada')
'''
#print(list(itertools.product(*guessVigenere(text,5,2))))

#print(permutation(list(itertools.product(*guessVigenere(text,5,2)))))
#print(permutation([[0,1],[0,1]]))
#ray=np.zeros(10, dtype=int)
#ray[0]=1
#print(ray)

'''
dictionary=""
with open("large.txt") as file:
    dictionary=file.read()

histFreqAnalysis(dictionary,True).savefig("freqDictionary.jpg")
print(frequencyAnalysis(dictionary,True))
'''


'''
print(splitRows("abcd efghi",3))
for i in splitRows("abcd efghi",3):
    histFreqAnalysis(i)
print(substitution('I am in Dahab','sebas'))
print(desubstitution('I sq jn Dszec','sebas'))
texto='The Rosetta Stone is a stele composed of granodiorite inscribed with three versions of a decree issued in Memphis, Egypt, in 196 BC during the Ptolemaic dynasty on behalf of King Ptolemy V Epiphanes. The top and middle texts are in Ancient Egyptian using hieroglyphic and Demotic scripts respectively, while the bottom is in Ancient Greek. The decree has only minor differences between the three versions, making the Rosetta Stone key to deciphering the Egyptian scripts. The stone was carved during the Hellenistic period and is believed to have originally been displayed within a temple, possibly at Sais. It was probably moved in late antiquity or during the Mamluk period, and was eventually used as building material in the construction of Fort Julien near the town of Rashid (Rosetta) in the Nile Delta. It was found there in July 1799 by French officer Pierre-François Bouchard during the Napoleonic campaign in Egypt. It was the first Ancient Egyptian bilingual text recovered in modern times, and it aroused widespread public interest with its potential to decipher this previously untranslated hieroglyphic script. Lithographic copies and plaster casts soon began circulating among European museums and scholars. When the British defeated the French they took the stone to London under the Capitulation of Alexandria in 1801. Since 1802, it has been on public display at the British Museum almost continuously and it is the most visited object.'

print(frequencyAnalysis(texto))

histFreqAnalysis(texto).savefig("a.jpg")
'''


