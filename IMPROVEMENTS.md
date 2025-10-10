# 📋 Lista Ulepszeń - Kalkulator EV

Ten plik zawiera listę potencjalnych ulepszeń dla projektu, pogrupowanych według priorytetów.

**Ostatnia aktualizacja:** 2025-10-10

---

## ✅ UKOŃCZONE (Quick Wins - 2025-10-10)

- [x] Ukryj kategorie AC/DC dla IONITY (pokazuj tylko HPC) - commit `57c66bc`
- [x] Dodaj favicon i meta tagi SEO/OG - commit `85a2b0c`
- [x] Dodaj loading spinner przy inicjalizacji - commit `4c44cb8`
- [x] Dodaj walidację min/max dla inputów - commit `f3f2e11`
- [x] Refactor: funkcja `saveSettings()` zamiast 17x duplikacja - commit `b9f459c`

---

## 🔴 HIGH PRIORITY (32 zadania)

### UX/UI Improvements (8)

1. **Brak feedback przy zapisywaniu**
   - Toasty/notyfikacje po zapisaniu ustawień
   - Użytkownik nie wie czy zmiany zostały zachowane
   - **Czas:** 30 min

2. **Brak instrukcji onboarding**
   - Tooltipsy wyjaśniające różnicę między trybami
   - Przykładowe scenariusze użycia
   - **Czas:** 2h

3. **Proporcje ładowania - niejasny UX**
   - Dodać wizualizację (pie chart) pokazującą proporcje
   - Lepsze wyjaśnienie auto-normalizacji
   - **Czas:** 1.5h

4. **Responsywność - jeden breakpoint (968px)**
   - Dodać breakpointy dla tabletów (768px-968px)
   - Optymalizacja dla małych telefonów (<375px)
   - **Czas:** 2h

5. **Sticky settings panel na mobile nie działa**
   - `position: sticky` wyłączone na mobile
   - **Czas:** 30 min

6. **Suwaki proporcji za małe na mobile**
   - Powiększone thumb dla touchscreen
   - **Czas:** 30 min

7. **Grid operatorów - 1 kolumna na mobile**
   - Rozważyć collapse/accordion dla lepszego UX
   - **Czas:** 1h

8. **Brak rankingu - filtrowanie**
   - Ukrywanie operatorów których nie używasz
   - Sortowanie według kryteriów
   - **Czas:** 1.5h

### SEO i Meta Tagi (4)

9. **Brak strukturalnych meta tagów** ✅ DONE
   - Meta description, keywords, canonical - **ZROBIONE**

10. **Brak Open Graph tags** ✅ DONE
    - og:image, og:title, og:description - **ZROBIONE**

11. **Brak Schema.org markup**
    - JSON-LD z strukturalnymi danymi (SoftwareApplication)
    - Rich snippets w Google (gwiazdki, ceny)
    - **Czas:** 1h

12. **Brak sitemap.xml i robots.txt**
    - **Czas:** 20 min

### Accessibility (4)

13. **Zero ARIA labels**
    - Dodać aria-label, aria-describedby, aria-live
    - **Czas:** 2h

14. **Brak focus indicators dla keyboard navigation**
    - Widoczne :focus dla użytkowników klawiaturowych
    - **Czas:** 30 min

15. **Suwaki bez labelów dla AT**
    - aria-valuemin, aria-valuemax, aria-valuenow
    - **Czas:** 1h

16. **Brak skip-to-content link**
    - Link do przeskoczenia headera
    - **Czas:** 20 min

### Funkcjonalności (3)

17. **Kalkulator oszczędności przy przejściu na EV**
    - Porównanie EV vs benzynowe/diesel
    - "100 km w EV = 15 zł vs spalinówka = 45 zł"
    - **Czas:** 3h

18. **Lokalizator ładowarek**
    - Integracja z mapą (Google Maps / OpenStreetMap)
    - Filtrowanie po mocy (AC/DC/HPC)
    - **Czas:** 8h (duże zadanie)

