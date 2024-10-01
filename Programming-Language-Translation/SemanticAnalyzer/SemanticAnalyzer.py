import sys

ulaz = []

for linija in sys.stdin:
    if linija.strip() == "":
        break
    else:
        ulaz.append(linija.strip())

definirane = {}     # {"<ime_var>": <redak_def>}
imena = {}          # {"<ime_var>": <dubina>}

dubina = 0
l = 0
while l != len(ulaz)-1:

    if "<naredba_pridruzivanja>" in ulaz[l]:

        ind = l+2
        uhvacen_error = False
        while "<lista_naredbi>" not in ulaz[ind]:
            
            if "<P>" in ulaz[ind] and "IDN" in ulaz[ind+1]:
                if ulaz[ind+1].split(" ")[2] == ulaz[l+1].split(" ")[2] and ulaz[ind+1].split(" ")[2] not in imena:
                    print("err " + ulaz[l+1].split(" ")[1] + " " + ulaz[l+1].split(" ")[2])
                    uhvacen_error = True
                    break
             
            ind += 1
        
        if uhvacen_error:
            break

        if ulaz[l+1].split(" ")[2] not in imena.keys():
            definirane.update({ulaz[l+1].split(" ")[2] : ulaz[l+1].split(" ")[1]})
            imena.update({ulaz[l+1].split(" ")[2] : dubina})


    if "<P>" in ulaz[l] and "IDN" in ulaz[l+1]:
        if ulaz[l+1].split(" ")[2] in imena.keys():
            if imena.get(ulaz[l+1].split(" ")[2]) <= dubina:
                print(ulaz[l+1].split(" ")[1] + " " + definirane.get(ulaz[l+1].split(" ")[2]) + " " + ulaz[l+1].split(" ")[2])
        else:
            print("err " + ulaz[l+1].split(" ")[1] + " " + ulaz[l+1].split(" ")[2])
            break

    if "KR_ZA" in ulaz[l]:
        
        dubina += 1

        ind = l+2
        uhvacen_error = False
        while "<lista_naredbi>" not in ulaz[ind]:
            
            if "<P>" in ulaz[ind] and "IDN" in ulaz[ind+1]:
                if ulaz[ind+1].split(" ")[2] == ulaz[l+1].split(" ")[2]:
                    print("err " + ulaz[l+1].split(" ")[1] + " " + ulaz[l+1].split(" ")[2])
                    uhvacen_error = True
                    break
             
            ind += 1
        
        if uhvacen_error:
            break

        if ulaz[l+1].split(" ")[2] not in imena:
            
            definirane.update({ulaz[l+1].split(" ")[2] : ulaz[l+1].split(" ")[1]})
            imena.update({ulaz[l+1].split(" ")[2] : dubina})

        if ulaz[l+1].split(" ")[2] in imena:
            definirane.update({ulaz[l+1].split(" ")[2] : ulaz[l+1].split(" ")[1]})
        
    if "KR_AZ" in ulaz[l]:
        
        ukloni = []
        for key, value in imena.items():
            if value == dubina:
                ukloni.append(key)
        
        for key in ukloni:
            del imena[key]
            
        dubina -= 1

    l = l + 1
