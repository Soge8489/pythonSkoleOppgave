# VLC oppdateringssjekk

Dette prosjektet sjekker om programmet **VLC** har en ny versjon ved å hente siste release fra GitHub (VideoLAN/VLC) og lagrer resultatet i en SQLite-database. Programmet sammenligner siste kjente versjon med den nye og gir beskjed om det finnes en oppdatering.

## Funksjoner
- Henter siste VLC-versjon fra GitHub Releases.
- Lagrer sjekker og siste kjente versjon i SQLite.
- Kan kjøre i testmodus med `--mock-version` uten nettverk.

## Kom i gang

### Krav
- Python 3.10+

### Kjør programmet
```bash
python main.py
```

### Testmodus (uten nettverk)
```bash
python main.py --mock-version 3.0.20
```

### Eksempel på output
- Første kjøring: `Ingen tidligere versjon lagret...`
- Senere kjøring med ny versjon: `Oppdatering funnet!`

## Database
- Standard databasefil: `vlc_updates.db`
- Tabeller:
  - `checks`: historikk over alle sjekker
  - `state`: siste kjente versjon per produkt

## GitHub
Du kan publisere dette i et nytt GitHub-repo ved å:
1. Opprette repo på GitHub.
2. Koble til lokal repo og pushe.

Eksempel:
```bash
git remote add origin git@github.com:brukernavn/vlc-update-checker.git
git push -u origin main
```
