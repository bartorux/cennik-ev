# CLAUDE.md

Ten plik zawiera wskazówki dla Claude Code (claude.ai/code) podczas pracy z kodem w tym repozytorium.

**WAŻNE: Zawsze komunikuj się po polsku w tym projekcie.**

## Przegląd projektu

To narzędzie do porównywania cen ładowania pojazdów elektrycznych w Polsce. Składa się z:
- Scrapera w Pythonie, który automatycznie pobiera dane cenowe od polskich operatorów ładowarek EV
- Statycznego interfejsu HTML/JavaScript służącego jako kalkulator do porównywania kosztów ładowania
- Workflow GitHub Actions do automatycznej aktualizacji cen

Projekt scrapuje ceny z operatorów GreenWay (z PDF-a), Orlen Charge (ze strony WWW przez Selenium) i generuje plik JSON, który wykorzystuje frontend.

**Strona na żywo:** https://bartorux.github.io/cennik-ev/

## Komendy

### Scraper w Pythonie

Instalacja zależności:
```bash
pip install -r requirements.txt
```

Uruchomienie scrapera ręcznie:
```bash
python scraper-python.py
```

To generuje plik `pricing-data.json` z najnowszymi informacjami o cenach.

**Uwaga:** Scraper Orlen wymaga Selenium + Chrome/Chromium.

### Podgląd frontendu lokalnie

Główny plik HTML to [index.html](index.html). Aby go podglądać:

**Opcja 1 - Live Server (najlepsza):**
1. Zainstaluj rozszerzenie "Live Server" w VS Code
2. Kliknij prawym przyciskiem na [index.html](index.html)
3. Wybierz "Open with Live Server"
4. Strona otworzy się w przeglądarce z auto-odświeżaniem

**Opcja 2 - Bezpośrednio w przeglądarce:**
- Kliknij prawym przyciskiem na [index.html](index.html) → "Copy Path"
- Wklej ścieżkę w pasku adresu przeglądarki

**Opcja 3 - Python HTTP Server:**
```bash
python -m http.server 8000
```
Następnie otwórz http://localhost:8000/index.html

Strona wymaga pliku `pricing-data.json` w tym samym katalogu (najpierw uruchom scraper).

## Architektura

### Przepływ danych

1. **Scraper ([scraper-python.py](scraper-python.py))** → **Dane JSON ([pricing-data.json](pricing-data.json))** → **Kalkulator WWW ([index.html](index.html))**

### Architektura scrapera (scraper-python.py)

Klasa `EVChargingPriceScraper` zawiera:
- `scrape_greenway()`: Pobiera cennik GreenWay z PDF-a z https://data.greenway.sk/clientzone/pl/GWP_pricelist_PL.pdf i parsuje używając PyPDF2 + regex
- `scrape_orlen()`: Scrapuje stronę Orlen Charge (Selenium + Chrome headless)
  - Sprawdza `/cennik-promo/` dla promocji czasowych z datami
  - Fallback do `/cennik/` gdy brak promocji
  - Wykrywa ceny standardowe i promocyjne (2 kolumny w tabeli)
- Metody z danymi awaryjnymi (`get_default_greenway_data()`, `get_default_orlen_data()`) gdy scraping się nie powiedzie
- Wzorce regex do wydobywania cen dla różnych typów ładowania (AC, DC ≤50kW, DC Mid 50-125kW, HPC >125kW)
- Wykrywanie promocji ze stron operatorów (daty, rabaty)

**Obsługiwani operatorzy:**
- **GreenWay**: 3 plany (Standard, Plus, Max) z różnymi opłatami abonamentowymi
- **Orlen Charge**: Bez abonamentu + promocje czasowe
- **IONITY**: 3 plany (Go, Motion, Power) - **tylko HPC** (>125kW)

