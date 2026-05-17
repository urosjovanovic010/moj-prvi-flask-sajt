from flask import Flask, render_template, request, redirect, session
import sqlite3
import re # NOVO: Biblioteka za čišćenje teksta

SINONIMI = [
    ['pedala', 'pedale', 'pedalo', 'pedals'],
    ['patike', 'patika', 'cipele', 'cipela', 'obuca', 'obuća', 'shoes', 'shoe'],
    ['rucice kocnica', 'rucica kocnice', 'ručice kočnica', 'ručica kočnice', 'brake lever', 'brake levers'],
    ['kocnica', 'kocnice', 'kocnicu', 'kočnica', 'kočnice', 'kočnicu', 'brake', 'brakes'],
    ['drzac bidona', 'držač bidona', 'korpica bidona', 'nosac bidona', 'nosač bidona', 'bottle cage', 'bottle holder'],
    ['nabla', 'nable', 'glavcina', 'glavcine', 'glavčina', 'glavčine', 'hub', 'hubs'],
    ['srednji pogon', 'pogon', 'pogoni', 'kurbla', 'kurble', 'crankset', 'crank'],
    ['zadnji menjac', 'zadnji menjač', 'menjac zadnji', 'menjač zadnji', 'rear derailleur'],
    ['prednji menjac', 'prednji menjač', 'menjac prednji', 'menjač prednji', 'front derailleur'],
    ['menjac', 'menjaci', 'menjač', 'menjači', 'derailleur', 'shifter'],
    ['lanac', 'lanci', 'chain', 'chains'],
    ['guma', 'gume', 'spoljna guma', 'unutrasnja guma', 'tire', 'tires', 'tube', 'tubes'],
    ['tocak', 'tockovi', 'točak', 'točkovi', 'wheel', 'wheels'],
    ['sediste', 'sedista', 'sedište', 'sedišta', 'sic', 'sedlo', 'sedla', 'saddle', 'seat'],
    ['kaciga', 'kacige', 'helmet', 'helmets'],
    ['lancanik', 'lancanici', 'lančanik', 'lančanici', 'kaseta', 'cassette', 'sprocket'],
    ['sajla', 'sajle', 'cable', 'cables'],
    ['buzir', 'buziri', 'bužir', 'bužiri', 'housing'],
    ['paknovi', 'pakne', 'plocice', 'pločice', 'plocice za disk kocnice', 'pločice za disk kočnice', 'plocice za disk', 'pločice za disk', 'disk plocice', 'disk pločice', 'brake pads', 'pads'],
    ['volan', 'volani', 'korman', 'upravljac', 'upravljač', 'handlebar', 'handlebars'],
    ['lula', 'lule', 'stem', 'stems'],
    ['sticna', 'sticne', 'šticna', 'šticne', 'cev sedla', 'cevi sedla', 'seatpost', 'seatposts'],
    ['selna sedla', 'šelna sedla', 'selna sedalne cevi', 'šelna sedalne cevi', 'zatvarac sticne', 'zatvarač šticne', 'seatpost clamp', 'selna', 'šelna'],
    ['srednja glava', 'patrona', 'osovina', 'bottom bracket'],
    ['gripovi', 'rucke', 'ručke', 'traka volana', 'grips', 'bar tape'],
    ['rotor', 'rotori', 'disk', 'diskovi', 'disc rotor'],
    ['felna', 'felne', 'obruc', 'obruči', 'obruci', 'zica', 'žica', 'zbice', 'žbice', 'rim', 'spokes'],
    ['kuka menjaca', 'kuka menjača', 'nosac menjaca', 'nosač menjača', 'derailleur hanger'],
    ['svetlo', 'svetla', 'lampa', 'lampe', 'light', 'lights', 'zadnje svetlo', 'prednje svetlo'],
    ['alat', 'alati', 'kljuc', 'ključ', 'kljucevi', 'ključeve', 'biciklisticki alat', 'biciklistički alat', 'alat za bicikl', 'alat za bicikle', 'tool', 'tools']
]

app = Flask(__name__)
# OBAVEZNO ZA SESIJE: Flask mora da ima "ključ" kojim kriptuje podatke o korisniku
app.secret_key = 'moja_super_tajna_sifra_za_korpu_123'

