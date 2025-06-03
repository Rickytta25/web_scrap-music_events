import requests
from selectorlib import Extractor
import smtplib
from os import getenv
import csv
import sqlite3

WEB_URL = r"https://programmer100.pythonanywhere.com/tours/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac 0S X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko)"}
EMAIL_SENDER = "radky.app.test123@gmail.com"
EMAIL_PASSWD = getenv("PASSWORD")
EMAIL_RECEIVER = "radky.app.test123@gmail.com"

connection = sqlite3.connect("event_data.db")
cursor = connection.cursor()


def get_html_code(url) -> str:
    """ Request a source code from the webpage url. """
    web_code = requests.get(url, headers=HEADERS)
    return web_code.text


def extract_data(web_code, yaml_file="extract_data.yaml", search="tours") -> str:
    """ Extract important data from web programmer100.pythonanywhere.com. """
    extractor = Extractor.from_yaml_file(yaml_file)
    data = extractor.extract(web_code)[search]
    return data


def extract_data_db(table):
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    return rows


def send_email(message) -> None:
    """ Send e-mail via SMTP protocol with gmail server. """
    with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465) as server:
        email_message = f"Subject: New music event has appeared!\n\n{message}"
        server.login(EMAIL_SENDER, EMAIL_PASSWD)
        server.sendmail(from_addr=EMAIL_SENDER, to_addrs=EMAIL_RECEIVER, msg=email_message)

    print("E-mail with new music event was sent.")


def store_data(new_data, store_file="music_event_data.txt") -> None:
    """ Store music event data in this format: name of event, place, date."""
    with open(store_file, mode="a", encoding="UTF-8") as file:
        file.write(new_data + "\n")


def store_data_csv(new_data, store_file="fake_temp_data.csv"):
    with open(store_file, "a", newline="") as csv_file:
        data_writer = csv.writer(csv_file, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(new_data)


def store_data_db(new_data):
    cursor.execute("INSERT INTO events VALUES (?, ?, ?)", new_data)
    connection.commit()


def check_duplicity(music_event) -> None:
    """ Prevent saving and send by e-mail one event twice. """
    with open("music_event_data.txt", mode="r", encoding="UTF-8") as file:
        content = file.readlines()
        if music_event + "\n" not in content:
            store_data(music_event)
            send_email(music_event)


def parse_music_data(music_data) -> tuple:
    event = music_data.split(", ")
    event = tuple([item.strip() for item in event])
    return event


def convert_csv_to_db(file_path):
    with open(file_path, "r", newline="") as csv_file:
        data_reader = csv.reader(csv_file, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
        next(data_reader, None)
        for row in data_reader:
            print(tuple(row))
            cursor.execute(f"INSERT INTO temperature VALUES {tuple(row)}")
        connection.commit()
