# Sigil
#### Video Demo:  <https://youtu.be/d4QlouoNCsk>
#### Description:

This is my final project for CS50X 2024. Sigil, a web application for classical cryptography enthusiasts.

One of my favourite hobbies as a child was to crack and come up with secret codes with my friends. Sigil provides helpful tools to encrypt, decrypt and analyse messages and allows you to challenge your code-breaker friends wherever they are in the world.

The current version of the app supports Vigenere type substitution ciphers. The cryptanalytic tools are optimized for English plaintext.

In this project I tried to consolidate the different topics introduced in CS50:
- Flask: the app was developed using the Flask micro-framework.
- Algorithms: particularly of use to develop the frequency attacks.
- Python: the development of the crypto.py file which functions as a cryptography library for the application.
- HTML, CSS and JavaScript: templates and static folder. There is some JS script within the HTML files. Mostly used to properly handle the form submissions.
- Databases: Designed a database to handle the creation of users, manage different chats and messages between users.
- ...

## Features

### Encrypt
- Allows you to encrypt any text using an alphabetic key like a Vigenere cipher.

### Decrypt
- The "known" mode allows you to decrypt a text using a known (Vigenere) key.
- The "guess" mode runs a frequency analytical attack.

 The guess mode takes as input a key length and the number of attempts used to compare the letter frequency over the rows of text with the english letter frequency. It then returns a table with the most likely keys computed and the likelihood for it to be the decryption key.
 The likelihood value is the ratio between words in the text and English words.

### Analysis
- Perform a frequency analysis of the text.
- Visualise the data with tables or histograms.
- Allows the user to perform a manual analysis of the text.

### Chat
Users can create an account in Sigil and chat with eachother:
- Allows for in-chat encryption and decryption.
- Messages are encrypted before being sent.
- Allows the users the privacy of encrypted text. 
- Allows "code-breakers" to challenge eachother with their own ciphers.


## About the files in this repo

### crypto.py

The cryptographic functions were all implemented in this file which functions as a cryptography library.

A list of the most common letters in a large english dictionary is defined as `freq_in_dict` on the begining of the file. This list is latter used to performe the frequency analysis attack.

The `alphabet` list is the defined list which contains all the upper and lower case letters in english. 

The `substitution` and `desubstitution` functions are responsible for encrypting and decrypting a string with a given key (check Vigenere cipher). The function `check_key` ensures that the key is fully alphabetic. The `substitution` function adds a letter in the given plain text with its correspondant key letter, and the `desubsistution` does its inverse. Note that both this functions only affect letters in the `alphabet` list, leaving all the other characters unaltered.

The `frequencyAnalysis` function takes a string as input and returns a dictionary where its keys are the letters in the alphabet and the values are the number of occurences of that letter in the given text. `histFreqAnalysis` returns instead a histogram of the letters and its number of occurences.

The function `splitRows` splits a given text into n rows, where n (defined as `period`) is the length of the key used for Vigenere encryption. This allows us to perform a frequency analysis on the different rows of a text encrypted with different letters of the Vigenere key as will be done in the `frequencyAnalysisVigenere`. The latter function takes as input a text and a period and returns a list of frequencyAnalysis dictionaries representing the number of occurences of each letter in each row of the text. `sortedFreq` is similar to `frequencyAnalysis` but returns instead a list of the n most common letters in the text.

The function `guessVigenere` takes as input a text, a key length and a number of attempts to return a list of lists with possible keys used to encrypt the text and the respective likelihood for each of this keys to be the correct one.
Firstly it splits the text into n rows where n is the key length using the `splitRows` function. Then it calculates the x most common letters in each row of the text where x is the number of attempts. 
This is then used to compare the most common letters in each row with the most common letters in the english dictionary (check frequency analysis cryptanalysis) and returns a list of lists (a list for each row) with the letters that might have been used to encrypt each row in the text. It then computes all the possible permutations among this list to return a list with all the possible keys formed from those letter combinations.
The likelihood for each of this strings to be the actual key is then calculated. This is done by decrypting the with each of the previously calculated possible keys and comparing the words in the decrypted text with english words in a large english dictionary using `check_word`. The likelihood for each possible key is then defined as the ratio of decrypted words that exist in the emglish dictionary divided by the total number of words in the text. The keys respective likelihoods are then stored in a dictionary and sorted into a lost by likelihood.


### helpers.py

I imported two functions from the finance assignment in CS50 `apology` and `login_required`. I also stored a large dictionary of english words in this file.

### crypto.db
This is the database.
Here is the schema used to create its tables:

```
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE chats(
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
sender_id INTEGER NOT NULL,
receiver_id INTEGER NOT NULL,
FOREIGN KEY(sender_id) REFERENCES users(id),
FOREIGN KEY(receiver_id) REFERENCES users(id));
CREATE TABLE messages(
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
chat_id INTEGER NOT NULL,
sender_id INTEGER NOT NULL,
message TEXT NOT NULL,
datetime NUMERIC,
FOREIGN KEY(chat_id) REFERENCES chats(id),
FOREIGN KEY(sender_id) REFERENCES users(id)
);
```

`users` was used to store the users' username and password's hash.
`chats` stores the ids of both users in open chats.
`messages` stores the messages's encrypted text as well as datetime, id of the sender and id of the chat where the message was sent.

###
For more questions feel free to contact me.
