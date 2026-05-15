import sqlite3
import xml.etree.ElementTree as ET # Ugrađena Python biblioteka za XML "drveće"

konekcija = sqlite3.connect('baza.db')
kursor = konekcija.cursor()

xml_fajl = '../test/trymybike/proizvodi/CATEYE-stock-SRB.xml'
uspesno_dodato = 0

print("Započinjem uvoz XML podataka (Oprema)... 🌳")

# Parsiramo (učitavamo) celo stablo XML dokumenta
stablo = ET.parse(xml_fajl)
koren = stablo.getroot()  # Ovo hvata onaj glavni <Products> tag

# Prolazimo kroz svaku granu (svaki <Product> tag)
for proizvod in koren.findall('Product'):
    opis_tag = proizvod.find('Opis')
    naziv = opis_tag.text if opis_tag is not None else ''
    
    sku_tag = proizvod.find('SKU')
    sku = sku_tag.text if sku_tag is not None else ''
    
    slika_tag = proizvod.find('Slika_1')
    slika = slika_tag.text if slika_tag is not None else ''
    
    # NOVA TAKSONOMIJA (Uzeto iz XML tagova)
    odeljak_tag = proizvod.find('Odeljak')
    odeljak = odeljak_tag.text if odeljak_tag is not None else ''
    
    kategorija_tag = proizvod.find('kategorija')
    kategorija = kategorija_tag.text if kategorija_tag is not None else ''
    
    potkategorija_tag = proizvod.find('potkategoriju')
    potkategorija = potkategorija_tag.text if potkategorija_tag is not None else ''
    
    proizvodjac_tag = proizvod.find('Proizvođač')
    proizvodjac = proizvodjac_tag.text if proizvodjac_tag is not None else ''
    
    # GLAVNA KATEGORIJA ZA MENI (Ručno zadajemo za ceo Cateye fajl)
    glavna_kategorija = "Oprema"
    
    kolicina_tag = proizvod.find('Količina')
    kolicina_tekst = kolicina_tag.text if kolicina_tag is not None else '0'
    kolicina = int(kolicina_tekst) if kolicina_tekst else 0
    
    cena_tag = proizvod.find('VP_Cena_RSD')
    cena_tekst = cena_tag.text if cena_tag is not None else '0'
    nabavna_cena = float(cena_tekst) if cena_tekst else 0
    prodajna_cena = nabavna_cena * 1.70
    
    if not slika: slika = 'placeholder.jpg'
        
    if naziv:
        kursor.execute('''
            INSERT INTO proizvodi (sku, naziv, cena, slika, glavna_kategorija, odeljak, kategorija, potkategorija, proizvodjac, kolicina)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (sku, naziv, int(prodajna_cena), slika, glavna_kategorija, odeljak, kategorija, potkategorija, proizvodjac, kolicina))



# MALA POPRAVKA: Sve Shimano artikle koje smo uvezli prošli put pretvaramo u "Delovi"
kursor.execute("UPDATE proizvodi SET kategorija = 'Delovi' WHERE kategorija != 'Oprema' AND kategorija != 'delovi' AND kategorija != 'oprema'")

konekcija.commit()
konekcija.close()

print(f"XML uvoz završen! Dodato {uspesno_dodato} artikala Opreme, a stari popravljeni na 'Delovi'!")
