import sqlite3
import csv

# Povezujemo se na tvoju SQLite bazu
konekcija = sqlite3.connect('baza.db')
kursor = konekcija.cursor()

# Putanja do tvog starog CSV fajla
csv_fajl = '../test/trymybike/SHIMANO-stock.csv'

uspesno_dodato = 0

print("Započinjem uvoz 4000+ artikala. Vežite se, polećemo... 🚀")

# Otvaramo CSV fajl (encoding utf-8 čuva naša slova poput č, ć, ž)
with open(csv_fajl, mode='r', encoding='utf-8') as fajl:
    # DictReader magično pretvara svaki red u rečnik koristeći imena kolona!
    citac = csv.DictReader(fajl)
    
    for red in citac:
        naziv = red['Opis']
        sku = red['SKU']
        slika = red['Slika 1']
        
        # NOVA TAKSONOMIJA (Uzeto iz CSV fajla)
        odeljak = red['Odeljak']
        kategorija = red['kategorija']
        potkategorija = red['potkategoriju'] # ovako piše u zaglavlju fajla
        proizvodjac = red['Proizvođač']
        
        # GLAVNA KATEGORIJA ZA MENI (Ručno zadajemo za ceo Shimano fajl)
        glavna_kategorija = "Delovi"
        
        kolicina_tekst = red['Količina']
        kolicina = int(kolicina_tekst) if kolicina_tekst else 0
        
        cena_tekst = red['VP Cena RSD']
        nabavna_cena = float(cena_tekst) if cena_tekst else 0
        prodajna_cena = nabavna_cena * 1.70
        
        if not slika: slika = 'placeholder.jpg'
        if not naziv: continue
            
        kursor.execute('''
            INSERT INTO proizvodi (sku, naziv, cena, slika, glavna_kategorija, odeljak, kategorija, potkategorija, proizvodjac, kolicina)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (sku, naziv, int(prodajna_cena), slika, glavna_kategorija, odeljak, kategorija, potkategorija, proizvodjac, kolicina))



# Trajno snimamo (commit) promene u bazu i zatvaramo
konekcija.commit()
konekcija.close()

print(f"Uvoz uspešno završen! U tvoju bazu je u deliću sekunde upisano {uspesno_dodato} artikala!")
