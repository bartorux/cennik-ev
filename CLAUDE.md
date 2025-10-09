# CLAUDE.md

Ten plik zawiera wskazówki dla Claude Code (claude.ai/code) podczas pracy z kodem w tym repozytorium.

**WAŻNE: Zawsze komunikuj się po polsku w tym projekcie.**

## Przegląd projektu

To narzędzie do porównywania cen ładowania pojazdów elektrycznych w Polsce. Składa się z:
- Scrapera w Pythonie, który automatycznie pobiera dane cenowe od polskich operatorów ładowarek EV
- Statycznego interfejsu HTML/JavaScript służącego jako kalkulator do porównywania kosztów ładowania
- Workflow GitHub Actions do automatycznej aktualizacji cen

Projekt scrapuje ceny z operatorów GreenWay (z PDF-a) i Orlen Charge (ze strony WWW) i generuje plik JSON, który wykorzystuje frontend.

## Komendy

### Scraper w Pythonie

Instalacja zależności:
```bash
pip install -r requirements-txt.txt
```

Uruchomienie scrapera ręcznie:
```bash
python scraper-python.py
```

To generuje plik `pricing-data.json` z najnowszymi informacjami o cenach.

### Podgląd frontendu w Visual Studio Code

Plik HTML ([updated-html.html](updated-html.html)) jest samodzielny. Aby go podglądać:

**Opcja 1 - Live Server (najlepsza):**
1. Zainstaluj rozszerzenie "Live Server" w VS Code
2. Kliknij prawym przyciskiem na [updated-html.html](updated-html.html)
3. Wybierz "Open with Live Server"
4. Strona otworzy się w przeglądarce z auto-odświeżaniem

**Opcja 2 - Bezpośrednio w przeglądarce:**
- Kliknij prawym przyciskiem na [updated-html.html](updated-html.html) → "Copy Path"
- Wklej ścieżkę w pasku adresu przeglądarki

**Opcja 3 - Python HTTP Server:**
```bash
python -m http.server 8000
```
Następnie otwórz http://localhost:8000/updated-html.html

Strona wymaga pliku `pricing-data.json` w tym samym katalogu (najpierw uruchom scraper).

## Architektura

### Przepływ danych

1. **Scraper ([scraper-python.py](scraper-python.py))** → **Dane JSON** → **Kalkulator WWW ([updated-html.html](updated-html.html))**

### Architektura scrapera (scraper-python.py)

Klasa `EVChargingPriceScraper` zawiera:
- `scrape_greenway()`: Pobiera cennik GreenWay z PDF-a z https://data.greenway.sk/clientzone/pl/GWP_pricelist_PL.pdf i parsuje używając PyPDF2 + regex
- `scrape_orlen()`: Scrapuje stronę Orlen Charge z https://orlencharge.pl/cennik/ używając BeautifulSoup
- Metody z danymi awaryjnymi (`get_default_greenway_data()`, `get_default_orlen_data()`) gdy scraping się nie powiedzie
- Wzorce regex do wydobywania cen dla różnych typów ładowania (AC, DC, HPC)
- Wykrywanie promocji ze stron operatorów

Format wyjściowy w `pricing-data.json`:
```json
{
  "lastUpdate": "znacznik czasu ISO",
  "operators": {
    "greenway": {
      "name": "GreenWay",
      "color": "#10b981",
      "subscriptions": [...],
      "promotions": [...]
    },
    "orlen": { ... }
  }
}
```

### Architektura frontendu (updated-html.html)

Aplikacja jednostronicowa z dwoma trybami obliczania:
1. **Tryb jednorazowy**: Oblicza koszt pojedynczej sesji ładowania (konkretna ilość kWh)
2. **Tryb miesięczny**: Oblicza koszty miesięczne z planami abonamentowymi

Kluczowe funkcje JavaScript:
- `loadPricingData()`: Pobiera pricing-data.json
- `calculateCosts()`: Główny silnik obliczeniowy, który wylicza koszty dla wszystkich kombinacji operator/abonament
- `calculateAndDisplay()`: Renderuje interfejs porównawczy
- `generateSubscriptionsList()`: Dynamicznie tworzy selektor abonamentów z danych JSON
- Trwałość ustawień w localStorage

Obsługiwane typy ładowania:
- AC (wolne, do 22 kW)
- DC (szybkie, do 50 kW)
- HPC (ultraszybkie, >100 kW)

### Workflow GitHub Actions (github-action.txt)

Zautomatyzowany workflow, który:
- Uruchamia się co 6 godzin przez cron (`0 */6 * * *`)
- Wykonuje scraper Pythona
- Commituje zaktualizowany pricing-data.json jeśli wykryto zmiany
- Waliduje strukturę JSON i zakresy cen
- Tworzy GitHub issues w przypadku błędu

## Dodawanie nowych operatorów

Aby dodać nowego operatora ładowarek EV:

1. W [scraper-python.py](scraper-python.py):
   - Dodaj nową metodę scrapującą (np. `scrape_ionity()`)
   - Postępuj według wzorca: pobierz dane, sparsuj ceny dla AC/DC/HPC, obsłuż błędy z danymi awaryjnymi
   - Dodaj do metody `save_to_file()`: `self.pricing_data["operators"]["ionity"] = self.scrape_ionity()`

2. Frontend automatycznie:
   - Załaduje nowego operatora z JSON-a
   - Doda go do selektora abonamentów
   - Uwzględni w porównaniach kosztów
   - Wyświetli w rankingu

## Ważne uwagi

- **Scraping cen**: GreenWay używa parsowania PDF (regex na ekstrakcji tekstu), Orlen używa scrapingu HTML (wiele selektorów + fallback)
- **Dane awaryjne**: Zawsze utrzymuj dane awaryjne na wypadek niepowodzenia scrapingu
- **Wzorce regex**: Scraper używa polskiego formatu liczb (przecinek jako separator dziesiętny, np. "2,40 zł/kWh")
- **Ustawienia użytkownika**: Frontend zachowuje preferencje użytkownika (tryb, zużycie, wybrane abonamenty) w localStorage
- **Wykrywanie promocji**: Scraper wyszukuje rabaty procentowe i zakresy dat na stronach promocyjnych (promocje czasowe)
- **Obliczanie progu opłacalności**: Frontend oblicza, kiedy plany abonamentowe stają się opłacalne na podstawie miesięcznego zużycia
- **Orlen - dwa cenniki**: Orlen Charge ma cennik standardowy i promocyjny (dla użytkowników aplikacji/karty Vitay). Scraper próbuje wykryć oba z tabeli HTML (2 kolumny cen). Jeśli nie znajdzie, tworzy promocyjny jako ~10% taniej od standardowego.
- **Tryb jednorazowy vs miesięczny**: W trybie jednorazowym pokazujemy TYLKO opcje bez abonamentu (bo nikt nie kupi abonamentu za 30-80 zł dla jednego ładowania). W trybie miesięcznym pokazujemy wszystkie opcje z obliczeniem opłacalności.
