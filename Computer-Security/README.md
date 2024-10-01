
# Computer Security Laboratory Assignment - Password Manager


## How to Run
The program is run on Ubuntu Linux 22.04 system in Terminal,
using the following commands:

```
$ chmod +x password-manager.py
$ mv password-manager.py manager
```

These commands will allow running the program in Terminal.
The program is used with commands as demonstrated below:

```
$ ./manager init mAsterPasswrd  // initialize password manager
Password manager initialized.
$ ./manager put mAsterPasswrd www.fer.hr pasSwrD123  // store new password for website
Stored password for www.fer.hr.
$ ./manager get mAsterPasswrd www.fer.hr  // retrieve password for website
Password for www.fer.hr is: pasSwrD123.
$ ./manager get wrongPasswrd www.fer.hr  // example of wrong master password
Master password incorrect or integrity check failed. 
```

## Specification

The *scrypt* function is used to derive the key, which receives a *salt* of 32 random bytes, and the master password.

For each new data received, a new key is derived.

To protect user data, the AES-GCM method is used, which provides confidentiality and integrity, which means that an attacker cannot determine any information about the data, as well as change the recorded data seamlessly.

These methods ensure the fulfillment of security requirements and safe storage of user data.