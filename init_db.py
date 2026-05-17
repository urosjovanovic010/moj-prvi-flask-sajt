import sqlite3

konekcija = sqlite3.connect('baza.db')
kursor = konekcija.cursor()

# Pravimo tabelu sa svim nivoima kategorija
kursor.execute('''
    CREATE TABLE IF NOT EXISTS proizvodi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT,
        naziv TEXT NOT NULL,
        cena INTEGER NOT NULL,
        slika TEXT,
        glavna_kategorija TEXT,
        odeljak TEXT,
        kategorija TEXT,
        potkategorija TEXT,
        proizvodjac TEXT,
        kolicina INTEGER
    )
''')

# Pravimo novu tabelu za čuvanje porudžbina
kursor.execute('DROP TABLE IF EXISTS porudzbine')
kursor.execute('''
    CREATE TABLE IF NOT EXISTS porudzbine (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ime_prezime TEXT NOT NULL,
        adresa TEXT NOT NULL,
        grad TEXT NOT NULL,
        postanski_broj TEXT NOT NULL,
        telefon TEXT NOT NULL,
        email TEXT NOT NULL,
        napomena TEXT,
        proizvodi_tekst TEXT NOT NULL,
        ukupna_cena INTEGER NOT NULL,
        dostava INTEGER NOT NULL,
        status TEXT DEFAULT 'Na čekanju',
        datum DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')


konekcija.commit()
konekcija.close()
print("Nova arhitektura baze je spremna!")
