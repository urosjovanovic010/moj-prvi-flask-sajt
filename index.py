from flask import Flask, render_template, request

from baza import proizvodi


app = Flask(__name__)

@app.route('/')
def home():
    moje_ime="Uros"
    
    return render_template('pocetna.html',moje_ime=moje_ime, proizvodi=proizvodi)

@app.route('/o-nama')
def onama():
    return render_template('o-nama.html')

@app.route('/proizvod/<int:id>')
def detalji_proizvoda(id):
    # Pravimo praznu promenljivu u koju ćemo smestiti nađen proizvod
    izabrani_proizvod = None
    
    # Prolazimo kroz našu "bazu"
    for p in proizvodi:
        if p["id"] == id:
            izabrani_proizvod = p  # Pronašli smo ga!
            break  # Zaustavljamo petlju jer smo našli šta tražimo
            
    # Ako proizvod sa tim ID-jem ne postoji (npr. neko ukuca /proizvod/99)
    if izabrani_proizvod == None:
        return render_template("404.html"), 404
        
    # Ako postoji, prosleđujemo ga u novi HTML templejt
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

