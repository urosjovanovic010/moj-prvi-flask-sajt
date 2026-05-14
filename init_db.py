import sqlite3
from baza import proizvodi  # Uvozimo nasu staru listu da ne kucamo rucno!

# 1. Konektujemo se na bazu (pošto fajl baza.db ne postoji, Python će ga sam napraviti!)
konekcija = sqlite3.connect('baza.db')
kursor = konekcija.cursor() # "Kursor" je naš alat koji izvršava SQL komande

# 2. Pravimo tabelu (Ovo ti je poznato iz PHP-a)
kursor.execute('''
    CREATE TABLE IF NOT EXISTS proizvodi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        naziv TEXT NOT NULL,
        cena INTEGER NOT NULL,
        slika TEXT,
        kategorija TEXT
    )
''')

# 3. Prolazimo kroz našu staru Python listu i ubacujemo svaki proizvod u SQL bazu
for p in proizvodi:
    # Pokušavamo da nađemo proizvod da ne bismo ubacili duplikate
    kursor.execute('SELECT naziv FROM proizvodi WHERE naziv = ?', (p["naziv"],))
    ako_postoji = kursor.fetchone()
    
    # Ako ga nema u bazi, ubaci ga (INSERT INTO)
    if not ako_postoji:
        kursor.execute('''
            INSERT INTO proizvodi (naziv, cena, slika, kategorija)
            VALUES (?, ?, ?, ?)
        ''', (p["naziv"], p["cena"], p["slika"], p["kategorija"]))
        print(f"Dodat proizvod u SQL bazu: {p['naziv']}")

# 4. Čuvamo (commit) promene i gasimo konekciju
konekcija.commit()
konekcija.close()

print("Bravo! Tvoja prava baza podataka je uspesno kreirana!")
