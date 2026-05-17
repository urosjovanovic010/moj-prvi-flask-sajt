# TryMyBike - Analiza i Roadmap (Plan Učenja)

Ovaj dokument služi kao tvoj lični putokaz. Prikazuje koliko si već napredovao i šta su sledeći logični koraci u pretvaranju ovog projekta u pravu, funkcionalnu web aplikaciju.

---

## 🏆 Analiza Dosadašnjeg Učenja (Šta smo već savladali)

Napravio si ogroman skok od nule do funkcionalne web aplikacije. Evo šta tvoj mozak sada već podvesno razume:

### 1. Python i Flask (Backend)
- **Rute (Routes):** Razumeš kako funkcija u Pythonu (npr. `@app.route('/')`) odgovara na ono što korisnik ukuca u browseru.
- **Dinamički URL-ovi:** Naučio si da hvataš parametre iz URL-a (`<int:id>`) i koristiš ih za pretragu proizvoda.
- **Arhitektura koda (MVC):** Uvideo si značaj odvajanja podataka (`baza.py`) od logike (`index.py`), što je temelj profesionalnog programiranja.
- **HTTP Kodovi:** Razumeš razliku između normalnog učitavanja stranice i greške (404), i znaš kako da Flask vrati pravi status kod.

### 2. Jinja2 i HTML (Frontend spona)
- **Templejti i Nasleđivanje:** Korišćenje `base.html` da se ne bi ponavljao kod za header i footer.
- **Dinamika u HTML-u:** Korišćenje `{% for %}` petlji i `{{ varijabli }}` za prikazivanje Python podataka na web stranici.
- **Linkovanje:** Dinamičko pravljenje linkova koristeći `url_for()`.

### 3. Tailwind CSS (Dizajn)
- **Utility-first CSS:** Znaš kako da stilizuješ elemente bez pisanja eksternih CSS fajlova (tekst, boje, razmaci, senke).
- **Responzivnost:** Razumeš "Mobile-first" pristup i korišćenje prefiksa (`md:`, `lg:`) za promenu izgleda na većim ekranima.
- **Napredni raspored:** Korišćenje Flexbox-a i CSS Grid-a za ređanje elemenata, kao i složenih `absolute`/`relative` slojeva za hero slike.

### 4. Alati i Workflow
- **Git i GitHub:** Redovno verzionisanje koda, pisanje commit poruka i pushovanje na remote repozitorijum.
- **Obsidian:** Korišćenje Obsidian-a za vođenje beleški direktno kroz strukturu projekta.

---

## 🚀 ROADMAP: Plan za Dalji Razvoj

Pred nama su 4 uzbudljive faze. Svaka faza donosi novi koncept koji se koristi u industriji.

### FAZA 1: Utvrđivanje gradiva i "Čišćenje" (Trenutno)
Cilj: Očistiti male tehničke dugove i obogatiti trenutni UI.
- [x] Očistiti `.gitignore` (skloniti `.obsidian` iz Git istorije da nam ne prlja kod).
- [x] Dodati lepši navigacioni meni u `base.html` (aktivan link, logo koji vodi na početnu).
- [x] Dodati još par proizvoda u `baza.py` da bi "Shop" izgledao bogatije.

### FAZA 2: Komunikacija sa korisnikom (HTML Forme i Metode)
Cilj: Omogućiti posetiocima da pošalju podatke na server.
- [x] Napraviti `kontakt.html` stranicu sa formom (Ime, Email, Poruka).
- [x] Učiti razliku između **GET** i **POST** metoda u web-u.
- [x] Napraviti Flask rutu koja prihvata te podatke i ispisuje ih u terminal (kasnije i na ekran "Uspešno ste poslali poruku").

### FAZA 3: Prelazak na Pravu Bazu Podataka (SQLite) (Završeno!)
Cilj: Zameniti naš `baza.py` pravom bazom podataka kako bi podaci trajno ostali sačuvani, baš kao na pravim sajtovima.
- [x] Uvod u relacione baze podataka (Tabele, Kolone, Redovi).
- [x] Povezivanje Flaska sa SQLite bazom podataka.
- [x] Čitanje proizvoda iz prave baze umesto iz Python liste.
- [x] *Bonus:* Automatski uvoz 4000+ artikala iz CSV i XML fajlova (Dropshipping integracija)!
- [x] *Bonus:* Napredna taksonomija (Odeljak, Kategorija, Potkategorija, SKU, Zalihe).

### FAZA 3.5: Napredno filtriranje i pretraga (Sledeći logičan korak)
Cilj: Iskoristiti novu arhitekturu baze da posetiocima sajta omogućimo lako pronalaženje delova.
- [ ] Pravljenje "Sidebar-a" na početnoj stranici za filtere.
- [ ] Izlistavanje svih proizvođača i kategorija iz baze.
- [ ] Dinamičko filtriranje proizvoda klikom na checkbox ili link.

### FAZA 4: Admin Panel (Kruna projekta)
Cilj: Napraviti zaštićen deo sajta gde vlasnik može da dodaje nove proizvode.
- [ ] Kreiranje skrivene rute `/admin` ili `/dodaj-proizvod`.
- [ ] Pravljenje forme gde ti možeš da ukucaš naziv novog bicikla, cenu i sliku, stisneš "Dodaj", i on se automatski upiše u bazu i pojavi na početnoj stranici!
- [ ] *(Bonus)* Brisanje i izmena postojećih proizvoda (CRUD operacije).

---

> Beleška: Svaki od ovih koraka ćemo raditi postepeno, razbijen u male zadatke, baš kao i do sada. Nema žurbe! Pravi inženjeri uče koncept, a ne kod napamet.
