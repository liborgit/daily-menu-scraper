import requests
from bs4 import BeautifulSoup
import json
import re
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)

URL = "https://#/"  # URL placeholder
OUTPUT_PATH = "menu.json"
TARGET_STRING = "###"  # Target string placeholder

def remove_extra_spaces(text: str) -> str:
    return " ".join(text.split())

def extract_menu_data(soup: BeautifulSoup) -> List[Dict[str, str]]:
    menu_items = soup.find_all("font", class_="wsw-02") # The class "wsw-02" is used
    menu_data = []
    current_dish = ""
    current_price = ""

    for item in menu_items:
        menu_text = item.get_text(strip=True)

        if not re.match(r"^\d+\.", menu_text):
            continue

        match = re.search(r"(\d+),\-?$", menu_text)
        if match:
            current_price = match.group(1)  # Extract the price as a string
            name = menu_text.replace(match.group(0), "").strip()
            full_dish = remove_extra_spaces(current_dish + " " + name)
            menu_data.append({"Dish": full_dish, "Price": current_price})
            current_dish = ""
        else:
            current_dish = current_dish + " " + menu_text if current_dish else menu_text

    return menu_data

def fetch_page_content(url: str) -> BeautifulSoup:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, "html.parser")
    except requests.RequestException as e:
        logging.error("Failed to fetch page content: %s", e)
        raise

def save_to_json(data: List[Dict[str, str]], filepath: str) -> None:
    try:
        with open(filepath, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        logging.info("Menu data saved to %s", filepath)
    except IOError as e:
        logging.error("Failed to save data to JSON: %s", e)

def clean_json_file(filepath: str, target_string: str) -> None:
    try:
        with open(filepath, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        for item in data:
            if target_string in item.get("Dish", ""):
                item["Dish"] = item["Dish"].replace(target_string, "").strip()

        with open(filepath, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        logging.info("Updated entries containing '%s' in %s", target_string, filepath)
    except (IOError, json.JSONDecodeError) as e:
        logging.error("Failed to clean JSON file: %s", e)

def main():
    soup = fetch_page_content(URL)
    menu_data = extract_menu_data(soup)
    save_to_json(menu_data, OUTPUT_PATH)
    clean_json_file(OUTPUT_PATH, TARGET_STRING)
    logging.info("Final menu data saved and cleaned.")

if __name__ == "__main__":
    main()