19. **Powiadomienia o promocjach**
    - Zapis email/push notifications
    - Backend (np. Firebase, Supabase)
    - **Czas:** 6h

### Code Quality (4)

20. **19x duplikacja `localStorage.setItem`** ✅ DONE
    - Funkcja `saveSettings()` - **ZROBIONE**

21. **Brak debounce na sliderach**
    - Każdy ruch wywołuje `calculateAndDisplay()` → może lagować
    - **Czas:** 30 min

22. **Brak cache dla obliczeń**
    - Memoizacja wyników calculateCosts()
    - **Czas:** 1h

23. **28 wywołań `console.log` w produkcji**
    - Usunąć lub warunkować (tylko dev mode)
    - **Czas:** 30 min

### Error Handling (4)

24. **Brak walidacji inputów** ✅ DONE
    - Funkcja `validateInput()` - **ZROBIONE**

25. **Race condition przy ładowaniu danych**
    - Użytkownik może kliknąć przed załadowaniem
    - **Czas:** 1h

26. **Brak obsługi offline**
    - Service Worker + cached data
    - **Czas:** 2h

27. **IONITY ma ceny "999" dla AC/DC** ✅ DONE
    - Ukrywanie niedostępnych opcji - **ZROBIONE**

### Analytics (2)

28. **Brak trackingu konwersji**
    - Google Analytics / Plausible
    - Eventi: wybór operatora, zmiana trybu, obliczenia
    - **Czas:** 1h

29. **Brak A/B testingu**
    - Framework do testowania różnych wersji UI
    - **Czas:** 3h

### Developer Experience (3)

30. **Brak testów jednostkowych**
    - Jest `test-frontend.html` ale tylko dla JSON
    - Testy dla calculateCosts(), normalizePercentages()
    - **Czas:** 4h

31. **Brak lintingu (ESLint, Prettier)**
    - Niespójne formatowanie (2 vs 4 spacje)
    - **Czas:** 1h

32. **Brak CI/CD dla frontendu**
    - GitHub Actions tylko dla scrapera
    - Automatyczne testy HTML przy PR
    - **Czas:** 2h

---

## 🟡 MEDIUM PRIORITY (30 zadań)

### UX Improvements (5)

33. **Brak dark mode**
    - Tylko jasny motyw
    - **Czas:** 3h

34. **Brak wizualizacji cen historycznych**
    - Wykres zmian cen w ostatnich miesiącach
    - **Czas:** 4h

35. **Brak porównania "co jeśli"**
    - Dwa scenariusze obok siebie
    - **Czas:** 2h

36. **Landscape mode optimization**
    - Telefon w poziomie - lepszy layout
    - **Czas:** 1h

37. **Font-size nie skaluje się**
    - Użycie `clamp()` dla responsywnych fontów
    - **Czas:** 30 min

### Funkcjonalności (4)

38. **Kalkulator czasu ładowania**
    - Na podstawie mocy ładowarki i pojemności baterii
    - "80 kWh bateria na HPC 150kW = ~32 min do 80%"
    - **Czas:** 2h

39. **Porównanie z ładowaniem domowym**
    - Taryfa G11/G12 z cenami prądu z gniazdka
    - **Czas:** 2h

40. **Historia obliczeń**
    - Zapisywanie ostatnich 5-10 scenariuszy
    - **Czas:** 2h

41. **Sugestie optymalizacji**
    - Algorytm sugerujący najlepszy plan
    - "Zmień z Plus na Max jeśli >180 kWh/mies"
    - **Czas:** 3h

### Performance (5)

42. **Brak minifikacji**
    - HTML/CSS/JS nie są zminifikowane
    - **Czas:** 30 min (setup build process)

43. **Fallback data hardcoded w JS**
    - 100+ linii w kodzie (już są w JSON)
    - **Czas:** 1h

44. **Brak Service Worker / PWA**
    - Offline support, instalacja jako app
    - **Czas:** 4h

45. **Brak lazy loading dla wykresu**
    - Chart renderowany nawet gdy niewidoczny
    - **Czas:** 1h

