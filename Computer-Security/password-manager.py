#!/usr/bin/env python3


from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
import sys


def encryptData(password, data):

    db = open("database.bin", "r")
    lines = db.readlines() 

    if len(lines) != 0:
        result = findExistingSite(password, "random_text")
        if result is False:
            return False
        if result != -1:
            removeLine(result)

    website = data.split(" ")[0]
    if len(lines) != 0:
        result = findExistingSite(password, website)
        if result is False:
            return False
        if result != -1:  
            removeLine(result)
    db.close()

    db = open("database.bin", "a")
    salt = get_random_bytes(32)
    key = scrypt(password, salt, key_len=32, N=2**14, r=8, p=1)
    db.write(salt.hex())
    cipher = AES.new(key, AES.MODE_GCM)
    ciphered_data = cipher.encrypt(data.encode("utf-8"))
    db.write(cipher.nonce.hex())
    passVerification = cipher.digest()
    db.write(passVerification.hex())
    db.write(ciphered_data.hex() + '\n')
    db.close()
    return True

def decryptData(password, website):
    db = open("database.bin", "r")
    fetchedPass = ""
    lines = db.readlines()
    for line in lines:
        try:
            line_bytes = bytes.fromhex(line)
            salt = line_bytes[:32]
            nonce = line_bytes[32:48]
            passVerification = line_bytes[48:64]
            encryptedData = line_bytes[64:]

            key = scrypt(password, salt, key_len=32, N=2**14, r=8, p=1)
            cipher = AES.new(key, AES.MODE_GCM, nonce)
            decryptedData = cipher.decrypt(encryptedData)
            decryptedData = decryptedData.decode("utf-8")
            cipher.verify(passVerification)
            if decryptedData.split(" ")[0] == website:
                fetchedPass = decryptedData.split(" ")[1]

        except ValueError as e:
            return False

    db.close()
    return fetchedPass


def findExistingSite(password, website):
    db = open("database.bin", "r")
    lines = db.readlines()
    lineNum = 0
    result = -1
    for line in lines:
        try:
            line_bytes = bytes.fromhex(line)
            salt = line_bytes[:32]
            nonce = line_bytes[32:48]
            passVerification = line_bytes[48:64]
            encryptedData = line_bytes[64:]

            key = scrypt(password, salt, key_len=32, N=2**14, r=8, p=1)
            cipher = AES.new(key, AES.MODE_GCM, nonce)
            decryptedData = cipher.decrypt(encryptedData)
            decryptedData = decryptedData.decode("utf-8")
            cipher.verify(passVerification)
            if decryptedData.split(" ")[0] == website:
                result = lineNum

        except ValueError as e:
            return False
        
        lineNum += 1
    
    db.close()
    return result

def removeLine(line):
    db = open("database.bin", "r")
    lines = db.readlines()
    del lines[line]
    db.close()
    
    db = open("database.bin", "w")
    db.writelines(lines)
    db.close()


# read input from console
wantedFunc = sys.argv[1]

#initialization
if wantedFunc == "init":
    db = open("database.bin", "w")
    masterPass = sys.argv[2]
    res = encryptData(masterPass, "random_text")
    db.close()
    print("Password manager initialized.")

if wantedFunc == "put":
    masterPass = sys.argv[2]
    website = sys.argv[3]
    webPass = sys.argv[4]
    data = website + " " + webPass 
    result = encryptData(masterPass, data)
    if result:
        print("Stored password for " + website)
    else:
        print("Wrong master password or integrity check failed.")

if wantedFunc == "get":
    masterPass = sys.argv[2]
    website = sys.argv[3]
    fetchedPass = decryptData(masterPass, website)
    if fetchedPass is False:
        print("Wrong master password or integrity check failed.")
    elif fetchedPass == "":
        print("Wrong master password or integrity check failed.")
    else:
        print("Password for " + website + " is: " + fetchedPass)
