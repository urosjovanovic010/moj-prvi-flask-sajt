from flask import Flask, render_template, request
import sqlite3



app = Flask(__name__)

@app.route('/')
def home():
    moje_ime = "Uros"
    
    # 1. Povezujemo se na bazu
    konekcija = sqlite3.connect('baza.db')
    konekcija.row_factory = sqlite3.Row # Magija: tera SQLite da nam vrati podatke kao rečnike, da ne menjamo HTML!
    kursor = konekcija.cursor()
    
    # 2. Čupamo SVE proizvode (ovo ti je poznato)
    kursor.execute('SELECT * FROM proizvodi')
    proizvodi_iz_baze = kursor.fetchall()
    
    # 3. Zatvaramo vezu (važno da ne zagušimo server)
    konekcija.close()
    
    return render_template('pocetna.html', moje_ime=moje_ime, proizvodi=proizvodi_iz_baze)

@app.route('/o-nama')
def onama():
    return render_template('o-nama.html')

@app.route('/proizvod/<int:id>')
def detalji_proizvoda(id):
    konekcija = sqlite3.connect('baza.db')
    konekcija.row_factory = sqlite3.Row
    kursor = konekcija.cursor()
    
    # Čupamo SAMO JEDAN proizvod gde se ID poklapa (umesto FOR petlje!)
    kursor.execute('SELECT * FROM proizvodi WHERE id = ?', (id,))
    izabrani_proizvod = kursor.fetchone()
    
    konekcija.close()
    
    # Ako ga nema u bazi
    if izabrani_proizvod is None:
        return render_template("404.html"), 404
        
    # Ako postoji, prosleđujemo ga u HTML
    return render_template('proizvod.html', proizvod=izabrani_proizvod)

@app.route('/kontakt', methods=['GET', 'POST'])
def kontakt():
    # Ako korisnik KLIKNE na dugme za slanje (POST)
    if request.method == 'POST':
        # Čitamo podatke po njihovom "name" atributu iz HTML-a
        korisnik_ime = request.form['ime']
        korisnik_poruka = request.form['poruka']
        
        # Za sada ćemo ih samo odštampati u tvom terminalu da vidimo da li radi
        print(f"NOVA PORUKA! Ime: {korisnik_ime} | Poruka: {korisnik_poruka}")
        
        # Vraćamo isti templejt, ali mu šaljemo signal da je poruka poslata i ime korisnika
        return render_template('kontakt.html', uspesno_poslato=True, korisnik=korisnik_ime)

        
    # Ako korisnik samo OTVARA stranicu normalno (GET)
    return render_template('kontakt.html')



if __name__ == '__main__':
    app.run(debug=True)