Format wyjściowy w `pricing-data.json`:
```json
{
  "lastUpdate": "znacznik czasu ISO",
  "operators": {
    "greenway": {
      "name": "GreenWay",
      "color": "#10b981",
      "subscriptions": [...],
      "promotions": []
    },
    "orlen": {
      "name": "Orlen Charge",
      "subscriptions": [...],
      "promotions": [{
        "name": "Promocja cenowa -25%",
        "validFrom": "2025-10-02",
        "validTo": "2025-11-03",
        "prices": {...}
      }]
    },
    "ionity": {
      "name": "IONITY",
      "subscriptions": [...],
      "promotions": []
    }
  }
}
```

### Architektura frontendu (index.html)

Aplikacja jednostronicowa (SPA) z dwoma trybami obliczania:

1. **Tryb jednorazowy**: Oblicza koszt pojedynczej sesji ładowania
   - Wybór ilości kWh (0-150)
   - Wybór typu ładowarki (AC/DC/DC Mid/HPC)
   - Pokazuje **tylko opcje bez abonamentu** (nikt nie kupuje abonamentu dla jednego ładowania)

2. **Tryb miesięczny**: Oblicza koszty miesięczne z planami abonamentowymi
   - Miesięczne zużycie w kWh (0-1000)
   - **Proporcje typów ładowania** - suwaki z auto-normalizacją do 100%:
     - AC (wolne, do 22 kW)
     - DC (szybkie, ≤50 kW)
     - DC Mid (średnie, 50-125 kW)
     - HPC (ultraszybkie, >125 kW)
   - **Dwa widoki porównania:**
     - **Per kategoria**: Osobne rankingi dla każdego typu ładowania
     - **Łączny koszt**: Suma według proporcji + wykres opłacalności

**Kluczowe funkcje JavaScript:**
- `loadPricingData()`: Pobiera pricing-data.json z cache-busting + fallback do danych awaryjnych
- `calculateCosts()`: Główny silnik obliczeniowy (operator × abonament × typ ładowania)
- `calculateCategoryResults()`: Obliczanie per kategoria (AC/DC/DC Mid/HPC)
- `calculateAndDisplay()`: Renderuje interfejs porównawczy
- `generateSubscriptionsList()`: Dynamicznie tworzy radio buttons dla planów abonamentowych
- `updateChart()`: Canvas-based wykres opłacalności (ukrywa krzywe gdy wszystkie typy wyłączone)
- `normalizePercents()`: Auto-normalizacja suwaków proporcji do 100%
- localStorage: Auto-save wszystkich ustawień użytkownika

**Obsługiwane typy ładowania:**
- **AC** - wolne (do 22 kW) - hotel, dom, parking
- **DC** - szybkie (≤50 kW) - podstawowe DC
- **DC Mid** - średnie (50-125 kW) - średnie DC
- **HPC** - ultraszybkie (>125 kW) - premium stacje (IONITY)

### Workflow GitHub Actions (.github/workflows/update-prices.yml)

Zautomatyzowany workflow, który:
- Uruchamia się co 6 godzin przez cron (`0 */6 * * *`)
- Instaluje Chrome/Chromium + ChromeDriver (dla Selenium)
- Wykonuje scraper Pythona
- Commituje zaktualizowany pricing-data.json jeśli wykryto zmiany
- Automatycznie wdraża na GitHub Pages (branch: main, root folder)

**Plik `.nojekyll`** wyłącza Jekyll - konieczny dla poprawnego działania GitHub Pages z plikami JSON.

## Dodawanie nowych operatorów

Aby dodać nowego operatora ładowarek EV:

1. **W [scraper-python.py](scraper-python.py):**
   - Dodaj nową metodę scrapującą (np. `scrape_ionity()`)
   - Postępuj według wzorca: pobierz dane, sparsuj ceny dla AC/DC/DC Mid/HPC, obsłuż błędy z danymi awaryjnymi
   - Dodaj do metody `save_to_file()`: `self.pricing_data["operators"]["ionity"] = self.scrape_ionity()`
   - **Ważne:** Jeśli operator nie obsługuje jakiegoś typu ładowania (np. IONITY nie ma AC/DC), ustaw cenę na `999` (placeholder)

