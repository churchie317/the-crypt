import string
import random

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """

    inFile = open(WORDLIST_FILENAME, 'r', 0)
    line = inFile.readline()
    wordlist = line.split()
    return wordlist

wordlist = load_words()

def strip_word(word):

    word = word.lower()
    
    for i in word:
        if i in string.digits or i in string.punctuation or i == " ":
            word = word.replace(i, "")

    return word

def is_word(wordlist, word):

    word = word.lower()
    
    for i in word:
        if i in string.digits or i in string.punctuation or i == " ":
            word = word.replace(i, "")

    return word in wordlist

def build_coder(shift):

    cipher = {}
    alpha = '!"#$%&\'()*+,-./:;<=>?@[]^_`{}~' + string.ascii_lowercase + " " + string.digits + string.ascii_uppercase
    
    shift = shift % 93

    counter = 0
    for i in range(len(alpha)):
        cipher[alpha[i]] = cipher.get(alpha[i], alpha[counter + shift])
        counter += 1
        if counter == (93 - shift):
            counter = 0 - shift
            
    return cipher

def build_encoder(shift):

    cipher_text = build_coder(shift)
    
    return cipher_text

def build_decoder(shift):

    shift = (shift % 93) * -1
    decipher_text = build_coder(shift)
    
    return decipher_text

def apply_coder(text, coder):

    code = ""
    
    for i in text:
        code += coder.get(i, i)
        
    return code
    
def apply_shift(text, shift):

    cipher_text = apply_coder(text, build_encoder(shift))
    
    return cipher_text
   
def find_best_shift(wordlist, text):

    best_shift = [0, 0]
    best_shift_test = [0, 0]
    best_word = ["", 0]
    
    for i in range(93):
        plain_text = apply_coder(text, build_decoder(i))
        plain_text_split = plain_text.split()
        for j in range(len(plain_text_split)):
            if is_word(wordlist, string.lower(plain_text_split[j])):
                best_shift_test[1] += 1
                if len(strip_word(plain_text_split[j])) > len(best_word[0]):
                    best_word[0] = strip_word(plain_text_split[j])
                    best_word[1] = i
                    best_shift[0] = best_word[1]
                    best_shift[1] = best_shift_test[1]
            else:
                break
        if best_shift_test[1] > best_shift[1]:
            best_shift[0] = i
            best_shift[1] = best_shift_test[1]    
        best_shift_test[1] = 0

    return best_shift[0]
   
def create_rand_shifts(text):

    shifts = [(0, random.randint(1, 93))]
    
    for i in range(len(text)):
        if text[i] == " ":
            shifts.append(((i + 1), random.randint(1, 93)))

    return shifts

def apply_shifts(text, shifts):

    cipher_text = ""
    counter = 0
    shift = 0
    cipher_portion = ""
    
    for i in range(len(shifts)):
        shift = shifts[i][1]
        cipher_portion = apply_coder(text[shifts[i][0]:], build_coder(shift))
        cipher_text = cipher_text[:shifts[i][0]] + cipher_portion
        cipher_portion = ""
        counter += 1
                      
    return cipher_text

def multi_layer_decryption_sol_rec(wordlist, text, start):

    plain_text = apply_coder(text[start:], build_decoder(find_best_shift(wordlist, text[start:])))

    if " " in plain_text:
        check_word = string.lower(plain_text[:plain_text.find(" ")])
        for i in string.punctuation:
            if i in check_word:
                check_word = check_word.replace(i, "")
    else:
        check_word = plain_text

    if " " in plain_text and is_word(wordlist, check_word):
        start = plain_text.find(" ") + 1
        return plain_text[:plain_text.find(" ")] + " " + multi_layer_decryption_sol_rec(wordlist, plain_text, start)
    else:
        return plain_text

def apply_encryption(text):
    
    encrypted_text = apply_shifts(text, create_rand_shifts(text))    

    print ""
    print string.center("-" * 80, 80)
    print "Encrypting, please be patient..."

    plain_text = apply_decryption(encrypted_text)

    while plain_text != text:
        encrypted_text = apply_shifts(text, create_rand_shifts(text))    
        plain_text = apply_decryption(encrypted_text)

    return encrypted_text
            

def apply_decryption(text):
    
    decrypted_text = multi_layer_decryption_sol_rec(wordlist, text, 0)

    return decrypted_text

def encrypt_decrypt_program_start():

    print string.center("-" * 80, 80)
    print "Remember, not all messages are capable of encryption. Before transmitting an"
    print "encrypted message, ensure that it was successfully encrypted."
    print string.center("-" * 80, 80)
    
    test = True
    while test == True:

        print ""
        print 'Type "encrypt" to encrypt a message, "decrypt" to decrypt a message, or "q" to'
        print "quit."
        
        test1 = True
        while test1 == True:
            user_input = str(raw_input(""))
            if user_input == "encrypt" or user_input == "decrypt" or user_input == "q" or user_input == "quit":
                test1 = False
            else:
                print ""
                print "ERROR: INVALID SELECTION."
                print ""
                print 'Type "encrypt" to encrypt a message or "decrypt" to decrypt a message.'

        if user_input == "encrypt":
            print ""
            plain_text = str(raw_input("Please enter the plain text: "))
            encrypted_text = apply_encryption(plain_text)
            print ""
            print "Encrypted text:", encrypted_text
            print string.center("-" * 80, 80)

        if user_input == "decrypt":
            print ""
            encrypted_text = str(raw_input("Please enter the encrypted text: "))
            decrypted_text = apply_decryption(encrypted_text)
            print ""
            print string.center("-" * 80, 80)
            print "Decrypted text:", decrypted_text
            print string.center("-" * 80, 80)

        if user_input == "q" or user_input == "quit":
            break

encrypt_decrypt_program_start()
