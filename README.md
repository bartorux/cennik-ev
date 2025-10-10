# 🚗 Kalkulator Cen Ładowania Pojazdów Elektrycznych

Porównywarka cen ładowania pojazdów elektrycznych w Polsce (GreenWay, Orlen Charge).

**🌐 Demo na żywo:** https://[twoja-nazwa].github.io/cennik/

---

## 📋 Spis treści

- [Dla użytkowników](#dla-użytkowników)
- [Dla administratora (Ty)](#dla-administratora)
  - [Jak zaktualizować promocję Orlen](#1-jak-zaktualizować-promocję-orlen)
  - [Jak wyłączyć promocję](#2-jak-wyłączyć-promocję)
  - [Jak uruchomić scraper](#3-jak-uruchomić-scraper-automatycznie)
  - [Jak wdrożyć zmiany](#4-jak-wdrożyć-zmiany-na-stronę)
- [Struktura projektu](#struktura-projektu)

---

## 👤 Dla użytkowników

### Funkcje:
- ✅ **Tryb jednorazowy**: Oblicz koszt ładowania określonej ilości kWh
- ✅ **Tryb miesięczny**: Porównaj koszty miesięczne z różnymi abonamentami
- ✅ **4 prędkości ładowania**: AC, DC ≤50kW, DC 50-125kW, DC >125kW
- ✅ **Dynamiczne suwaki proporcji**: Auto-normalizacja do 100%
- ✅ **Promocje czasowe**: Automatyczne uwzględnianie aktywnych promocji
- ✅ **Próg opłacalności**: Zobacz kiedy abonament się opłaca
- ✅ **Auto-save**: Wszystkie zmiany zapisują się automatycznie

### Obsługiwani operatorzy:
- 🟢 **GreenWay** (3 plany: Standard, Plus, Max)
- 🔴 **Orlen Charge** (cennik standardowy + promocje czasowe)

---

## 🔧 Dla administratora

### Pliki na GitHub Pages (publiczne):
```
📁 Repozytorium
├── index.html              ← Główny kalkulator (publiczny)
├── pricing-data.json       ← Dane cenowe (publiczny)
├── CLAUDE.md              ← Dokumentacja dla AI
└── README.md              ← Ta instrukcja
```

### Pliki TYLKO lokalnie (nie commituj!):
```
📁 Twój komputer
├── edytor-promocji.html    ← Edytor promocji (PRYWATNY)
├── scraper-python.py       ← Scraper (opcjonalny)
├── requirements-txt.txt    ← Zależności Python
└── .env                    ← Sekrety (jeśli będą)
```

---

## 1. 🎯 Jak zaktualizować promocję Orlen?

### Krok 1: Sprawdź aktualne ceny na stronie Orlen

1. Wejdź na: https://orlencharge.pl/cennik/
2. Kliknij **"Sprawdź cenę"** przy dowolnym złączu
3. Zobaczysz tabelę z 2 kolumnami:
   - **Kolumna 1**: Cena standardowa (np. AC 1,95 PLN/kWh)
   - **Kolumna 2**: Cena promocyjna (np. AC 1,46 PLN/kWh) + daty (np. "2.10 - 3.11.2025")

### Krok 2: Otwórz edytor promocji

**Lokalnie na swoim komputerze:**
```bash
# Otwórz plik w przeglądarce
# Windows:
start edytor-promocji.html

# Lub kliknij prawym → "Open with" → Chrome/Firefox
```

### Krok 3: Wypełnij formularz

- ✅ **Zaznacz**: "Promocja aktywna"
- **Nazwa**: np. "Promocja cenowa -25%"
- **Data od**: np. 2025-02-10
- **Data do**: np. 2025-11-03
- **Ceny** (4 przedziały):
  - AC: 1.46
  - DC (≤50kW): 2.02
  - DC Mid (50-125kW): 2.17
  - HPC (>125kW): 2.39
- **Warunki**: "Obowiązuje dla wszystkich użytkowników"

### Krok 4: Generuj i kopiuj kod

**Wybierz metodę:**

#### **Metoda A: Bezpośrednia edycja JSON (szybsza)**
1. Kliknij **"Generuj JSON"**
2. Kopiuj wygenerowany kod
3. Otwórz `pricing-data.json`
4. Znajdź sekcję `"orlen"` → `"promotions":`
5. Zamień na skopiowany kod
6. Zapisz plik

#### **Metoda B: Edycja Python (trwalsza)**
1. Kliknij **"Generuj kod Python"**
2. Kopiuj wygenerowany kod
3. Otwórz `scraper-python.py`
4. Znajdź funkcję `get_default_orlen_data()`
5. Zamień sekcję `"promotions":` na skopiowany kod
6. Zapisz plik
7. Uruchom: `python scraper-python.py`

### Krok 5: Wdróż na stronę

```bash
git add pricing-data.json
git commit -m "Aktualizacja promocji Orlen: -25% do 3.11.2025"
git push
```

**Gotowe!** Strona zaktualizuje się automatycznie w ~2 minuty.

---

## 2. ❌ Jak wyłączyć promocję?

### Kiedy promocja wygasła:

#### **Sposób 1: Przez edytor (zalecany)**
1. Otwórz `edytor-promocji.html`
2. **Odznacz**: "Promocja aktywna"
3. Kliknij **"Generuj JSON"**
4. Skopiuj: `[]` (pusta tablica)
5. Wklej do `pricing-data.json` → `"orlen"` → `"promotions": []`
6. Commit i push

#### **Sposób 2: Ręcznie**
Otwórz `pricing-data.json` i znajdź:
```json
"orlen": {
  "promotions": [
    { ... }  ← Usuń całą zawartość
  ]
}
```

Zamień na:
```json
"orlen": {
  "promotions": []
}
```

### Użytkownicy mogą też wyłączyć promocję:

Użytkownicy widzą checkbox **"Uwzględnij promocje czasowe"** w kalkulatorze.
- ✅ Zaznaczony: Pokazuje ceny promocyjne
- ❌ Odznaczony: Pokazuje ceny standardowe

---

## 3. 🤖 Jak uruchomić scraper automatycznie?

### Opcja A: GitHub Actions (zalecana - AKTYWNA)

**Workflow automatyczny (`.github/workflows/update-prices.yml`):**
- ✅ Uruchamia się co 6 godzin
- ✅ **GreenWay**: Scraper PDF → pobiera 3 plany z cennika
- ✅ **Orlen**: Selenium scraper → sprawdza `/cennik-promo/` i `/cennik/`
- ✅ Automatycznie wykrywa promocje i daty
- ✅ Commituje zmiany tylko jeśli ceny się zmieniły

**Wymagania:**
- Chrome/Chromium (zainstalowany automatycznie w GitHub Actions)
- Selenium (w `requirements.txt`)

### Opcja B: Lokalnie (ręcznie)

```bash
# 1. Zainstaluj zależności (raz)
pip install -r requirements.txt

# 2. Uruchom scraper (wymaga Chrome)
python scraper-python.py

# 3. Sprawdź co się zmieniło
git diff pricing-data.json

# 4. Commituj jeśli wszystko OK
git add pricing-data.json
git commit -m "Aktualizacja cen przez scraper"
git push
```

---

## 4. 🚀 Jak wdrożyć zmiany na stronę?

### Zmiany w danych (pricing-data.json):
```bash
git add pricing-data.json
git commit -m "Opis zmian"
git push
```

### Zmiany w kalkulatorze (index.html):
```bash
git add index.html
git commit -m "Nowa funkcja: ..."
git push
```

### Zmiany w wielu plikach:
```bash
git add .
git commit -m "Duża aktualizacja"
git push
```

**Czas wdrożenia:** ~1-3 minuty

---

## 📁 Struktura projektu

### Publiczne (GitHub Pages):
```
index.html              # Główny kalkulator
pricing-data.json       # Dane cenowe (GreenWay + Orlen)
CLAUDE.md              # Dokumentacja dla AI asystenta
README.md              # Ta instrukcja
```

### Backend (w repo, ale nie na Pages):
```
scraper-python.py       # Scraper cen (Selenium + PDF)
requirements.txt        # Zależności Python
.github/workflows/      # GitHub Actions (auto-scraping co 6h)
.gitignore             # Lista ignorowanych plików
```

### Pliki testowe (nie commitować):
```
edytor-promocji.html    # Edytor promocji (opcjonalny)
scrape_orlen_final.py   # Testy Selenium
orlen_*.txt            # Logi testowe
```

---

## 🔐 Bezpieczeństwo

### Co NIE publikować:
- ❌ `edytor-promocji.html` - tylko dla Ciebie
- ❌ Pliki `.py` - opcjonalnie można, ale nie muszą być publiczne
- ❌ Pliki testowe, `.env`, sekrety

### Plik `.gitignore` zadba o to automatycznie.

---

## ❓ FAQ

### Jak często aktualizować ceny?

**GreenWay:** Automatycznie przez scraper (co 6h przez GitHub Actions)
**Orlen:** Ręcznie gdy ogłoszą nową promocję (zwykle co miesiąc)

### Co jeśli scraper przestanie działać?

Scraper ma **dane awaryjne** (fallback). Jeśli scraping się nie powiedzie, użyje ostatnich znanych cen.

### Jak dodać nowego operatora (np. Ionity)?

Zobacz: `CLAUDE.md` → sekcja "Dodawanie nowych operatorów"

### Gdzie szukać pomocy?

- 📖 **Dokumentacja techniczna**: `CLAUDE.md`
- 🤖 **AI Asystent**: Claude Code czyta ten plik automatycznie
- 🐛 **Problemy**: Utwórz issue w repozytorium

---

## 🎉 Szybki start dla nowego admina

```bash
# 1. Sklonuj repozytorium
git clone https://github.com/[twoje-repo]/cennik.git
cd cennik

# 2. Zainstaluj Python (jeśli chcesz scraper)
pip install -r requirements-txt.txt

# 3. Edytuj promocję
# Otwórz: edytor-promocji.html w przeglądarce

# 4. Zaktualizuj dane
# Edytuj pricing-data.json

# 5. Wdróż
git add pricing-data.json
git commit -m "Aktualizacja promocji"
git push

# 6. Zobacz zmiany
# Odśwież: https://[twoje-repo].github.io/cennik/
```

---

---

## 🔄 Historia zmian

### v2.0 (2025-10-09)
- ✅ Dodano 4 prędkości ładowania (DC Mid 50-125kW)
- ✅ Dynamiczne suwaki proporcji z auto-normalizacją
- ✅ Auto-save wszystkich ustawień
- ✅ Selenium scraper dla Orlen (promo + standardowe)
- ✅ GitHub Actions z Chrome/ChromeDriver
- ✅ Automatyczne wykrywanie promocji i dat

### v1.0 (2025-10-02)
- ✅ Tryb jednorazowy i miesięczny
- ✅ GreenWay (3 plany) + Orlen
- ✅ Promocje czasowe
- ✅ Próg opłacalności

---

**Ostatnia aktualizacja:** 2025-10-09
**Maintainer:** EV Charging Calculator Team
