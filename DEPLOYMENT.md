# 🚀 Instrukcja Wdrożenia na GitHub Pages

## Krok 1: Utwórz repozytorium na GitHub

1. Wejdź na https://github.com/new
2. Nazwa: `cennik-ev` (lub dowolna inna)
3. Widoczność: **Public** (dla GitHub Pages darmowe)
4. **NIE** zaznaczaj "Add a README" (mamy już)
5. Kliknij **Create repository**

---

## Krok 2: Dodaj pliki do repozytorium

### Z linii komend (Git Bash / Terminal):

```bash
# Przejdź do folderu projektu
cd c:/Users/57000023/Documents/cennik

# Inicjalizuj Git (jeśli jeszcze nie)
git init

# Dodaj wszystkie pliki
git add index.html pricing-data.json CLAUDE.md README.md .gitignore
git add .github/workflows/update-prices.yml
git add scraper-python.py requirements-txt.txt

# Pierwszy commit
git commit -m "🎉 Pierwsza wersja kalkulatora cen EV"

# Połącz z GitHub (zamień [twoja-nazwa] i [cennik-ev])
git remote add origin https://github.com/[twoja-nazwa]/[cennik-ev].git

# Wyślij na GitHub
git branch -M main
git push -u origin main
```

### Przez GitHub Desktop (łatwiejsze):

1. Otwórz GitHub Desktop
2. File → Add Local Repository
3. Wybierz folder: `c:\Users\57000023\Documents\cennik`
4. Kliknij "Publish repository"
5. Wybierz nazwę i kliknij "Publish"

---

## Krok 3: Włącz GitHub Pages

1. Wejdź na stronę swojego repo: `https://github.com/[twoja-nazwa]/[cennik-ev]`
2. Kliknij **Settings** (u góry)
3. W menu bocznym kliknij **Pages**
4. W sekcji "Source" wybierz:
   - Branch: **main**
   - Folder: **/ (root)**
5. Kliknij **Save**
6. Poczekaj ~2 minuty

**Twoja strona będzie dostępna pod:**
`https://[twoja-nazwa].github.io/[cennik-ev]/`

---

## Krok 4: Sprawdź czy działa

1. Otwórz link: `https://[twoja-nazwa].github.io/[cennik-ev]/`
2. Powinieneś zobaczyć kalkulator
3. Sprawdź czy:
   - ✅ Dane operatorów się ładują
   - ✅ Promocja Orlen jest widoczna
   - ✅ Obliczenia działają
   - ✅ Zmiana trybów działa

---

## Krok 5: Włącz GitHub Actions (automatyzacja)

### Konfiguracja uprawnień:

1. W repozytorium wejdź: **Settings** → **Actions** → **General**
2. Przewiń do "Workflow permissions"
3. Zaznacz: **Read and write permissions**
4. Kliknij **Save**

### Testuj workflow:

1. Wejdź w zakładkę **Actions** (u góry)
2. Zobaczysz workflow: "Aktualizacja Cen EV"
3. Kliknij **Run workflow** → **Run workflow**
4. Obserwuj wykonanie (zielony ✅ = OK)

**Od teraz scraper będzie działał automatycznie co 6 godzin!**

---

## Krok 6: Zarządzanie promocjami (Ty)

### Aktualizacja promocji Orlen:

```bash
# 1. Sprawdź promocję na: https://orlencharge.pl/cennik/

# 2. Otwórz edytor LOKALNIE (nie commituj go!)
start edytor-promocji.html

# 3. Wypełnij formularz i wygeneruj JSON

# 4. Edytuj pricing-data.json

# 5. Commit i push
git add pricing-data.json
git commit -m "Aktualizacja promocji Orlen -30%"
git push

# 6. Strona zaktualizuje się automatycznie w ~2 min
```

### Wyłączenie promocji:

```json
// W pricing-data.json → "orlen" → "promotions":
"promotions": []
```

---

## 🔐 Bezpieczeństwo edytora

**WAŻNE:** Plik `edytor-promocji.html` jest w `.gitignore` - **nie będzie** publikowany!

### Sprawdź czy edytor jest bezpieczny:

```bash
# Ten plik NIE powinien być śledzony przez Git
git status

# Nie powinien pokazywać "edytor-promocji.html"
```

### Jak używać edytora:

1. ✅ **Lokalnie na swoim PC** - otwórz bezpośrednio w przeglądarce
2. ❌ **NIE** umieszczaj go na GitHub Pages
3. ❌ **NIE** commituj do repozytorium

---

## 📊 Monitorowanie

### Sprawdź logi GitHub Actions:

1. Zakładka **Actions**
2. Kliknij na konkretne uruchomienie
3. Zobacz logi - czy scraper znalazł nowe ceny

### Sprawdź historię commitów:

```bash
git log --oneline --graph
```

Zobaczysz commity:
- 🤖 Automatyczne (przez GitHub Actions)
- 👤 Ręczne (Twoje aktualizacje promocji)

---

## 🛠️ Rozwiązywanie problemów

### Problem: GitHub Pages nie działa

**Rozwiązanie:**
1. Settings → Pages → sprawdź czy "Source" = main + / (root)
2. Sprawdź czy `index.html` istnieje w repo
3. Poczekaj 5 minut i odśwież

### Problem: GitHub Actions failuje

**Rozwiązanie:**
1. Actions → kliknij na czerwony ❌
2. Zobacz logi błędu
3. Najczęściej: brak uprawnień do zapisu
   - Settings → Actions → General → "Read and write permissions"

### Problem: Scraper nie znajduje cen GreenWay

**Rozwiązanie:**
- To normalne! PDF może się zmienić
- Scraper użyje danych awaryjnych (fallback)
- Możesz ręcznie zaktualizować w `scraper-python.py` → `get_default_greenway_data()`

### Problem: Promocja Orlen nie wyświetla się

**Sprawdź:**
1. Czy daty są poprawne (format: YYYY-MM-DD)
2. Czy promocja nie wygasła
3. Czy checkbox "Uwzględnij promocje" jest zaznaczony w kalkulatorze

---

## 🎉 Gotowe!

Twoja strona działa na:
`https://[twoja-nazwa].github.io/[cennik-ev]/`

### Co dalej?

- 📊 **Monitoruj** - Actions będą aktualizować ceny automatycznie
- 🎯 **Aktualizuj** - Promocje Orlen ręcznie przez edytor
- 📈 **Rozwijaj** - Dodaj nowych operatorów (zobacz CLAUDE.md)

---

**Potrzebujesz pomocy?**
- 📖 Dokumentacja: `README.md`
- 🤖 Techniczna: `CLAUDE.md`
- 💬 Issues: Utwórz w repozytorium