# --- GLOBALNA FUNKCIJA ZA SVE STRANICE ---
# Ovo nam omogućava da HTML na svakoj stranici zna koliko imamo u korpi!
@app.context_processor
def inject_korpa():
    broj_artikala = 0
    if 'korpa' in session:
        broj_artikala = sum(session['korpa'].values()) # Sabira sve količine iz korpe
    return dict(broj_artikala_u_korpi=broj_artikala)

# --- RUTA ZA DODAVANJE U KORPU ---
@app.route('/dodaj_u_korpu/<int:id>')
def dodaj_u_korpu(id):
    # Ako korisnik tek došao i nema korpu, mi mu pravimo praznu: {}
    if 'korpa' not in session:
        session['korpa'] = {}
        
    id_str = str(id) # Sesije više vole stringove nego brojeve
    
    # Ako već ima taj proizvod u korpi, samo mu dodajemo +1 na količinu
    if id_str in session['korpa']:
        session['korpa'][id_str] += 1
    # Ako nema, dodajemo ga i količina je 1
    else:
        session['korpa'][id_str] = 1
        
    # Flask mora da zna da smo menjali sesiju da bi je sačuvao!
    session.modified = True 
    
    # Vraćamo ga na stranicu sa koje je kliknuo na dugme (request.referrer)
    return redirect(request.referrer or '/')

# --- NAŠ CUSTOM JINJA FILTER ZA SEO URL-ove ---
def napravi_slug(tekst):
    tekst = str(tekst).lower() # Sve u mala slova
    # Menjamo naša slova u "ošišanu" latinicu
    tekst = tekst.replace('š', 's').replace('đ', 'dj').replace('č', 'c').replace('ć', 'c').replace('ž', 'z')
    # Sve što nije slovo ili broj (npr. razmaci, zarezi) pretvaramo u jednu crticu
    tekst = re.sub(r'[^a-z0-9]+', '-', tekst)
    return tekst.strip('-') # Sklanjamo crtice sa krajeva
# Registrujemo ovu funkciju kao filter koji ćemo zvati "slugify" u HTML-u!
app.jinja_env.filters['slugify'] = napravi_slug

@app.route('/')
def home():
    moje_ime = "Uros"
    
    # 1. Povezujemo se na bazu
    konekcija = sqlite3.connect('baza.db')
    konekcija.row_factory = sqlite3.Row # Magija: tera SQLite da nam vrati podatke kao rečnike, da ne menjamo HTML!
    kursor = konekcija.cursor()
    
    # 2. Čupamo SVE proizvode (ovo ti je poznato)
        # NOVO: Čupamo 6 nasumičnih proizvoda za početnu!
    kursor.execute('SELECT * FROM proizvodi WHERE kolicina > 0 ORDER BY RANDOM() LIMIT 6')


    proizvodi_iz_baze = kursor.fetchall()
    
    # 3. Zatvaramo vezu (važno da ne zagušimo server)
    konekcija.close()
    
    return render_template('pocetna.html', moje_ime=moje_ime, proizvodi=proizvodi_iz_baze)

