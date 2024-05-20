import re
import matplotlib.pyplot as plt


alphabet=list(map(chr,range(97,123)))#creates list with alphabet

def check_key(key):#key validity check
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

def frequencyAnalysis(encrypted):
    frequencies = {letter: 0 for letter in alphabet}
    for letter in alphabet:
        frequencies[letter]=len(re.findall(letter,encrypted))
    return frequencies
        

def histFreqAnalysis(encrypted):
    freqAnalysis=frequencyAnalysis(encrypted)
    frequencies=[]
    for i in alphabet:
       frequencies.append(freqAnalysis[i])
    fig=plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(alphabet,frequencies, linestyle='',marker='')
    ax.stairs(frequencies, color='black')
    return fig

print(substitution('I am in Dahab','sebas'))
print(desubstitution('I sq jn Dszec','sebas'))
texto='The Rosetta Stone is a stele composed of granodiorite inscribed with three versions of a decree issued in Memphis, Egypt, in 196 BC during the Ptolemaic dynasty on behalf of King Ptolemy V Epiphanes. The top and middle texts are in Ancient Egyptian using hieroglyphic and Demotic scripts respectively, while the bottom is in Ancient Greek. The decree has only minor differences between the three versions, making the Rosetta Stone key to deciphering the Egyptian scripts. The stone was carved during the Hellenistic period and is believed to have originally been displayed within a temple, possibly at Sais. It was probably moved in late antiquity or during the Mamluk period, and was eventually used as building material in the construction of Fort Julien near the town of Rashid (Rosetta) in the Nile Delta. It was found there in July 1799 by French officer Pierre-François Bouchard during the Napoleonic campaign in Egypt. It was the first Ancient Egyptian bilingual text recovered in modern times, and it aroused widespread public interest with its potential to decipher this previously untranslated hieroglyphic script. Lithographic copies and plaster casts soon began circulating among European museums and scholars. When the British defeated the French they took the stone to London under the Capitulation of Alexandria in 1801. Since 1802, it has been on public display at the British Museum almost continuously and it is the most visited object.'

print(frequencyAnalysis(texto))
histFreqAnalysis(texto).savefig("a.jpg")