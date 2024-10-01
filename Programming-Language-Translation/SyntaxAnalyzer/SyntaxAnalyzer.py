import sys

def provjeri_ulaz(ulaz, p):

    if ulaz[p].split()[0] == "L_ZAGRADA" or ulaz[p].split()[0] == "KR_ZA":
        return True

# ucitavanje tablice / gramatike

tablica = {}
tablica.update({"<program>": {"IDN": 1, "KR_ZA": 1, "!": 1}})
tablica.update({"<lista_naredbi>": {"IDN": 2, "KR_ZA": 2, "KR_AZ": 3, "!": 3}})
tablica.update({"<naredba>": {"IDN": 4, "KR_ZA": 5}})
tablica.update({"<naredba_pridruzivanja>": {"IDN": 6}})
tablica.update({"<za_petlja>": {"KR_ZA": 7}})
tablica.update({"<E>": {"IDN": 8, "BROJ": 8, "OP_PLUS": 8, "OP_MINUS":8, "L_ZAGRADA": 8}})
tablica.update({"<E_lista>": {"IDN": 3, "OP_PLUS": 9, "OP_MINUS": 9, "D_ZAGRADA": 3, "KR_ZA": 3, "KR_DO": 3, "KR_AZ": 3, "!": 3}})
tablica.update({"<T>": {"IDN": 10, "BROJ": 10, "OP_PLUS": 10, "OP_MINUS": 10, "L_ZAGRADA": 10}})
tablica.update({"<T_lista>": {"IDN": 3, "OP_PLUS": 3, "OP_MINUS": 3, "OP_PUTA": 11, "OP_DIJELI": 11, "D_ZAGRADA": 3, "KR_ZA": 3, "KR_DO": 3, "KR_AZ": 3, "!": 3}})
tablica.update({"<P>": {"IDN": 14, "BROJ": 14, "OP_PLUS": 12, "OP_MINUS": 12, "L_ZAGRADA": 13}})
tablica.update({"IDN": {"IDN": 14}})
tablica.update({"OP_PRIDRUZI": {"OP_PRIDRUZI": 14}})
tablica.update({"KR_OD": {"KR_OD": 14}})
tablica.update({"KR_DO": {"KR_DO": 14}})
tablica.update({"KR_AZ": {"KR_AZ": 14}})
tablica.update({"D_ZAGRADA": {"D_ZAGRADA": 14}})

zavrsni_znakovi = ["IDN", "BROJ", "OP_PRIDRUZI", "KR_OD", "KR_DO", "KR_ZA", "KR_AZ", "L_ZAGRADA", "D_ZAGRADA", "!", "OP_PLUS", "OP_MINUS", "OP_PUTA", "OP_DIJELI"]

# MAIN

stog = []
indent_stog = []
indent_stog_special = []
lista_ispis = []

stog.append("<program>")
indent_stog.append(0)

ulaz = []


'''
while True:
    linija = input()
    if linija == "":
        break
    ulaz.append(linija)
'''

for linija in sys.stdin:
    if linija.strip() == "":
        break
    else:
        ulaz.append(linija.rstrip())

           
ulaz.append("!")

