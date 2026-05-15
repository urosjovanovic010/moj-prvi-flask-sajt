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

konekcija.commit()
konekcija.close()
print("Nova arhitektura baze je spremna!")