46. **Całe CSS/JS inline w HTML (2233 linii)**
    - Separacja do zewnętrznych plików
    - Lepsze caching
    - **Czas:** 2h

### SEO (2)

47. **Title jest generyczny**
    - Dodać long-tail keywords
    - **Czas:** 15 min

48. **Brak lang variants (hreflang)**
    - Jeśli planujesz wersje EN, DE, CZ
    - **Czas:** 30 min

### Accessibility (3)

49. **Kontrast kolorów niezgodny z WCAG**
    - Niektóre małe teksty (#64748b na #f8fafc)
    - **Czas:** 1h

50. **Brak `lang` attribute na elementach obcojęzycznych**
    - Screen readery źle wymawiają
    - **Czas:** 30 min

51. **Checkboxy/Radio bez visible labels**
    - Niektóre tylko w onclick handlers
    - **Czas:** 1h

### Error Handling (3)

52. **Brak timeout dla fetch**
    - fetch() może wisieć w nieskończoność
    - **Czas:** 30 min

53. **Promocje nie są walidowane po stronie frontendu**
    - Błędna data w JSON → crash
    - **Czas:** 30 min

54. **Suwaki proporcji mogą nie sumować się do 100%**
    - Zaokrąglenia → 99% lub 101%
    - **Czas:** 30 min

### Analytics (3)

55. **Brak heatmap**
    - Hotjar / Microsoft Clarity
    - **Czas:** 30 min (setup)

56. **Brak error trackingu (Sentry)**
    - Błędy JS u użytkowników
    - **Czas:** 1h

57. **Brak User Feedback widget**
    - Łatwe zgłaszanie błędów/sugestii
    - **Czas:** 2h

### Developer Experience (3)

58. **Brak TypeScript**
    - Tylko vanilla JS
    - **Czas:** 8h (duża migracja)

59. **Brak komponentyzacji**
    - Cały kod w jednym pliku
    - Funkcje 100+ linii
    - **Czas:** 6h (refactor)

60. **Dokumentacja techniczna tylko w CLAUDE.md**
    - Brak JSDoc w kodzie
    - **Czas:** 3h

### Nice-to-Have (6)

61. **Eksport wyników do PDF/PNG**
    - html2canvas / jsPDF
    - **Czas:** 3h

62. **Udostępnianie wyników przez link**
    - URL encoding ustawień
    - **Czas:** 2h

---

## 🟢 LOW PRIORITY (19 zadań)

### UX (2)

63. **Wizualizacje historyczne**
    - Trendy cen w czasie
    - **Czas:** 4h

64. **Porównanie "co jeśli"**
    - Split screen dla 2 scenariuszy
    - **Czas:** 3h

### Funkcjonalności (2)

65. **Kalkulator kosztu podróży**
    - Wprowadź trasę (km) → koszt ładowania
    - **Czas:** 3h

66. **Tryb porównania flotowego**
    - Dla firm - 5, 10, 50 pojazdów
    - **Czas:** 4h

### Performance (2)

67. **Brak tree-shaking**
    - Przyszłościowe (obecnie brak bibliotek)
    - **Czas:** -

68. **Brak CDN dla statycznych assetów**
    - GitHub Pages ma już globalny CDN
    - **Czas:** -

### SEO (1)

69. **Brak Google Analytics / Plausible** (duplikat #28)

### Accessibility (1)

70. **Brak prefers-reduced-motion**
    - Animacje zawsze włączone
    - **Czas:** 30 min

### Error Handling (1)

71. **Brak obsługi starych przeglądarek**
    - IE11 się wysypie (ale w 2025 <0.1% rynku)
    - **Czas:** -

### Developer (1)

72. **Brak changelog**
    - Historia zmian tylko w Git
    - **Czas:** 30 min (setup)

### Nice-to-Have (11)

73. **Porównanie z krajami sąsiednimi**
    - "W Niemczech to samo = X zł"
    - **Czas:** 6h

74. **Widget do embedowania**
    - `<script>` tag dla forów/blogów
    - **Czas:** 4h

75. **Notyfikacje o nowych promocjach**
    - Email/Push (duplikat #19)

76. **Porównanie z rokiem poprzednim**
    - "Ceny wzrosły o 8% r/r"
    - **Czas:** 3h

77. **Kalkulator zwrotu z abonamentu**
    - "Po 3 miesiącach zaoszczędzisz X zł"
    - **Czas:** 2h

78. **Gamifikacja**
    - "Zaoszczędziłeś 500 zł"
    - **Czas:** 4h

79. **Integracja z aplikacjami operatorów**
    - Deep link do Orlen Charge app
    - **Czas:** 3h (wymaga partnerstw)

80. **Brak environment variables**
    - Wszystko hardcoded
    - **Czas:** 1h

81. **Brak localStorage error handling**
    - Safari private mode może crashować
    - **Status:** ✅ CZĘŚCIOWO DONE (funkcja saveSettings ma try-catch)
    - **Czas:** 10 min

---

## 📊 PODSUMOWANIE

### Status realizacji:
- ✅ **Ukończone:** 5/81 (6.2%)
- 🔴 **High Priority:** 32 zadania (~80h pracy)
- 🟡 **Medium Priority:** 30 zadań (~85h pracy)
- 🟢 **Low Priority:** 19 zadań (~50h pracy)

### Quick Wins (łatwe + duży impact):
1. ✅ ~~Favicon i meta tagi SEO~~ - DONE
2. ✅ ~~Loading spinner~~ - DONE
3. ✅ ~~Walidacja inputów~~ - DONE
4. ✅ ~~Funkcja `saveSettings()`~~ - DONE
5. ✅ ~~Ukryj IONITY dla AC/DC~~ - DONE
6. **Debounce na sliderach** - 30 min (#21)
7. **Usuń console.log z produkcji** - 30 min (#23)
8. **Google Analytics** - 1h (#28)
9. **Responsywność mobile** - 2h (#4)
10. **Podstawowe ARIA labels** - 2h (#13)

### Duże zadania strategiczne:
1. **Lokalizator ładowarek** - 8h (#18)
2. **Kalkulator EV vs paliwo** - 3h (#17)
3. **Service Worker / PWA** - 4h (#44)
4. **TypeScript migration** - 8h (#58)
5. **Testy jednostkowe** - 4h (#30)

---

## 🎯 Sugerowana kolejność realizacji:

### Sprint 1: UX i SEO (10h)
- [ ] Debounce na sliderach (#21)
- [ ] Usuń console.log (#23)
- [ ] Google Analytics (#28)
- [ ] Responsywność mobile (#4)
- [ ] ARIA labels (#13)
- [ ] Schema.org markup (#11)
- [ ] Sitemap i robots.txt (#12)

### Sprint 2: Funkcjonalności core (15h)
- [ ] Kalkulator EV vs paliwo (#17)
- [ ] Kalkulator czasu ładowania (#38)
- [ ] Porównanie z ładowaniem domowym (#39)
- [ ] Historia obliczeń (#40)
- [ ] Eksport do PDF (#61)

### Sprint 3: Performance i PWA (10h)
- [ ] Service Worker (#44)
- [ ] Minifikacja (#42)
- [ ] Separacja CSS/JS (#46)
- [ ] Cache dla obliczeń (#22)
- [ ] Lazy loading (#45)

### Sprint 4: Developer Experience (10h)
- [ ] Testy jednostkowe (#30)
- [ ] ESLint + Prettier (#31)
- [ ] CI/CD (#32)
- [ ] JSDoc dokumentacja (#60)

### Sprint 5: Advanced Features (20h)
- [ ] Lokalizator ładowarek (#18)
- [ ] Powiadomienia o promocjach (#19)
- [ ] Dark mode (#33)
- [ ] Wizualizacja historii cen (#34)

---

**Uwagi:**
- Czas podany jest szacunkowy dla jednej osoby
- Priorytety mogą się zmieniać w zależności od feedbacku użytkowników
- Niektóre zadania można zrobić równolegle
- Quick wins dają największy ROI (return on investment)