2. **Frontend automatycznie:**
   - Załaduje nowego operatora z JSON-a
   - Doda go do selektora abonamentów (radio buttons per operator)
   - Uwzględni w porównaniach kosztów (pomija ceny `>= 999`)
   - Wyświetli w rankingu z właściwym kolorem
   - **IONITY** - specjalna logika: w trybie miesięcznym liczy tylko HPC, pomija inne typy

3. **Dane awaryjne:**
   - Dodaj nowego operatora do `useFallbackData()` w [index.html](index.html)
   - Struktura: `{id, name, monthlyCost, prices: {ac, dc, dc_mid, hpc}, benefits: []}`

## Ważne uwagi

### Scraping
- **GreenWay**: Parsowanie PDF (PyPDF2 + regex na ekstrakcji tekstu)
- **Orlen**: Selenium + Chrome headless (najpierw `/cennik-promo/`, fallback do `/cennik/`)
  - Dwa cenniki: standardowy i promocyjny (2 kolumny w tabeli HTML)
  - Wykrywanie dat promocji (regex: "X miesiąca YYYY r. do dnia Y miesiąca YYYY r.")
- **Wzorce regex**: Polski format liczb (przecinek jako separator dziesiętny, np. "2,40 zł/kWh")
- **Dane awaryjne**: Zawsze utrzymuj aktualne dane awaryjne w `get_default_*_data()` i `useFallbackData()`

### Frontend
- **Auto-save**: Wszystkie ustawienia zapisują się automatycznie w localStorage
  - Tryb (instant/monthly), zużycie, proporcje typów, wybrane abonamenty, włączone promocje
- **Ładowanie danych**:
  - `fetch('pricing-data.json')` z cache-busting (`?t=${Date.now()}`)
  - Fallback do danych awaryjnych gdy fetch się nie powiedzie
  - Verbose logging w konsoli (`🔄`, `📡`, `📦`, `✅`, `❌`)
- **Wykres opłacalności**:
  - Canvas-based (nie ma bibliotek Chart.js)
  - Ukrywa krzywe gdy wartości = 0 (wszystkie typy ładowania wyłączone)
  - Pokazuje się tylko w trybie miesięcznym + widok "Łączny koszt"
- **Normalizacja procentów**: Suwaki auto-normalizują się do 100% (gdy zmienisz jeden, reszta się dopasuje)
- **Obliczanie progu opłacalności**: Frontend oblicza, kiedy plany abonamentowe stają się opłacalne (breakEvenPoint w kWh/mies)
- **Tryb jednorazowy vs miesięczny**:
  - **Jednorazowy**: Pokazuje TYLKO opcje bez abonamentu (nikt nie kupuje abonamentu za 30-80 zł dla jednego ładowania)
  - **Miesięczny**: Pokazuje wszystkie opcje z obliczeniem opłacalności + 2 widoki (per kategoria / łączny koszt)

### Promocje czasowe
- Scraper wykrywa promocje ze stron operatorów (daty, rabaty)
- Frontend sprawdza `validFrom` i `validTo` (porównanie z `new Date()`)
- Użytkownik może włączyć/wyłączyć promocje w ustawieniach (checkbox "Uwzględnij promocje czasowe")
- Promocje wyświetlane z czerwonym badge "PROMO"

### GitHub Pages
- **Plik `.nojekyll`** - konieczny! Wyłącza Jekyll
- Ścieżka do pricing-data.json: **`pricing-data.json`** (nie `./pricing-data.json`)
- Cache-busting: `?t=${Date.now()}` + nagłówki `cache: 'no-cache'`
- Deployment: automatyczny po każdym push do `main` (branch: main, folder: root)
