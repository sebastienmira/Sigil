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
- HTML, CSS and JavaScript: templates and static folder. There is some JS script within the HTML files. Mostly used to properly earn the form submissions.
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

A list of the most common letters in a large english dictionary is defined as `freq_in_dict` on the begining of the file. 