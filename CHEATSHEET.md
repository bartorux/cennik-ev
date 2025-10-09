# ⚡ Ściąga Administratora

## 🎯 Najczęstsze zadania

### 1. Aktualizacja promocji Orlen (ręcznie)

```bash
# Krok 1: Sprawdź promocję
# https://orlencharge.pl/cennik/ → "Sprawdź cenę"

# Krok 2: Edytuj lokalnie
start edytor-promocji.html

# Krok 3: Wdróż zmiany
git add pricing-data.json
git commit -m "Promocja Orlen: -25% do 3.11"
git push
```

⏱️ **Czas wdrożenia:** ~2 minuty

---

### 2. Wyłączenie promocji

**W pricing-data.json:**
```json
"orlen": {
  "promotions": []
}
```

```bash
git add pricing-data.json
git commit -m "Wyłączenie promocji Orlen"
git push
```

---

### 3. Ręczne uruchomienie scrapera

**Lokalnie:**
```bash
python scraper-python.py
git add pricing-data.json
git commit -m "Aktualizacja cen (ręczna)"
git push
```

**Przez GitHub Actions:**
1. GitHub → Actions → "Aktualizacja Cen EV"
2. Run workflow → Run

---

### 4. Sprawdzenie logów automatyzacji

1. GitHub → **Actions**
2. Kliknij na ostatnie uruchomienie
3. Zobacz czy są zmiany

---

## 📁 Struktura plików

### ✅ Commituj (publiczne):
```
index.html                      # Kalkulator
pricing-data.json               # Dane
.github/workflows/*.yml         # Automatyzacja
scraper-python.py               # Scraper (opcja)
requirements-txt.txt            # Zależności (opcja)
```

### ❌ NIE commituj (prywatne):
```
edytor-promocji.html           # ← TYLKO U CIEBIE!
updated-html.html              # Stara wersja
test_*.py                      # Testy
*.log                          # Logi
```

---

## 🐛 Najczęstsze problemy

| Problem | Rozwiązanie |
|---------|-------------|
| Strona nie działa | Settings → Pages → sprawdź Source = main |
| Actions failują | Settings → Actions → "Read and write" |
| Edytor w repo | Sprawdź `.gitignore` i usuń z Git |
| Promocja nie działa | Sprawdź daty (YYYY-MM-DD) |
| Scraper fails | Użyje fallback - to OK |

---

## 🔗 Linki

- **Strona live:** https://[twoja-nazwa].github.io/[repo]/
- **Repo:** https://github.com/[twoja-nazwa]/[repo]
- **Actions:** https://github.com/[twoja-nazwa]/[repo]/actions
- **Orlen ceny:** https://orlencharge.pl/cennik/

---

## 📝 Szablony commit messages

```bash
# Promocje
git commit -m "Nowa promocja Orlen -30%"
git commit -m "Wyłączenie promocji Orlen"

# Automatyzacja
git commit -m "🤖 Auto-update cen $(date)"

# Funkcje
git commit -m "Dodanie operatora Ionity"
git commit -m "Poprawka kalkulatora"

# Pilne
git commit -m "HOTFIX: Błąd obliczania kosztu"
```

---

## ⚙️ Komendy Git

```bash
# Status
git status

# Dodaj pliki
git add pricing-data.json
git add .

# Commit
git commit -m "Wiadomość"

# Push
git push

# Historia
git log --oneline

# Cofnij zmiany (OSTROŻNIE!)
git checkout -- pricing-data.json
```

---

**Zachowaj ten plik!** 📌