prihvacen = True
ulaz_pok = 0
pomocni = {}
razmaci = 0
while len(stog) != 0:
   
    pomocni = tablica.get(stog[-1])
    if pomocni.get(ulaz[ulaz_pok].split()[0]) == 1:
        lista_ispis.append(indent_stog[-1]*" " + stog[-1] )
        razmaci = indent_stog[-1] + 1
        stog.pop()
        indent_stog.pop()
        stog.append("<lista_naredbi>")
        indent_stog.append(razmaci)
    
    elif pomocni.get(ulaz[ulaz_pok].split()[0]) == 2:
        lista_ispis.append(indent_stog[-1]*" " + stog[-1] )
        razmaci = indent_stog[-1] + 1
        stog.pop()
        indent_stog.pop()
        stog.append("<lista_naredbi>")
        indent_stog.append(razmaci)
        stog.append("<naredba>")
        indent_stog.append(razmaci)

    elif pomocni.get(ulaz[ulaz_pok].split()[0]) == 3:
        lista_ispis.append(indent_stog[-1]*" " + stog[-1] )
        lista_ispis.append(indent_stog[-1]*" " + " $")
        stog.pop()
        indent_stog.pop()
    
    elif pomocni.get(ulaz[ulaz_pok].split()[0]) == 4:
        lista_ispis.append(indent_stog[-1]*" " + stog[-1] )
        razmaci = indent_stog[-1] + 1
        stog.pop()
        indent_stog.pop()
        stog.append("<naredba_pridruzivanja>")
        indent_stog.append(razmaci)        

    elif pomocni.get(ulaz[ulaz_pok].split()[0]) == 5:
        lista_ispis.append(indent_stog[-1]*" " + stog[-1] )
        razmaci = indent_stog[-1] + 1
        stog.pop()
        indent_stog.pop()
        stog.append("<za_petlja>")
        indent_stog.append(razmaci)       

    elif pomocni.get(ulaz[ulaz_pok].split()[0]) == 6:
        lista_ispis.append(indent_stog[-1]*" " + stog[-1] )
        razmaci = indent_stog[-1] + 1
        stog.pop()
        indent_stog.pop()
        stog.append("<E>")
        indent_stog.append(razmaci)
        stog.append("OP_PRIDRUZI")
        indent_stog.append(razmaci)
        if provjeri_ulaz(ulaz, ulaz_pok):
            indent_stog_special.append(indent_stog[-1]) 
        lista_ispis.append(indent_stog[-1]*" " + ulaz[ulaz_pok]  )
        ulaz_pok += 1

    elif pomocni.get(ulaz[ulaz_pok].split()[0]) == 7:
        lista_ispis.append(indent_stog[-1]*" " + stog[-1]  )
        razmaci = indent_stog[-1] + 1
        stog.pop()
        indent_stog.pop()
        stog.append("KR_AZ")
        indent_stog.append(razmaci)
        stog.append("<lista_naredbi>")
        indent_stog.append(razmaci)
        stog.append("<E>")
        indent_stog.append(razmaci)
        stog.append("KR_DO")
        indent_stog.append(razmaci)
        stog.append("<E>")
        indent_stog.append(razmaci)
        stog.append("KR_OD")
        indent_stog.append(razmaci)
        stog.append("IDN")
        indent_stog.append(razmaci) 
        if provjeri_ulaz(ulaz, ulaz_pok):
            indent_stog_special.append(indent_stog[-1])
        lista_ispis.append(indent_stog[-1]*" " + ulaz[ulaz_pok]  )
        ulaz_pok += 1

    elif pomocni.get(ulaz[ulaz_pok].split()[0]) == 8:    
        lista_ispis.append(indent_stog[-1]*" " + stog[-1] )
        razmaci = indent_stog[-1] + 1
        stog.pop()
        indent_stog.pop()
        stog.append("<E_lista>")
        indent_stog.append(razmaci)
        stog.append("<T>")
        indent_stog.append(razmaci)

    elif pomocni.get(ulaz[ulaz_pok].split()[0]) == 9:
        lista_ispis.append(indent_stog[-1]*" " + stog[-1] )
        razmaci = indent_stog[-1] + 1
        stog.pop()
        indent_stog.pop()
        stog.append("<E>")
        indent_stog.append(razmaci) 
        if provjeri_ulaz(ulaz, ulaz_pok):
            indent_stog_special.append(indent_stog[-1])
        lista_ispis.append(indent_stog[-1]*" " + ulaz[ulaz_pok] )
        ulaz_pok += 1

    elif pomocni.get(ulaz[ulaz_pok].split()[0]) == 10:
        lista_ispis.append(indent_stog[-1]*" " + stog[-1] )
        razmaci = indent_stog[-1] + 1
        stog.pop()
        indent_stog.pop()
        stog.append("<T_lista>")
        indent_stog.append(razmaci)
        stog.append("<P>")
        indent_stog.append(razmaci)

    elif pomocni.get(ulaz[ulaz_pok].split()[0]) == 11:
        lista_ispis.append(indent_stog[-1]*" " + stog[-1] )
        razmaci = indent_stog[-1] + 1
        stog.pop()
        indent_stog.pop()
        stog.append("<T>")
        indent_stog.append(razmaci)
        if provjeri_ulaz(ulaz, ulaz_pok):
            indent_stog_special.append(indent_stog[-1])
        lista_ispis.append(indent_stog[-1]*" " + ulaz[ulaz_pok] )
        ulaz_pok += 1

    elif pomocni.get(ulaz[ulaz_pok].split()[0]) == 12:
        lista_ispis.append(indent_stog[-1]*" " + stog[-1] )
        razmaci = indent_stog[-1] + 1
        stog.pop()
        indent_stog.pop()
        stog.append("<P>")
        indent_stog.append(razmaci)
        if provjeri_ulaz(ulaz, ulaz_pok):
            indent_stog_special.append(indent_stog[-1])
        lista_ispis.append(indent_stog[-1]*" " + ulaz[ulaz_pok])
        ulaz_pok += 1
    
    elif pomocni.get(ulaz[ulaz_pok].split()[0]) == 13:
        lista_ispis.append(indent_stog[-1]*" " + stog[-1])
        razmaci = indent_stog[-1] + 1
        stog.pop()
        indent_stog.pop()
        stog.append("D_ZAGRADA")
        indent_stog.append(razmaci)
        stog.append("<E>")
        indent_stog.append(razmaci)
        if provjeri_ulaz(ulaz, ulaz_pok):
            indent_stog_special.append(indent_stog[-1])
        lista_ispis.append(indent_stog[-1]*" " + ulaz[ulaz_pok])
        ulaz_pok += 1

    elif pomocni.get(ulaz[ulaz_pok].split()[0]) == 14:
        if stog[-1].strip() == "<P>":
            lista_ispis.append(indent_stog[-1]*" " + stog[-1])
            razmaci = indent_stog[-1] + 1
            stog.pop()
            indent_stog.pop()
            if provjeri_ulaz(ulaz, ulaz_pok):
                indent_stog_special.append(indent_stog[-1])
            lista_ispis.append(razmaci*" " + ulaz[ulaz_pok])
            ulaz_pok += 1
        else:
            razmaci = indent_stog[-1] + 1
            stog.pop()
            indent_stog.pop()
            if ulaz[ulaz_pok].split()[0] == "KR_AZ" or ulaz[ulaz_pok].split()[0] == "D_ZAGRADA":
                lista_ispis.append(indent_stog_special[-1]*" " + ulaz[ulaz_pok])
                indent_stog_special.pop()
            else:
                lista_ispis.append(indent_stog[-1]*" " + ulaz[ulaz_pok])
            ulaz_pok += 1
    
    else:
        if ulaz[ulaz_pok].split()[0] == "!" or ulaz[ulaz_pok].split()[0] == "KR_AZ": 
            print("err kraj")
        else:
            print("err " + ulaz[ulaz_pok])
        prihvacen = False
        break
    

if prihvacen:
    for i in lista_ispis:
        print(i)


