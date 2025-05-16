import requests
import os
import json
from bs4 import BeautifulSoup

def fetch_day_html(date):
    # Замените на актуальный URL вашей школы с параметром даты
    url = f"https://www.socscms.com/SOCS/CoCurricular/CalendarDay.asp?FType=0&FID=0&Date=04/14/2025={date}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def parse_events_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find_all("tr")
    result = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue
        try:
            time = cols[1].text.strip()
            title_tag = cols[2].find("span", title=True)
            if not title_tag:
                continue
            title = title_tag['title']
            location = cols[2].text.strip().split("Location:")[-1].strip()
            event_link = cols[3].find("a")
            if not event_link:
                continue
            event_id = event_link["href"].split("EventID=")[-1]
            result.append({
                "time": time,
                "title": title,
                "location": location,
                "event_id": event_id
            })
        except Exception:
            continue
    return result

def fetch_event_details(event_id):
    url = f"https://www.socscms.com/SOCS/CoCurricular/EventDetails.asp?EventID=14073409={event_id}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    teacher = "Not found"
    students = "Unknown"

    teacher_tag = soup.find(text="Teacher:")
    if teacher_tag and teacher_tag.find_next():
        teacher = teacher_tag.find_next().text.strip()

    students_tag = soup.find(text="Participants:")
    if students_tag and students_tag.find_next():
        students = students_tag.find_next().text.strip()

    return {
        "teacher": teacher,
        "students": students
    }

def save_day_data(date, data):
    os.makedirs("data", exist_ok=True)
    with open(f"data/{date}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    date = input("Введите дату (например, 2025-04-15): ").strip()
    html = fetch_day_html(date)
    events = parse_events_from_html(html)
    
    for event in events:
        details = fetch_event_details(event["event_id"])
        event.update(details)

    save_day_data(date, events)
    print(f"Данные за {date} сохранены в data/{date}.json")

if __name__ == "__main__":
    main()