# Pametna ruta koja hvata tekst iz URL-a (npr. /kategorija/Oprema)
@app.route('/kategorija/<ime_kategorije>')
def kategorija(ime_kategorije):
    izabrani_odeljak = request.args.get('odeljak')
    izabrana_kategorija = request.args.get('kategorija') 
    izabrana_potkategorija = request.args.get('potkategorija') # 1. Hvatamo treći nivo!

    konekcija = sqlite3.connect('baza.db')
    konekcija.row_factory = sqlite3.Row
    kursor = konekcija.cursor()
    
    # --- GRADIMO UPIT ZA PROIZVODE ---
    upit = 'SELECT * FROM proizvodi WHERE glavna_kategorija = ? AND kolicina > 0'
    parametri = [ime_kategorije]
    
    if izabrani_odeljak:
        upit += ' AND odeljak = ?'
        parametri.append(izabrani_odeljak)
        
    if izabrana_kategorija:
        upit += ' AND kategorija = ?'
        parametri.append(izabrana_kategorija)
        
    if izabrana_potkategorija: # 2. Filtriramo proizvode i po trećem nivou!
        upit += ' AND potkategorija = ?'
        parametri.append(izabrana_potkategorija)
        
    upit += ' LIMIT 24'
    
    kursor.execute(upit, tuple(parametri))
    proizvodi_iz_baze = kursor.fetchall()
    
    # --- ČUPAMO MENIJE IZ BAZE ---
    kursor.execute('SELECT DISTINCT odeljak FROM proizvodi WHERE glavna_kategorija = ? AND odeljak != "" AND kolicina > 0', (ime_kategorije,))
    svi_odeljci = kursor.fetchall()
    
    sve_kategorije = []
    if izabrani_odeljak:
        kursor.execute('SELECT DISTINCT kategorija FROM proizvodi WHERE glavna_kategorija = ? AND odeljak = ? AND kategorija != "" AND kolicina > 0', (ime_kategorije, izabrani_odeljak))
        sve_kategorije = kursor.fetchall()
        
    sve_potkategorije = []
    if izabrana_kategorija: # 3. Čupamo potkategorije samo za izabranu kategoriju!
        kursor.execute('SELECT DISTINCT potkategorija FROM proizvodi WHERE glavna_kategorija = ? AND odeljak = ? AND kategorija = ? AND potkategorija != "" AND kolicina > 0', (ime_kategorije, izabrani_odeljak, izabrana_kategorija))
        sve_potkategorije = kursor.fetchall()
        
    konekcija.close()
    
    return render_template(
        'pocetna.html', 
        proizvodi=proizvodi_iz_baze, 
        moje_ime="Uros", 
        odeljci=svi_odeljci, 
        trenutna_kategorija=ime_kategorije,
        izabrani_odeljak=izabrani_odeljak,
        izabrana_kategorija=izabrana_kategorija,
        izabrana_potkategorija=izabrana_potkategorija,
        kategorije=sve_kategorije,
        potkategorije=sve_potkategorije
    )




@app.route('/o-nama')
def onama():
    return render_template('o-nama.html')

# NOVO: Rutu skraćujemo na /p/ i dodajemo joj <slug> tekst na kraju
@app.route('/p/<int:id>/<sku>/<slug>')
def detalji_proizvoda(id, sku, slug):
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

@app.route('/pretraga')
def pretraga():
    trazena_rec = request.args.get('q', '').strip()
    # Hvatamo stranu iz URL-a (npr. ?q=menjac&strana=2). Ako nema, podrazumevamo da je 1.
    trenutna_strana = request.args.get('strana', 1, type=int) 
    PROIZVODA_PO_STRANI = 18
    
    if not trazena_rec:  
        return redirect('/')
        
    trazena_rec_mala = trazena_rec.lower()
    sve_reci_za_pretragu = [trazena_rec_mala]
    
    for grupa in SINONIMI:
        if trazena_rec_mala in grupa:
            sve_reci_za_pretragu = grupa
            break
            
    konekcija = sqlite3.connect('baza.db')
    konekcija.row_factory = sqlite3.Row
    kursor = konekcija.cursor()
    
    uslovi = []
    parametri = []
    
    for rec in sve_reci_za_pretragu:
        uslovi.append("(naziv LIKE ? OR sku LIKE ?)")
        # HAK: SQLite ne ume da pretvori velika Č,Ć,Ž,Š,Đ u mala kad radi LIKE. 
        # Zato ta slova menjamo u "_" što u SQL-u znači "bilo koje jedno slovo"!
        rec_sigurna_za_bazu = rec.replace('č', '_').replace('ć', '_').replace('ž', '_').replace('š', '_').replace('đ', '_')
        parametri.extend([f"%{rec_sigurna_za_bazu}%", f"%{rec_sigurna_za_bazu}%"])
        
    sql_uslovi = " OR ".join(uslovi)
    
    # KORAK 1: Pitamo bazu koliko UKUPNO ima ovakvih proizvoda (bez limita)
    upit_za_brojanje = f"SELECT COUNT(*) FROM proizvodi WHERE ({sql_uslovi}) AND kolicina > 0"
    kursor.execute(upit_za_brojanje, tuple(parametri))
    ukupan_broj_proizvoda = kursor.fetchone()[0] # Izvlačimo samo taj jedan broj
    
    # Računamo koliko nam ukupno stranica treba (ako imamo 20 proizvoda podeljeno sa 18, treba nam 2 stranice)
    import math
    ukupno_strana = math.ceil(ukupan_broj_proizvoda / PROIZVODA_PO_STRANI)
    
    # KORAK 2: Izvlačimo samo proizvode ZA OVU STRANU (OFFSET i LIMIT)
    preskok = (trenutna_strana - 1) * PROIZVODA_PO_STRANI
    
    upit = f"SELECT * FROM proizvodi WHERE ({sql_uslovi}) AND kolicina > 0 LIMIT ? OFFSET ?"
    # Dodajemo Limit i Offset na kraj liste parametara
    parametri.extend([PROIZVODA_PO_STRANI, preskok]) 
    
    kursor.execute(upit, tuple(parametri))
    nadzeni_proizvodi = kursor.fetchall()
    konekcija.close()
    
    # Šaljemo sve to u HTML da bismo dole mogli da nacrtamo brojeve stranica
    return render_template(
        'pocetna.html',
        proizvodi=nadzeni_proizvodi,
        trenutna_kategorija=f'Rezultati pretrage: "{trazena_rec}"',
        odeljci=[{'odeljak': 'Svi rezultati'}],
        trenutna_strana=trenutna_strana,
        ukupno_strana=ukupno_strana,
        trazena_rec=trazena_rec # Šaljemo i traženu reč nazad da bismo znali šta da dodamo na linkove dugmića
    )

