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
            
            # Parsowanie cen - wzorce regex dla różnych planów
            # Energia Standard (bez abonamentu)
            standard_pattern = r"Energia Standard.*?AC.*?(\d+[,\.]\d+).*?DC.*?(\d+[,\.]\d+)"
            standard_match = re.search(standard_pattern, full_text, re.DOTALL)
            
            if standard_match:
                greenway_data["subscriptions"].append({
                    "id": "greenway_standard",
                    "name": "Energia Standard",
                    "monthlyCost": 0,
                    "prices": {
                        "ac": float(standard_match.group(1).replace(',', '.')),
                        "dc": float(standard_match.group(2).replace(',', '.')),
                        "hpc": float(standard_match.group(2).replace(',', '.'))  # GreenWay nie rozróżnia DC/HPC
                    },
                    "benefits": []
                })
            else:
                # Fallback - domyślne wartości jeśli nie znaleziono w PDF
                logger.warning("Nie znaleziono cen Standard w PDF, używam domyślnych")
                greenway_data["subscriptions"].append({
                    "id": "greenway_standard",
                    "name": "Energia Standard",
                    "monthlyCost": 0,
                    "prices": {"ac": 1.95, "dc": 3.15, "hpc": 3.15},
                    "benefits": []
                })
            
            # Energia Plus
            plus_pattern = r"Energia Plus.*?(\d+[,\.]\d+)\s*zł/mies.*?AC.*?(\d+[,\.]\d+).*?DC.*?(\d+[,\.]\d+)"
            plus_match = re.search(plus_pattern, full_text, re.DOTALL)
            
            if plus_match:
                greenway_data["subscriptions"].append({
                    "id": "greenway_plus",
                    "name": "Energia Plus",
                    "monthlyCost": float(plus_match.group(1).replace(',', '.')),
                    "prices": {
                        "ac": float(plus_match.group(2).replace(',', '.')),
                        "dc": float(plus_match.group(3).replace(',', '.')),
                        "hpc": float(plus_match.group(3).replace(',', '.'))
                    },
                    "benefits": ["Dla średniego zużycia 50-200 kWh/mies"]
                })
            else:
                logger.warning("Nie znaleziono cen Plus w PDF, używam domyślnych")
                greenway_data["subscriptions"].append({
                    "id": "greenway_plus",
                    "name": "Energia Plus",
                    "monthlyCost": 29.99,
                    "prices": {"ac": 1.75, "dc": 2.40, "hpc": 2.40},
                    "benefits": ["Dla średniego zużycia 50-200 kWh/mies"]
                })
            
            # Energia Max
            max_pattern = r"Energia Max.*?(\d+[,\.]\d+)\s*zł/mies.*?AC.*?(\d+[,\.]\d+).*?DC.*?(\d+[,\.]\d+)"
            max_match = re.search(max_pattern, full_text, re.DOTALL)
            
            if max_match:
                greenway_data["subscriptions"].append({
                    "id": "greenway_max",
                    "name": "Energia Max",
                    "monthlyCost": float(max_match.group(1).replace(',', '.')),
                    "prices": {
                        "ac": float(max_match.group(2).replace(',', '.')),
                        "dc": float(max_match.group(3).replace(',', '.')),
                        "hpc": float(max_match.group(3).replace(',', '.'))
                    },
                    "benefits": ["Dla wysokiego zużycia >200 kWh/mies"]
                })
            else:
                logger.warning("Nie znaleziono cen Max w PDF, używam domyślnych")
                greenway_data["subscriptions"].append({
                    "id": "greenway_max",
                    "name": "Energia Max",
                    "monthlyCost": 79.99,
                    "prices": {"ac": 1.60, "dc": 2.10, "hpc": 2.10},
                    "benefits": ["Dla wysokiego zużycia >200 kWh/mies"]
                })
            
            logger.info(f"GreenWay: znaleziono {len(greenway_data['subscriptions'])} plany")
            return greenway_data
            
        except Exception as e:
            logger.error(f"Błąd przy scrapowaniu GreenWay: {e}")
            # Zwracamy domyślne dane w razie błędu
            return self.get_default_greenway_data()
    
    def scrape_orlen(self) -> Dict[str, Any]:
        """Scrapuje cennik Orlen Charge ze strony WWW"""
        logger.info("Rozpoczynam scrapowanie Orlen Charge...")

        try:
            orlen_data = {
                "name": "Orlen Charge",
                "color": "#ef4444",
                "subscriptions": [],
                "promotions": []
            }

            # Scrapowanie cennika standardowego
            standard_url = "https://orlencharge.pl/cennik/"
            response = requests.get(standard_url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Szukamy tabeli z cennikiem
            standard_prices = {}
            promo_prices = {}
            
            # Różne selektory do wypróbowania
            table_selectors = [
                'table',
                '.pricing-table',
                'table.cennik',
                '[class*="price"]',
                '[class*="cennik"]'
            ]
            
            table_found = False
            for selector in table_selectors:
                tables = soup.select(selector)
                if tables:
                    for table in tables:
                        rows = table.find_all('tr')
                        for row in rows:
                            cells = row.find_all(['td', 'th'])
                            if len(cells) >= 2:
                                text = ' '.join([cell.get_text().strip() for cell in cells])
                                
                                # Parsowanie cen - standardowe i promocyjne
                                if 'AC' in text and 'PLN' in text:
                                    # Szukamy wszystkich cen w wierszu (może być standard i promo)
                                    price_matches = re.findall(r'(\d+[,\.]\d+)', text)
                                    if len(price_matches) >= 1:
                                        standard_prices['ac'] = float(price_matches[0].replace(',', '.'))
                                        table_found = True
                                    if len(price_matches) >= 2:
                                        promo_prices['ac'] = float(price_matches[1].replace(',', '.'))

                                elif 'DC' in text and ('50' in text or 'do 50' in text) and 'PLN' in text:
                                    price_matches = re.findall(r'(\d+[,\.]\d+)', text)
                                    if len(price_matches) >= 1:
                                        standard_prices['dc'] = float(price_matches[0].replace(',', '.'))
                                        table_found = True
                                    if len(price_matches) >= 2:
                                        promo_prices['dc'] = float(price_matches[1].replace(',', '.'))

                                elif 'DC' in text and ('125' in text or 'powyżej' in text or '>' in text) and 'PLN' in text:
                                    price_matches = re.findall(r'(\d+[,\.]\d+)', text)
                                    if len(price_matches) >= 1:
                                        standard_prices['hpc'] = float(price_matches[0].replace(',', '.'))
                                        table_found = True
                                    if len(price_matches) >= 2:
                                        promo_prices['hpc'] = float(price_matches[1].replace(',', '.'))
                
                if table_found:
                    break
            
            # Jeśli nie znaleziono w tabeli, szukaj w tekście
            if not table_found:
                body_text = soup.get_text()

                # Wzorce dla różnych typów ładowania
                ac_pattern = r"AC.*?(\d+[,\.]\d+)\s*(?:PLN|zł)/kWh"
                dc_pattern = r"DC.*?≤\s*50.*?(\d+[,\.]\d+)\s*(?:PLN|zł)/kWh"
                hpc_pattern = r"DC.*?>\s*125.*?(\d+[,\.]\d+)\s*(?:PLN|zł)/kWh"

                ac_match = re.search(ac_pattern, body_text, re.IGNORECASE)
                dc_match = re.search(dc_pattern, body_text, re.IGNORECASE)
                hpc_match = re.search(hpc_pattern, body_text, re.IGNORECASE)

                if ac_match:
                    standard_prices['ac'] = float(ac_match.group(1).replace(',', '.'))
                if dc_match:
                    standard_prices['dc'] = float(dc_match.group(1).replace(',', '.'))
                if hpc_match:
                    standard_prices['hpc'] = float(hpc_match.group(1).replace(',', '.'))

            # Jeśli nadal brak cen standardowych, użyj domyślnych
            if not standard_prices:
                logger.warning("Nie znaleziono cen Orlen na stronie, używam domyślnych")
                standard_prices = {"ac": 1.95, "dc": 2.89, "hpc": 3.19}

            # Dodaj cennik standardowy (tylko jeden)
            orlen_data["subscriptions"].append({
                "id": "orlen_standard",
                "name": "Bez abonamentu",
                "monthlyCost": 0,
                "prices": standard_prices,
                "benefits": []
            })

            # Jeśli znaleziono ceny promocyjne, dodaj jako promocję CZASOWĄ
            if promo_prices and len(promo_prices) >= 3:
                # Szukaj dat promocji na stronie
                try:
                    body_text = soup.get_text()
                    # Wzorzec: "od 2.10 do 3.11 2025" lub podobne
                    date_pattern = r'(\d{1,2})\.(\d{1,2}).*?(\d{1,2})\.(\d{1,2})\s*(\d{4})'
                    date_match = re.search(date_pattern, body_text)

                    if date_match:
                        start_day, start_month, end_day, end_month, year = date_match.groups()

                        orlen_data["promotions"].append({
                            "name": "Promocja cenowa",
                            "validFrom": f"{year}-{start_month.zfill(2)}-{start_day.zfill(2)}",
                            "validTo": f"{year}-{end_month.zfill(2)}-{end_day.zfill(2)}",
                            "prices": promo_prices,
                            "conditions": ["Obowiązuje dla wszystkich użytkowników"]
                        })
                        logger.info(f"Znaleziono promocję Orlen od {start_day}.{start_month} do {end_day}.{end_month}.{year}")
                    else:
                        logger.warning("Znaleziono ceny promocyjne, ale nie wykryto dat")
                except Exception as e:
                    logger.warning(f"Błąd przy parsowaniu dat promocji: {e}")
            
            # Sprawdzanie promocji
            promo_urls = [
                "https://orlencharge.pl/cennik-promo/",
                "https://orlencharge.pl/promocje/",
                "https://orlencharge.pl/aktualnosci/"
            ]
            
            for promo_url in promo_urls:
                try:
                    promo_response = requests.get(promo_url, timeout=30)
                    if promo_response.status_code == 200:
                        promo_soup = BeautifulSoup(promo_response.content, 'html.parser')
                        promo_text = promo_soup.get_text()
                        
                        # Szukamy informacji o promocji
                        promo_patterns = [
                            r"promocja.*?(\d+)\s*%",
                            r"taniej.*?(\d+)\s*%",
                            r"-(\d+)\s*%",
                            r"rabat.*?(\d+)\s*%"
                        ]
                        
                        for pattern in promo_patterns:
                            match = re.search(pattern, promo_text, re.IGNORECASE)
                            if match:
                                discount = int(match.group(1))
                                
                                # Szukamy dat
                                date_pattern = r"(\d{1,2})[.\-/](\d{1,2})[.\-/](\d{4})"
                                dates = re.findall(date_pattern, promo_text)
                                
                                if dates and len(dates) >= 2:
                                    start_date = f"{dates[0][2]}-{dates[0][1]:0>2}-{dates[0][0]:0>2}"
                                    end_date = f"{dates[1][2]}-{dates[1][1]:0>2}-{dates[1][0]:0>2}"
                                    
                                    # Oblicz ceny promocyjne
                                    promo_prices = {}
                                    for key, value in prices.items():
                                        promo_prices[key] = round(value * (1 - discount/100), 2)
                                    
                                    orlen_data["promotions"].append({
                                        "name": f"Promocja -{discount}%",
                                        "validFrom": start_date,
                                        "validTo": end_date,
                                        "prices": promo_prices,
                                        "conditions": ["Dla wszystkich użytkowników aplikacji"]
                                    })
                                    
                                    logger.info(f"Znaleziono promocję Orlen: -{discount}%")
                                    break
                        
                        if orlen_data["promotions"]:
                            break
                            
                except Exception as e:
                    logger.warning(f"Nie można sprawdzić promocji Orlen z {promo_url}: {e}")
            
            logger.info(f"Orlen: znaleziono cennik {'z promocją' if orlen_data['promotions'] else 'bez promocji'}")
            return orlen_data
            
        except Exception as e:
            logger.error(f"Błąd przy scrapowaniu Orlen: {e}")
            return self.get_default_orlen_data()
    
    def get_default_greenway_data(self) -> Dict[str, Any]:
        """Zwraca domyślne dane GreenWay"""
        return {
            "name": "GreenWay",
            "color": "#10b981",
            "subscriptions": [
                {
                    "id": "greenway_standard",
                    "name": "Energia Standard",
                    "monthlyCost": 0,
                    "prices": {"ac": 1.95, "dc": 3.15, "hpc": 3.15},
                    "benefits": []
                },
                {
                    "id": "greenway_plus",
                    "name": "Energia Plus",
                    "monthlyCost": 29.99,
                    "prices": {"ac": 1.75, "dc": 2.40, "hpc": 2.40},
                    "benefits": ["Dla średniego zużycia 50-200 kWh/mies"]
                },
                {
                    "id": "greenway_max",
                    "name": "Energia Max",
                    "monthlyCost": 79.99,
                    "prices": {"ac": 1.60, "dc": 2.10, "hpc": 2.10},
                    "benefits": ["Dla wysokiego zużycia >200 kWh/mies"]
                }
            ],
            "promotions": []
        }
    
    def get_default_orlen_data(self) -> Dict[str, Any]:
        """Zwraca domyślne dane Orlen

        UWAGA: Promocje Orlen są ładowane przez JavaScript i nie da się ich scrapować.
        Aktualizuj ręcznie daty i ceny promocji gdy Orlen zmieni ofertę.
        Sprawdź: https://orlencharge.pl/cennik/ (kliknij "Sprawdź cenę")
        """
        return {
            "name": "Orlen Charge",
            "color": "#ef4444",
            "subscriptions": [
                {
                    "id": "orlen_standard",
                    "name": "Bez abonamentu",
                    "monthlyCost": 0,
                    "prices": {"ac": 1.95, "dc": 2.89, "hpc": 3.19},
                    "benefits": []
                }
            ],
            "promotions": [
                {
                    "name": "Promocja cenowa -25%",
                    "validFrom": "2025-02-10",
                    "validTo": "2025-11-03",
                    "prices": {"ac": 1.46, "dc": 2.02, "hpc": 2.39},
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