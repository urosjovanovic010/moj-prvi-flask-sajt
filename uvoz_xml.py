import sqlite3
import xml.etree.ElementTree as ET
import glob # 1. Uvozimo glob za pretragu fajlova
import os   # 2. Uvozimo os za čitanje imena fajla
import math # <-- OVO JE NOVO

konekcija = sqlite3.connect('baza.db')
kursor = konekcija.cursor()
kursor.execute('UPDATE proizvodi SET kolicina = 0')
print("Sve zalihe u bazi resetovane na 0. Počinjemo osvežavanje...")


# 3. Skupljamo sve XML fajlove u jednu listu
svi_xml_fajlovi = glob.glob('../test/trymybike/proizvodi/*.xml')

# 4. Glavna petlja: Prolazimo kroz SVAKI pronađeni fajl
for xml_fajl in svi_xml_fajlovi:
    ime_fajla = os.path.basename(xml_fajl) # Izvlači samo ime (npr. LAZER-stock-SRB.xml)
    print(f"Započinjem uvoz iz: {ime_fajla}... 🚀")
    
    # 5. Dinamički određujemo kategoriju na osnovu imena fajla!
    if "SHIMANO" in ime_fajla:
        glavna_kategorija = "Delovi"
    else:
        glavna_kategorija = "Oprema"
        
    stablo = ET.parse(xml_fajl)
    koren = stablo.getroot()
    
    # 6. Tvoja stara petlja za proizvode SADA IDE OVDE (mora biti uvučena udesno)
    for proizvod in koren.findall('Product'):
        opis_tag = proizvod.find('Opis')
        naziv = opis_tag.text if opis_tag is not None else ''
        
        sku_tag = proizvod.find('SKU')
        sku = sku_tag.text if sku_tag is not None else ''
        
        slika_tag = proizvod.find('Slika_1')
        slika = slika_tag.text if slika_tag is not None else ''
        
        odeljak_tag = proizvod.find('Odeljak')
        odeljak = odeljak_tag.text if odeljak_tag is not None else ''
        
        kategorija_tag = proizvod.find('kategorija')
        kategorija = kategorija_tag.text if kategorija_tag is not None else ''
        
        potkategorija_tag = proizvod.find('potkategoriju')
        potkategorija = potkategorija_tag.text if potkategorija_tag is not None else ''
        
        proizvodjac_tag = proizvod.find('Proizvođač')
        proizvodjac = proizvodjac_tag.text if proizvodjac_tag is not None else ''
        
        # OBRISANO: Ono staro hardkodovano glavna_kategorija = "Oprema" (rešili smo to iznad)
        
        kolicina_tag = proizvod.find('Količina')
        kolicina_tekst = kolicina_tag.text if kolicina_tag is not None else '0'
        kolicina = int(kolicina_tekst) if kolicina_tekst else 0
        
        cena_tag = proizvod.find('VP_Cena_RSD')
        cena_tekst = cena_tag.text if cena_tag is not None else '0'
        nabavna_cena = float(cena_tekst) if cena_tekst else 0
        prodajna_cena = nabavna_cena * 1.75
        
        # NOVO: Zaokruživanje na prvu gornju deseticu (npr. 1233 u 1240)
        konacna_cena = math.ceil(prodajna_cena / 10.0) * 10
        
        if not slika: slika = 'placeholder.jpg'
            
        if naziv:
            # Pitamo bazu: "Da li već imaš proizvod sa ovim SKU kodom?"
            kursor.execute('SELECT id FROM proizvodi WHERE sku = ?', (sku,))
            postojeci = kursor.fetchone()
            
            if postojeci:
                # Proizvod postoji! Samo mu osvežavamo cenu i vraćamo pravu količinu
                kursor.execute('''
                    UPDATE proizvodi 
                    SET cena = ?, kolicina = ?
                    WHERE sku = ?
                ''', (int(konacna_cena), kolicina, sku))
            else:
                # Proizvod ne postoji! Ovo je neki potpuno novi artikal, ubacujemo ga celog
                kursor.execute('''
                    INSERT INTO proizvodi (sku, naziv, cena, slika, glavna_kategorija, odeljak, kategorija, potkategorija, proizvodjac, kolicina)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (sku, naziv, int(konacna_cena), slika, glavna_kategorija, odeljak, kategorija, potkategorija, proizvodjac, kolicina))

konekcija.commit()
konekcija.close()
print("SVI XML fajlovi su uspešno uvezeni!")
