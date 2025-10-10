#!/usr/bin/env python3
"""
Scraper cenników operatorów ładowarek EV w Polsce
Autor: EV Charging Price Scraper
Data: 2025
"""

import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import PyPDF2
import io
import re
import logging
from typing import Dict, List, Optional, Any

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EVChargingPriceScraper:
    """Główna klasa do scrapowania cenników operatorów ładowarek"""
    
    def __init__(self):
        self.pricing_data = {
            "lastUpdate": datetime.now().isoformat(),
            "operators": {}
        }
        
    def scrape_greenway(self) -> Dict[str, Any]:
        """Scrapuje cennik GreenWay z PDF"""
        logger.info("Rozpoczynam scrapowanie GreenWay...")
        
        try:
            # URL do PDF z cennikiem GreenWay
            pdf_url = "https://data.greenway.sk/clientzone/pl/GWP_pricelist_PL.pdf"
            
            response = requests.get(pdf_url, timeout=30)
            response.raise_for_status()
            
            # Parsowanie PDF
            pdf_file = io.BytesIO(response.content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            greenway_data = {
                "name": "GreenWay",
                "color": "#10b981",
                "subscriptions": [],
                "promotions": []
            }
            
            # Wyciąganie tekstu ze wszystkich stron
            full_text = ""
            for page in pdf_reader.pages:
                full_text += page.extract_text()
            
            # Parsowanie cen - czytamy z tabeli
            # Linia: "AC 2) 1,60 zł  1,75 zł  1,95 zł  2,05 zł"
            # Kolumny: Max, Plus, Standard, Jednorazowe
            ac_line_match = re.search(r'AC[^0-9]*(\d+[,\.]\d+)[^0-9]+(\d+[,\.]\d+)[^0-9]+(\d+[,\.]\d+)', full_text)
            dc_line_match = re.search(r'DC[^0-9]*(\d+[,\.]\d+)[^0-9]+(\d+[,\.]\d+)[^0-9]+(\d+[,\.]\d+)', full_text)
            fee_line_match = re.search(r'Miesięczna opłata[^0-9]*(\d+[,\.]\d+)[^0-9]+(\d+[,\.]\d+)', full_text, re.IGNORECASE)

            if ac_line_match and dc_line_match:
                # Kolumna 1 = Max, 2 = Plus, 3 = Standard
                ac_max = float(ac_line_match.group(1).replace(',', '.'))
                ac_plus = float(ac_line_match.group(2).replace(',', '.'))
                ac_standard = float(ac_line_match.group(3).replace(',', '.'))

                dc_max = float(dc_line_match.group(1).replace(',', '.'))
                dc_plus = float(dc_line_match.group(2).replace(',', '.'))
                dc_standard = float(dc_line_match.group(3).replace(',', '.'))

                # Energia Standard (bez abonamentu)
                greenway_data["subscriptions"].append({
                    "id": "greenway_standard",
                    "name": "Energia Standard",
                    "monthlyCost": 0,
                    "prices": {
                        "ac": ac_standard,
                        "dc": dc_standard,
                        "dc_mid": dc_standard,
                        "hpc": dc_standard
                    },
                    "benefits": []
                })
            else:
                logger.warning("Nie znaleziono cen Standard w PDF, używam domyślnych")
                greenway_data["subscriptions"].append({
                    "id": "greenway_standard",
                    "name": "Energia Standard",
                    "monthlyCost": 0,
                    "prices": {"ac": 1.95, "dc": 3.15, "dc_mid": 3.15, "hpc": 3.15},
                    "benefits": []
                })
            
            # Energia Plus (używamy tych samych zmiennych co Standard)
            if ac_line_match and dc_line_match and fee_line_match:
                fee_max = float(fee_line_match.group(1).replace(',', '.'))
                fee_plus = float(fee_line_match.group(2).replace(',', '.'))

                greenway_data["subscriptions"].append({
                    "id": "greenway_plus",
                    "name": "Energia Plus",
                    "monthlyCost": fee_plus,
                    "prices": {
                        "ac": ac_plus,
                        "dc": dc_plus,
                        "dc_mid": dc_plus,
                        "hpc": dc_plus
                    },
                    "benefits": ["Dla średniego zużycia 50-200 kWh/mies"]
                })

                # Energia Max
                greenway_data["subscriptions"].append({
                    "id": "greenway_max",
                    "name": "Energia Max",
                    "monthlyCost": fee_max,
                    "prices": {
                        "ac": ac_max,
                        "dc": dc_max,
                        "dc_mid": dc_max,
                        "hpc": dc_max
                    },
                    "benefits": ["Dla wysokiego zużycia >200 kWh/mies"]
                })
            else:
                logger.warning("Nie znaleziono cen Plus/Max w PDF, używam domyślnych")
                greenway_data["subscriptions"].append({
                    "id": "greenway_plus",
                    "name": "Energia Plus",
                    "monthlyCost": 29.99,
                    "prices": {"ac": 1.75, "dc": 2.40, "dc_mid": 2.40, "hpc": 2.40},
                    "benefits": ["Dla średniego zużycia 50-200 kWh/mies"]
                })
                greenway_data["subscriptions"].append({
                    "id": "greenway_max",
                    "name": "Energia Max",
                    "monthlyCost": 79.99,
                    "prices": {"ac": 1.60, "dc": 2.10, "dc_mid": 2.10, "hpc": 2.10},
                    "benefits": ["Dla wysokiego zużycia >200 kWh/mies"]
                })
            
            logger.info(f"GreenWay: znaleziono {len(greenway_data['subscriptions'])} plany")
            return greenway_data
            
        except Exception as e:
            logger.error(f"Błąd przy scrapowaniu GreenWay: {e}")
            # Zwracamy domyślne dane w razie błędu
            return self.get_default_greenway_data()
    
    def scrape_orlen(self) -> Dict[str, Any]:
        """Scrapuje cennik Orlen Charge (wymaga Selenium)

        Sprawdza dwie strony:
        1. /cennik-promo/ - jeśli istnieje promocja, pobiera ceny standard + promo + daty
        2. /cennik/ - fallback, pobiera tylko ceny standardowe
        """
        logger.info("Rozpoczynam scrapowanie Orlen Charge...")

        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
        except ImportError:
            logger.warning("Selenium nie jest zainstalowany, używam danych domyślnych")
            return self.get_default_orlen_data()

        driver = None
        try:
            orlen_data = {
                "name": "Orlen Charge",
                "color": "#ef4444",
                "subscriptions": [],
                "promotions": []
            }

            # Konfiguracja Chrome headless
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')

            # W GitHub Actions używamy chromium-browser
            import os
            if os.environ.get('CI'):
                chrome_options.binary_location = '/usr/bin/chromium-browser'

            logger.info("Uruchamiam Chrome...")
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(30)

            standard_prices = {}
            promo_prices = {}
            promo_dates = None

            # NAJPIERW: Sprawdź stronę promocyjną
            try:
                promo_url = "https://orlencharge.pl/cennik-promo/"
                logger.info(f"Sprawdzam stronę promocyjną: {promo_url}")
                driver.get(promo_url)

                WebDriverWait(driver, 15).until(
                    lambda d: d.execute_script('return document.readyState') == 'complete'
                )

                import time
                time.sleep(3)

                page_text = driver.find_element(By.TAG_NAME, "body").text
                logger.info(f"Strona promocyjna: {len(page_text)} znaków")

                # Parsowanie cen PROMOCYJNYCH (tabela ma 2 kolumny: standard | promo)
                # Format: "AC 1,95 PLN/kWh 1,46 PLN/kWh"
                patterns = [
                    # AC - 2 kolumny (standard, promo)
                    (r'AC\s+(\d+[,\.]\d+)\s+PLN/kWh\s+(\d+[,\.]\d+)', 'ac'),
                    # DC ≤50kW
                    (r'DC[^0-9]*≤\s*50[^0-9]+(\d+[,\.]\d+)\s+PLN/kWh\s+(\d+[,\.]\d+)', 'dc'),
                    # DC 50-125kW
                    (r'DC[^0-9]+50[^0-9]+125[^0-9]+(\d+[,\.]\d+)\s+PLN/kWh\s+(\d+[,\.]\d+)', 'dc_mid'),
                    # DC >125kW
                    (r'DC[^0-9]+>\s*125[^0-9]+(\d+[,\.]\d+)\s+PLN/kWh\s+(\d+[,\.]\d+)', 'hpc'),
                ]

                for pattern, price_key in patterns:
                    match = re.search(pattern, page_text, re.IGNORECASE | re.DOTALL)
                    if match:
                        standard_prices[price_key] = float(match.group(1).replace(',', '.'))
                        promo_prices[price_key] = float(match.group(2).replace(',', '.'))
                        logger.info(f"{price_key}: standard={standard_prices[price_key]}, promo={promo_prices[price_key]}")

                # Parsowanie dat promocji
                # Format: "2 października 2025 r. godz. 9:00 do dnia 3 listopada 2025 r. godz. 9:00"
                date_pattern = r'(\d{1,2})\s+(\w+)\s+(\d{4}).*?do dnia\s+(\d{1,2})\s+(\w+)\s+(\d{4})'
                date_match = re.search(date_pattern, page_text, re.IGNORECASE)

                if date_match:
                    start_day, start_month_name, start_year, end_day, end_month_name, end_year = date_match.groups()

                    # Mapowanie nazw miesięcy
                    months = {
                        'stycznia': '01', 'lutego': '02', 'marca': '03', 'kwietnia': '04',
                        'maja': '05', 'czerwca': '06', 'lipca': '07', 'sierpnia': '08',
                        'września': '09', 'października': '10', 'listopada': '11', 'grudnia': '12'
                    }

                    start_month = months.get(start_month_name.lower(), '01')
                    end_month = months.get(end_month_name.lower(), '12')

                    promo_dates = {
                        'validFrom': f"{start_year}-{start_month}-{start_day.zfill(2)}",
                        'validTo': f"{end_year}-{end_month}-{end_day.zfill(2)}"
                    }
                    logger.info(f"Promocja: {start_day} {start_month_name} - {end_day} {end_month_name} {end_year}")

            except Exception as e:
                logger.warning(f"Brak strony promocyjnej lub błąd: {e}")

            # JEŚLI nie znaleziono cen, FALLBACK: /cennik/
            if not standard_prices:
                try:
                    url = "https://orlencharge.pl/cennik/"
                    logger.info(f"Fallback: ładuję stronę standardową: {url}")
                    driver.get(url)

                    WebDriverWait(driver, 15).until(
                        lambda d: d.execute_script('return document.readyState') == 'complete'
                    )

                    import time
                    time.sleep(3)

                    page_text = driver.find_element(By.TAG_NAME, "body").text
                    logger.info(f"Strona standardowa: {len(page_text)} znaków")

                    # Na stronie standardowej NIE MA promocji - tylko 1 kolumna
                    patterns = [
                        (r'AC[^0-9]*(\d+[,\.]\d+)\s+PLN/kWh', 'ac'),
                        (r'DC[^0-9]*≤\s*50[^0-9]+(\d+[,\.]\d+)\s+PLN/kWh', 'dc'),
                        (r'DC[^0-9]+50[^0-9]+125[^0-9]+(\d+[,\.]\d+)\s+PLN/kWh', 'dc_mid'),
                        (r'DC[^0-9]+>\s*125[^0-9]+(\d+[,\.]\d+)\s+PLN/kWh', 'hpc'),
                    ]

                    for pattern, price_key in patterns:
                        match = re.search(pattern, page_text, re.IGNORECASE)
                        if match:
                            standard_prices[price_key] = float(match.group(1).replace(',', '.'))
                            logger.info(f"{price_key}: {standard_prices[price_key]}")

                except Exception as e:
                    logger.error(f"Błąd ładowania strony standardowej: {e}")

            # Jeśli NADAL brak cen, użyj domyślnych
            if not standard_prices:
                logger.warning("Nie znaleziono żadnych cen, używam domyślnych")
                standard_prices = {
                    "ac": 1.95,
                    "dc": 2.69,
                    "dc_mid": 2.89,
                    "hpc": 3.19
                }

            # Dodaj cennik standardowy
            orlen_data["subscriptions"].append({
                "id": "orlen_standard",
                "name": "Bez abonamentu",
                "monthlyCost": 0,
                "prices": standard_prices,
                "benefits": []
            })

            # Dodaj promocję jeśli znaleziono
            if promo_prices and len(promo_prices) >= 4 and promo_dates:
                orlen_data["promotions"].append({
                    "name": "Promocja cenowa -25%",
                    "validFrom": promo_dates['validFrom'],
                    "validTo": promo_dates['validTo'],
                    "prices": promo_prices,
                    "conditions": ["Obowiązuje dla wszystkich użytkowników"]
                })
                logger.info(f"Dodano promocję: {len(promo_prices)} cen")

            logger.info(f"Orlen: {len(orlen_data['subscriptions'])} plany, {len(orlen_data['promotions'])} promocje")
            return orlen_data

        except Exception as e:
            logger.error(f"Błąd przy scrapowaniu Orlen: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return self.get_default_orlen_data()

        finally:
            if driver:
                driver.quit()
    
    def get_default_greenway_data(self) -> Dict[str, Any]:
        """Zwraca domyślne dane GreenWay z dc_mid (duplikacja DC)"""
        return {
            "name": "GreenWay",
            "color": "#10b981",
            "subscriptions": [
                {
                    "id": "greenway_standard",
                    "name": "Energia Standard",
                    "monthlyCost": 0,
                    "prices": {"ac": 1.95, "dc": 3.15, "dc_mid": 3.15, "hpc": 3.15},
                    "benefits": []
                },
                {
                    "id": "greenway_plus",
                    "name": "Energia Plus",
                    "monthlyCost": 29.99,
                    "prices": {"ac": 1.75, "dc": 2.40, "dc_mid": 2.40, "hpc": 2.40},
                    "benefits": ["Dla średniego zużycia 50-200 kWh/mies"]
                },
                {
                    "id": "greenway_max",
                    "name": "Energia Max",
                    "monthlyCost": 79.99,
                    "prices": {"ac": 1.60, "dc": 2.10, "dc_mid": 2.10, "hpc": 2.10},
                    "benefits": ["Dla wysokiego zużycia >200 kWh/mies"]
                }
            ],
            "promotions": []
        }
    
    def get_default_orlen_data(self) -> Dict[str, Any]:
        """Zwraca domyślne dane Orlen z 4 przedziałami DC"""
        return {
            "name": "Orlen Charge",
            "color": "#ef4444",
            "subscriptions": [
                {
                    "id": "orlen_standard",
                    "name": "Bez abonamentu",
                    "monthlyCost": 0,
                    "prices": {
                        "ac": 1.95,
                        "dc": 2.69,
                        "dc_mid": 2.89,
                        "hpc": 3.19
                    },
                    "benefits": []
                }
            ],
            "promotions": [
                {
                    "name": "Promocja cenowa -25%",
                    "validFrom": "2025-10-02",
                    "validTo": "2025-11-03",
                    "prices": {
                        "ac": 1.46,
                        "dc": 2.02,
                        "dc_mid": 2.17,
                        "hpc": 2.39
                    },
                    "conditions": ["Obowiązuje dla wszystkich użytkowników"]
                }
            ]
        }
    
    def check_additional_operators(self):
        """Miejsce na dodanie kolejnych operatorów w przyszłości"""
        # Tu można dodać scrapowanie innych operatorów
        # np. Ionity, Powerdot, Elocity itp.
        pass
    
    def save_to_file(self, filename: str = "pricing-data.json"):
        """Zapisuje dane do pliku JSON"""
        try:
            # Scrapuj wszystkich operatorów
            self.pricing_data["operators"]["greenway"] = self.scrape_greenway()
            self.pricing_data["operators"]["orlen"] = self.scrape_orlen()
            
            # Zapisz do pliku
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.pricing_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Dane zapisane do {filename}")
            print(f"[OK] Pomyslnie zaktualizowano cenniki!")
            print(f"GreenWay: {len(self.pricing_data['operators']['greenway']['subscriptions'])} plany")
            print(f"Orlen: {len(self.pricing_data['operators']['orlen']['subscriptions'])} plany, "
                  f"{len(self.pricing_data['operators']['orlen']['promotions'])} promocje")
            
        except Exception as e:
            logger.error(f"Błąd przy zapisywaniu danych: {e}")
            raise

def main():
    """Główna funkcja"""
    scraper = EVChargingPriceScraper()
    scraper.save_to_file()

if __name__ == "__main__":
    main()