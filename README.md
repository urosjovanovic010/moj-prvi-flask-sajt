# Pokretanje Flask Projekta

Ovaj fajl služi kao podsetnik za komande koje je potrebno pokrenuti svaki put kada počinješ rad na projektu.

## Koraci za pokretanje

Svaki put kada otvoriš novi terminal (ili započneš rad u Antigravity-ju), potrebno je da uradiš sledeće:

1. **Aktiviraj virtuelno okruženje:**
   Ovo govori tvom terminalu da koristi specifičnu verziju Python-a i biblioteka (poput Flask-a) instaliranih za ovaj projekat.
   ```fish
   source .venv/bin/activate.fish
   ```
   *(Znaćeš da si uspeo ako se na početku linije u terminalu pojavi tekst `(.venv)`).*

2. **Pokreni Flask aplikaciju:**
   Nakon što je okruženje aktivirano, pokrećeš tvoj glavni Python fajl koji startuje server:
   ```fish
   python index.py
   ```

3. **Otvori aplikaciju u browseru:**
   Sada kada server radi, možeš videti svoj sajt tako što ćeš u internet pregledaču (Chrome, Firefox, itd.) otići na adresu:
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Zašto ovo radimo?
- **Virtuelno okruženje** drži naš projekat izolovanim. To znači da se alati i biblioteke za ovaj projekat ne mešaju sa drugim projektima na tvom računaru.
- **`python index.py`** bukvalno čita kod koji si napisao i pretvara ga u živi web server koji može da prima zahteve i šalje HTML stranice nazad.
