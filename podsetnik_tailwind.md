# Tailwind CSS - Podsetnik (Cheatsheet)

Ovo je tvoj lični podsetnik za Tailwind CSS. Ovde beležimo sve "lego kockice" (klase) koje smo do sada iskoristili u projektu, podeljene po kategorijama. 
Fajl ćemo ažurirati kako budemo učili nove stvari!

---

## 1. Tipografija (Tekst i Fontovi)
- **Veličina teksta**: 
  - `text-lg` (Large - malo veći tekst)
  - `text-xl`, `text-2xl`, `text-3xl`, `text-4xl`, `text-5xl`, `text-6xl` (Sve veći i veći naslovi)
- **Debljina teksta**:
  - `font-semibold` (Polu-podebljano)
  - `font-bold` (Podebljano)
  - `font-extrabold` (Ekstra podebljano)
  - `font-mono` (Monospace font, izgleda kao kod)
- **Poravnanje teksta**:
  - `text-center` (Centrira tekst)
  - `text-left` (Poravnanje ulevo)

## 2. Boje (Tekst i Pozadina)
*Napomena: Brojevi od 100 do 900 označavaju nijansu (100 je najsvetlija, 900 najtamnija).*
- **Tekst (text-...)**: 
  - `text-white` (Bela slova)
  - `text-gray-200`, `text-gray-600`, `text-gray-800` (Siva slova, za paragrafe i naslove)
  - `text-blue-300`, `text-blue-600`, `text-blue-700` (Plava slova)
  - `text-green-600` (Zelena slova, koristili smo za cene)
  - `text-red-500` (Crvena slova, npr. za 404 grešku)
- **Pozadina (bg-...)**:
  - `bg-white` (Bela pozadina)
  - `bg-gray-50`, `bg-gray-100`, `bg-gray-800` (Nijanse sive pozadine)
  - `bg-blue-600` (Plava pozadina, npr. za dugmiće i header)
- **Providnost (Opacity)**:
  - `bg-black/60` (Crna pozadina sa 60% providnosti - sjajno za zatamnjivanje slika)

## 3. Razmaci (Spajanje: Margine i Padding)
*Napomena: `m` je margina (prostor OKO elementa), `p` je padding (prostor UNUTAR elementa).*
- **Sve strane**: `p-4`, `p-6`, `p-8`, `p-10` (Unutrašnji razmak sa svih strana)
- **Gore/Dole/Levo/Desno**:
  - `mt-4`, `mt-8`, `mt-10` (Margin Top - prazan prostor iznad)
  - `mb-2`, `mb-4`, `mb-6`, `mb-8` (Margin Bottom - prazan prostor ispod)
  - `mr-4` (Margin Right - prostor desno)
- **Horizontalno (X osa - levo i desno)**: `px-4`, `px-6` (Padding na levoj i desnoj strani)
- **Vertikalno (Y osa - gore i dole)**: `py-2`, `py-3`, `py-6` (Padding gore i dole)
- **Centriranje na sredinu ekrana**: `mx-auto` (Automatska leva i desna margina, gura element u centar)

## 4. Izgled i Struktura (Layout)
- `container` (Ograničava širinu elementa tako da ne ide od ivice do ivice ekrana)
- `max-w-lg`, `max-w-2xl` (Maksimalna širina - štiti da tekst ne bude previše širok)
- `w-full` (Širina 100%)
- `h-full` (Visina 100%)
- `h-96` (Fiksna visina - oko 384 piksela)
- `flex` (Uključuje Flexbox - moćan način za ređanje elemenata)
  - `flex-col` (Ređa elemente jedan ISPOD drugog, u kolonu)
  - `justify-center`, `justify-between` (Raspoređivanje elemenata po glavnoj osi)
  - `items-center` (Centrira elemente vertikalno)
  - `flex-grow` (Govori elementu da zauzme sav preostali slobodan prostor)
- `min-h-screen` (Minimalna visina je 100% visine ekrana)
- `inline-block` (Omogućava da `<a>` tag izgleda kao dugme)

## 5. Mreža (Grid)
- `grid` (Uključuje Grid sistem)
- `grid-cols-1` (Jedna kolona)
- `grid-cols-3` (Tri kolone)
- `gap-6` (Prazan prostor/rupa između redova i kolona u mreži)

## 6. Apsolutno pozicioniranje i Slojevi (Z-Index)
- `relative` (Priprema kontejner da elementi unutar njega mogu da idu jedan PREKO drugog)
- `absolute` (Izvlači element iz normalnog toka i stavlja ga PREKO drugih)
- `inset-0` (Skraćenica koja rasteže apsolutni element od ivice do ivice kontejnera u svim pravcima)
- `z-10` (Gura element na 10. sprat - odnosno, donosi ga napred ispred elemenata sa manjim z-indexom)
- `object-cover` (Primenjuje se na slike da ne bi bile spljoštene, već se elegantno rastegnu i iseku viškove)
- `overflow-hidden` (Sve što ispadne van granica kontejnera se seče i ne vidi se)

## 7. Granice, Senke i Animacije
- **Ivice (Corners)**: `rounded`, `rounded-lg`, `rounded-full` (Zaobljene ivice)
- **Senke**: `shadow-sm`, `shadow-md`, `shadow-lg` (Senka ispod elementa)
- **Linije (Borders)**: 
  - `border`, `border-gray-200`, `border-blue-300` (Tanka ivica oko elementa sa bojom)
  - `border-t`, `border-b` (Border Top i Border Bottom)
- **Efekti**:
  - `backdrop-blur-sm` (Stakleni efekat / zamagljivanje onoga što je iza elementa)
- **Interakcija**:
  - `hover:bg-blue-700` (Kada pređeš mišem, promeni pozadinu u tamnije plavu)
  - `hover:text-blue-200` (Kada pređeš mišem, promeni tekst u svetlo plavu)
  - `hover:shadow-md` (Dodaj jaču senku na hover)
  - `transition` (Ovo omogućava da promene boje i senke na hover budu glatke, a ne nagle)

---

## 8. NAJBOLJA PRAKSA ZA EKRANE (Responzivni dizajn)
**Tailwind koristi "Mobile-First" pristup.** Ovo znači da sve klase koje napišeš BEZ prefiksa važe primarno za **mobilne telefone**. 

Da bi promenio izgled na većim ekranima, koristiš prefikse:
- `sm:` (Mali ekrani - preko 640px)
- `md:` (Srednji ekrani - tableti, preko 768px)
- `lg:` (Veliki ekrani - laptopovi, preko 1024px)
- `xl:` (Desktop ekrani - preko 1280px)

### Šta je PRAKSA da se stavi i menja?
Najčešće ne menjaš boje, već **veličine, margine i raspored (layout)**.
1. **Tekst:** Na mobilnom koristiš manji tekst, a na računaru veći.
   - Primer: `<h1 class="text-3xl md:text-5xl lg:text-6xl">Naslov</h1>`
2. **Raspored kolona (Grid):** Na mobilnom stavljaš elemente u 1 kolonu, a na računaru u 3 ili 4.
   - Primer: `<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4">...</div>`
3. **Margine (Prazan prostor):** Mobilni ekrani imaju manje prostora, pa stavljaš manje margine, a na računaru ih povećavaš da diše.
   - Primer: `<div class="p-4 md:p-8 lg:p-12">...</div>`
4. **Sakrivanje elemenata:** Ponekad želiš da se neki meni vidi na telefonu (hamburger meni), a ne na računaru, ili obrnuto.
   - Primer (sakrij na telefonu, pokaži na kompjuteru): `<div class="hidden md:block">Meni</div>`
