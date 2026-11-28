import json
from pathlib import Path

import requests

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
}


def get_response(url: str):
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    return response

def parse_onliner_ram():
    results = []
    url = "https://catalog.onliner.by/sdapi/catalog.api/search/dram?group=0&group_limit=0&order=price:asc&limit=30&dramkit[0]=ddr4dimm&dramkit[1]=regddr4dimm&dramkit[2]=ddr4sodreg&dramkit[3]=ddr4sodimm&dramkit[operation]=union&volume_dram[from]=16gb"
    data = get_response(url).json()
    pages_count = data["page"]["last"]

    for product in data["products"]:
        result = {}

        result["title"] = product["full_name"]

        amount = product["description_list"][0]
        if "ГБ" not in amount:
            for item in product["description_list"]:
                if "ГБ" in item:
                    amount = item
                    break

        amount = int(amount.replace (" ГБ", ""))
        result["amount"] = amount
        price = float(product["prices"]["price_min"]["amount"])
        result["price"] = price
        result["url"] = product["html_url"]
        
        result["price_per_gb"] = price / amount

        results.append(result)

    for i in range(2, pages_count + 1):
        url = f"https://catalog.onliner.by/sdapi/catalog.api/search/dram?group=0&group_limit=0&order=price:asc&limit=30&dramkit[0]=ddr4dimm&dramkit[1]=regddr4dimm&dramkit[2]=ddr4sodreg&dramkit[3]=ddr4sodimm&dramkit[operation]=union&volume_dram[from]=16gb&page={i}"
        data = get_response(url).json()

        for product in data["products"]:
            result = {}

            result["title"] = product["full_name"]

            amount = product["description_list"][0]
            if "ГБ" not in amount:
                for item in product["description_list"]:
                    if "ГБ" in item:
                        amount = item
                        break

            amount = int(amount.replace (" ГБ", ""))
            result["amount"] = amount
            price = float(product["prices"]["price_min"]["amount"])
            result["price"] = price
            result["url"] = product["html_url"]
            
            result["price_per_gb"] = price / amount

            results.append(result)
    
    return results


if __name__ == "__main__":
    result_amount = int(input("Сколько результатов вывести? "))
    print("Поиск...")
    results = sorted(parse_onliner_ram(), key = lambda product: product["price_per_gb"])

    print()
    for i in range(0, result_amount):
        result = results[i]

        print(f"№{i + 1}: {result["title"]}\n" + 
        f"Объем: {result["amount"]} ГБ, цена товара: {result["price"]} руб.\n" +
        f"Цена за ГБ: {result["price_per_gb"]:.2f} руб.\n" +
        f"Ссылка: {result["url"]}\n")