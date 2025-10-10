# Konfiguracja GitHub Pages

## Problem
Strona https://bartorux.github.io/cennik-ev/ nie ładuje automatycznie danych - wymaga kliknięcia "Odśwież ceny".

## Rozwiązanie

### Krok 1: Włącz GitHub Pages
1. Wejdź na: https://github.com/bartorux/cennik-ev/settings/pages
2. W sekcji **"Source"**:
   - Wybierz: **"Deploy from a branch"**
   - Branch: **`main`**
   - Folder: **`/ (root)`**
3. Kliknij **"Save"**
4. Poczekaj 2-3 minuty

### Krok 2: Sprawdź czy działa
1. Otwórz: https://bartorux.github.io/cennik-ev/
2. Sprawdź czy dane ładują się automatycznie (bez klikania "Odśwież ceny")
3. Otwórz konsolę przeglądarki (F12) i sprawdź czy są błędy

### Krok 3: Sprawdź plik pricing-data.json
Upewnij się, że plik jest dostępny pod adresem:
https://bartorux.github.io/cennik-ev/pricing-data.json

### Co już zostało naprawione w kodzie?
✅ Dodano plik `.nojekyll` (wyłącza Jekyll na GitHub Pages)
✅ Poprawiono ścieżkę do `pricing-data.json` (z `./pricing-data.json` na `pricing-data.json`)
✅ Zaktualizowano dane awaryjne (dodano IONITY i dc_mid)
✅ Dodano lepsze logowanie błędów w konsoli

### Debugowanie
Jeśli strona nadal nie działa, otwórz konsolę (F12) i sprawdź:
- Czy pojawia się komunikat: `✅ Dane cenowe załadowane pomyślnie`
- Czy są błędy 404 (plik nie znaleziony)
- Czy są błędy CORS (Cross-Origin Resource Sharing)

### Statusy w interfejsie
Po poprawnym załadowaniu zobaczysz:
- ✅ **Ładowanie danych...** → aktualna data
- ✅ **Ostatnia aktualizacja: --** → rzeczywisty czas (np. "2h temu")
- ✅ **Sprawdzanie promocji...** → info o promocjach lub "Brak aktywnych promocji"
