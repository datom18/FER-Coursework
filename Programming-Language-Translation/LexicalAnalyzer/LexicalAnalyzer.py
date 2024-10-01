import sys

def provjeri(rijec, br_linije):
    if rijec == "za":
          print("KR_ZA {} za".format(br_linije))
    if rijec == "od":
          print("KR_OD {} od".format(br_linije))
    if rijec == "do":
          print("KR_DO {} do".format(br_linije))
    if rijec == "az":
          print("KR_AZ {} az".format(br_linije))
    if rijec.isdigit():
         print("BROJ {} {}".format(br_linije, rijec))  
    if rijec == "=":
         print("OP_PRIDRUZI {} =".format(br_linije))
    if rijec == "+":
         print("OP_PLUS {} +".format(br_linije))
    if rijec == "-":
         print("OP_MINUS {} -".format(br_linije))
    if rijec == "*":
         print("OP_PUTA {} *".format(br_linije))
    if rijec == "/":
         print("OP_DIJELI {} /".format(br_linije))
    if rijec == "(":
         print("L_ZAGRADA {} (".format(br_linije))  
    if rijec == ")":
         print("D_ZAGRADA {} )".format(br_linije))


def provjera_pocetak_brojem(rijec, br_linije):
      
      if rijec.isalnum() and not rijec.isdigit() and rijec[0].isdigit():
         broj = ""
         idn = ""
         c = 0
         for l in rijec:
            c += 1 
            if l.isdigit():
               broj += l
            else:
               print("BROJ {} {}".format(br_linije, broj))
               idn += l
               break
         for l in rijec[c:]:
            idn += l

         print("IDN {} {}".format(br_linije, idn))




linije = []
kljucne_rijeci = ["za", "od", "do", "az"]
znakovi = ["=", "+", "-", "*", "/", "(", ")"]


prazne_linije = 0
while True:
    linija = sys.stdin.readline().strip()
    if linija == "":
        prazne_linije += 1
        linije.append(linija)
        if prazne_linije == 2:
            break
    else:
        linije.append(linija)
        prazne_linije = 0


br_linije = 0
for linija in linije:
    br_linije += 1
    split_lista = linija.split()
    for rijec in split_lista:
      if "//" in rijec:
        if rijec.startswith("//") or rijec == "//":
            break
        else:
            indeks = 0
            for i in rijec:
                indeks += 1
                if i == "/":
                    break
            rijec = rijec[0:indeks-1]        
      if rijec == "za":
          print("KR_ZA {} za".format(br_linije))
      if rijec == "od":
          print("KR_OD {} od".format(br_linije))
      if rijec == "do":
          print("KR_DO {} do".format(br_linije))
      if rijec == "az":
          print("KR_AZ {} az".format(br_linije))
      if rijec.isdigit():
         print("BROJ {} {}".format(br_linije, rijec))  
      if rijec == "=":
         print("OP_PRIDRUZI {} =".format(br_linije))
      if rijec == "+":
         print("OP_PLUS {} +".format(br_linije))
      if rijec == "-":
         print("OP_MINUS {} -".format(br_linije))
      if rijec == "*":
         print("OP_PUTA {} *".format(br_linije))
      if rijec == "/":
         print("OP_DIJELI {} /".format(br_linije))
      if rijec == "(":
         print("L_ZAGRADA {} (".format(br_linije))  
      if rijec == ")":
         print("D_ZAGRADA {} )".format(br_linije))
      if rijec.isalnum() and rijec[0].isalpha() and not rijec.isdigit() and rijec not in kljucne_rijeci:
         print("IDN {} {}".format(br_linije, rijec))
      
 
      if rijec.isalnum() and not rijec.isdigit() and rijec[0].isdigit():
        provjera_pocetak_brojem(rijec, br_linije)


      #SLUCAJEVI NPR i*i*i  
      if not rijec.isalnum() and rijec not in znakovi:
         nova_rijec = ""
         c = 0
         for l in rijec:
            c += 1
            if l.isalnum():
               nova_rijec += l
               if c == len(rijec) and nova_rijec != "":
                    if nova_rijec.isalnum() and not nova_rijec.isdigit() and nova_rijec[0].isdigit():
                        provjera_pocetak_brojem(nova_rijec, br_linije)
                    elif nova_rijec.isdigit():
                        print("BROJ {} {}".format(br_linije, nova_rijec))                     
                    else:
                        print("IDN {} {}".format(br_linije, nova_rijec))
            else:
               if nova_rijec == "":
                  provjeri(l, br_linije)
               else:
                  
                  if nova_rijec.isalnum() and not nova_rijec.isdigit() and nova_rijec[0].isdigit():
                        provjera_pocetak_brojem(nova_rijec, br_linije)
                  elif nova_rijec.isdigit():
                        print("BROJ {} {}".format(br_linije, nova_rijec))                          
                  else:
                        print("IDN {} {}".format(br_linije, nova_rijec))
                  nova_rijec = ""
                  provjeri(l, br_linije)