@app.route('/korpa')
def korpa():
    # Ako je korpa prazna ili ne postoji
    if 'korpa' not in session or not session['korpa']:
        return render_template('korpa.html', proizvodi=[], ukupna_cena=0)
        
    id_ovi = list(session['korpa'].keys())
    # Pravimo string za SQL "IN" komandu, npr: "12, 45, 88"
    id_string = ",".join(id_ovi)
    
    konekcija = sqlite3.connect('baza.db')
    konekcija.row_factory = sqlite3.Row
    kursor = konekcija.cursor()
    
    # Izvlačimo sve te proizvode odjednom
    kursor.execute(f"SELECT * FROM proizvodi WHERE id IN ({id_string})")
    proizvodi_iz_baze = kursor.fetchall()
    konekcija.close()
    
    proizvodi_u_korpi = []
    ukupna_cena = 0
    
    for p in proizvodi_iz_baze:
        id_str = str(p['id'])
        kolicina = session['korpa'][id_str]
        cena = p['cena']
        ukupno_za_ovaj = cena * kolicina
        ukupna_cena += ukupno_za_ovaj
        
        # Pravimo rečnik koji spaja podatke iz baze sa količinom iz sesije
        proizvodi_u_korpi.append({
            'id': p['id'],
            'naziv': p['naziv'],
            'slika': p['slika'],
            'cena': cena,
            'kolicina': kolicina,
            'ukupno': ukupno_za_ovaj,
            'slug': napravi_slug(p['naziv'])
        })
        
    dostava = 0 if ukupna_cena >= 10000 else 700
    return render_template('korpa.html', proizvodi=proizvodi_u_korpi, ukupna_cena=ukupna_cena, dostava=dostava)

@app.route('/izbaci_iz_korpe/<int:id>')
def izbaci_iz_korpe(id):
    id_str = str(id)
    if 'korpa' in session and id_str in session['korpa']:
        del session['korpa'][id_str]
        session.modified = True
    # Kada ga izbaci, vrati korisnika nazad na stranicu korpe
    return redirect(url_for('korpa'))

