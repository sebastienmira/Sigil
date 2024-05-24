import re
import matplotlib.pyplot as plt

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
    return 

def sortedFreq(text, n=5): #n most common letters in text
    freq=frequencyAnalysis(text)
    sortedFreq=sorted(freq.items(),key=lambda x:x[1], reverse=True)
    return sortedFreq[:n]


def guessCaeser(text, attempts=1):#compares frequency with dictionary to decrypt caeser encryption
    mostfreq=sortedFreq(text,attempts)
    possibilities=[]
    for i in mostfreq:
        key=alphabet[alphabet.index(i[0])-alphabet.index(freq_in_dict[0])]
        message=desubstitution(text,key)
        possibilities.append([message,key])
    return possibilities
    
'''
def guessVigenere(text, attempts=1)
'''




    

'''
texto='The Rosetta Stone is a stele composed of granodiorite inscribed with three versions of a decree issued in Memphis, Egypt, in 196 BC during the Ptolemaic dynasty on behalf of King Ptolemy V Epiphanes. The top and middle texts are in Ancient Egyptian using hieroglyphic and Demotic scripts respectively, while the bottom is in Ancient Greek. The decree has only minor differences between the three versions, making the Rosetta Stone key to deciphering the Egyptian scripts. The stone was carved during the Hellenistic period and is believed to have originally been displayed within a temple, possibly at Sais. It was probably moved in late antiquity or during the Mamluk period, and was eventually used as building material in the construction of Fort Julien near the town of Rashid (Rosetta) in the Nile Delta. It was found there in July 1799 by French officer Pierre-François Bouchard during the Napoleonic campaign in Egypt. It was the first Ancient Egyptian bilingual text recovered in modern times, and it aroused widespread public interest with its potential to decipher this previously untranslated hieroglyphic script. Lithographic copies and plaster casts soon began circulating among European museums and scholars. When the British defeated the French they took the stone to London under the Capitulation of Alexandria in 1801. Since 1802, it has been on public display at the British Museum almost continuously and it is the most visited object.'

text="vjg tqugvvc uvqpg ku c uvgng eqorqugf qh itcpqfkqtkvg kpuetkdgf ykvj vjtgg xgtukqpu qh c fgetgg kuuwgf kp ogorjku, giarv, kp 196 de fwtkpi vjg rvqngocke fapcuva qp dgjcnh qh mkpi rvqngoa x grkrjcpgu. vjg vqr cpf okffng vgzvu ctg kp cpekgpv giarvkcp wukpi jkgtqinarjke cpf fgoqvke uetkrvu tgurgevkxgna, yjkng vjg dqvvqo ku kp cpekgpv itggm. vjg fgetgg jcu qpna okpqt fkhhgtgpegu dgvyggp vjg vjtgg xgtukqpu, ocmkpi vjg tqugvvc uvqpg mga vq fgekrjgtkpi vjg giarvkcp uetkrvu. vjg uvqpg ycu ectxgf fwtkpi vjg jgnngpkuvke rgtkqf cpf ku dgnkgxgf vq jcxg qtkikpcnna dggp fkurncagf ykvjkp c vgorng, rquukdna cv ucku. kv ycu rtqdcdna oqxgf kp ncvg cpvkswkva qt fwtkpi vjg oconwm rgtkqf, cpf ycu gxgpvwcnna wugf cu dwknfkpi ocvgtkcn kp vjg eqpuvtwevkqp qh hqtv lwnkgp pgct vjg vqyp qh tcujkf (tqugvvc) kp vjg pkng fgnvc. kv ycu hqwpf vjgtg kp lwna 1799 da htgpej qhhkegt rkgttg-htcpçqku dqwejctf fwtkpi vjg pcrqngqpke ecorckip kp giarv. kv ycu vjg hktuv cpekgpv giarvkcp dknkpiwcn vgzv tgeqxgtgf kp oqfgtp vkogu, cpf kv ctqwugf ykfgurtgcf rwdnke kpvgtguv ykvj kvu rqvgpvkcn vq fgekrjgt vjku rtgxkqwuna wpvtcpuncvgf jkgtqinarjke uetkrv. nkvjqitcrjke eqrkgu cpf rncuvgt ecuvu uqqp dgicp ektewncvkpi coqpi gwtqrgcp owugwou cpf uejqnctu. yjgp vjg dtkvkuj fghgcvgf vjg htgpej vjga vqqm vjg uvqpg vq nqpfqp wpfgt vjg ecrkvwncvkqp qh cngzcpftkc kp 1801. ukpeg 1802, kv jcu dggp qp rwdnke fkurnca cv vjg dtkvkuj owugwo cnoquv eqpvkpwqwuna cpf kv ku vjg oquv xkukvgf qdlgev."
print(guessCaeser(text,1))

print(sortedFreq(texto))
'''


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


