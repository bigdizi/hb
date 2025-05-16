import requests
from bs4 import BeautifulSoup
import json

# Твой HTML с Pastebin — можно заменить на локальный файл, если хочешь
url = "https://pastebin.com/raw/5UWnuVJL"
response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, "html.parser")

events = []

# Каждое событие — строка таблицы <tr>
for tr in soup.find_all("tr"):
    tds = tr.find_all("td")
    if len(tds) < 5:
        continue  # пропускаем неполные строки

    # Время — обычно во втором <td>
    time = tds[1].text.strip()

    # Название и локация — в третьем <td>
    third_td = tds[2]
    title_span = third_td.find("b").find("span")
    title = title_span["title"] if title_span and "title" in title_span.attrs else title_span.text.strip()
    
    # Локация — текст после <br/>
    location_text = ""
    br = third_td.find("br")
    if br and br.next_sibling:
        location_text = br.next_sibling.strip()
        if location_text.lower().startswith("location:"):
            location_text = location_text[len("location:"):].strip()

    # Ссылки на детали и регистрацию
    details_link = None
    register_link = None
    details_a = tds[3].find("a")
    if details_a and "href" in details_a.attrs:
        details_link = details_a["href"]

    register_a = tds[4].find("a")
    if register_a and "href" in register_a.attrs:
        register_link = register_a["href"]

    event = {
        "time": time,
        "title": title,
        "location": location_text,
        "details_url": details_link,
        "register_url": register_link
    }
    events.append(event)

# Сохраняем в файл (можно изменить путь/имя)
with open("2025-04-15.json", "w", encoding="utf-8") as f:
    json.dump(events, f, ensure_ascii=False, indent=4)

print(f"Parsed {len(events)} events. Saved to 2025-04-15.json")