@app.route('/placanje', methods=['GET', 'POST'])
def placanje():
    # 1. Ako je korpa prazna, vraćamo ga nazad
    if 'korpa' not in session or not session['korpa']:
        return redirect(url_for('korpa'))

    # 2. Isto kao u korpi, računamo cenu
    id_ovi = list(session['korpa'].keys())
    id_string = ",".join(id_ovi)
    
    konekcija = sqlite3.connect('baza.db')
    konekcija.row_factory = sqlite3.Row
    kursor = konekcija.cursor()
    
    kursor.execute(f"SELECT * FROM proizvodi WHERE id IN ({id_string})")
    proizvodi_iz_baze = kursor.fetchall()
    
    ukupna_cena = 0
    opis_narudzbine_lista = [] # Ovde skupljamo tekst: "Lanac (2 kom.)"
    
    for p in proizvodi_iz_baze:
        id_str = str(p['id'])
        kolicina = session['korpa'][id_str]
        ukupna_cena += p['cena'] * kolicina
        # Spajamo naziv i količinu
        opis_narudzbine_lista.append(f"{p['naziv']} ({kolicina} kom.)")
        
    # Pretvaramo celu listu u jedan dugačak tekst odvojen uspravnom crtom
    proizvodi_tekst = " | ".join(opis_narudzbine_lista)
    dostava = 0 if ukupna_cena >= 10000 else 700
    
    # 3. KADA KORISNIK KLIKNE "NARUČI" (POST)
    if request.method == 'POST':
        ime_prezime = request.form['ime_prezime']
        adresa = request.form['adresa']
        grad = request.form['grad']
        postanski_broj = request.form['postanski_broj']
        telefon = request.form['telefon']
        email = request.form['email']
        napomena = request.form.get('napomena', '')
        
        # Ovde bi u realnom sistemu išla funkcija za slanje na email (npr. Flask-Mail)
        print(f"--- [SISTEM] Email za potvrdu je spreman za slanje na: {email} ---")
        
        # Upisujemo u onu našu novu tabelu 'porudzbine'
        kursor.execute('''
            INSERT INTO porudzbine (ime_prezime, adresa, grad, postanski_broj, telefon, email, napomena, proizvodi_tekst, ukupna_cena, dostava)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (ime_prezime, adresa, grad, postanski_broj, telefon, email, napomena, proizvodi_tekst, ukupna_cena, dostava))
        konekcija.commit()
        konekcija.close()
        
        # ISPRAZNI KORPU NAKON KUPOVINE!
        session['korpa'] = {}
        session.modified = True
        
        # Prikaži mu stranicu da je sve prošlo ok
        return render_template('uspesno.html')
        
    konekcija.close()
    
    # 4. KADA KORISNIK SAMO OTVARA STRANICU (GET)
    return render_template('placanje.html', ukupna_cena=ukupna_cena, dostava=dostava)

@app.route('/o-nama')
def o_nama():
    return render_template('o-nama.html')



# ==========================================
# 5. ADMIN PANEL RUTE
# ==========================================
@app.route('/admin')
def admin_dashboard():
    konekcija = sqlite3.connect('baza.db')
    konekcija.row_factory = sqlite3.Row
    kursor = konekcija.cursor()
    
    # Povlačimo sve porudžbine sortirane od najnovije ka najstarijoj
    kursor.execute('SELECT * FROM porudzbine ORDER BY datum DESC')
    sve_porudzbine = kursor.fetchall()
    
    konekcija.close()
    
    return render_template('admin_dashboard.html', porudzbine=sve_porudzbine)

@app.route('/admin/porudzbina/<int:id>', methods=['GET', 'POST'])
def admin_order(id):
    konekcija = sqlite3.connect('baza.db')
    konekcija.row_factory = sqlite3.Row
    kursor = konekcija.cursor()
    
    # Ako admin menja status
    if request.method == 'POST':
        novi_status = request.form['status']
        kursor.execute('UPDATE porudzbine SET status = ? WHERE id = ?', (novi_status, id))
        konekcija.commit()
        
    kursor.execute('SELECT * FROM porudzbine WHERE id = ?', (id,))
    porudzbina = kursor.fetchone()
    
    if porudzbina is None:
        konekcija.close()
        return "Porudžbina ne postoji.", 404

    # Parsiramo proizvodi_tekst da bismo izvukli sliku i SKU iz baze
    obogaceni_proizvodi = []
    stavke = porudzbina['proizvodi_tekst'].split(' | ')
    
    for stavka in stavke:
        # Primer: "Lanac Shimano (2 kom.)"
        try:
            # Razdvajamo ime od "(X kom.)"
            delovi = stavka.rsplit(' (', 1)
            ime = delovi[0]
            kolicina_str = delovi[1].replace(' kom.)', '')
            kolicina = int(kolicina_str)
        except:
            ime = stavka
            kolicina = 1
            
        # Trazimo u bazi
        kursor.execute('SELECT slika, sku, cena FROM proizvodi WHERE naziv = ? LIMIT 1', (ime,))
        baza_proizvod = kursor.fetchone()
        
        obogaceni_proizvodi.append({
            'naziv': ime,
            'kolicina': kolicina,
            'slika': baza_proizvod['slika'] if baza_proizvod else 'placeholder.jpg',
            'sku': baza_proizvod['sku'] if baza_proizvod else 'N/A',
            'cena': baza_proizvod['cena'] if baza_proizvod else 0,
            'ukupno': (baza_proizvod['cena'] * kolicina) if baza_proizvod else 0
        })

    konekcija.close()
        
    return render_template('admin_order.html', p=porudzbina, stavke=obogaceni_proizvodi)

if __name__ == '__main__':
    app.run(debug=True)

