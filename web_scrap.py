import functions as fn


# web scrap music events and send e-mail
web_code = fn.get_html_code(fn.WEB_URL)
extracted_data = fn.extract_data(web_code)
print(extracted_data)
if extracted_data != "No upcoming tours":
    rows = fn.extract_data_db("events")
    extracted_data = fn.parse_music_data(extracted_data)
    if extracted_data not in rows:
        fn.store_data_db(extracted_data)
        fn.send_email(extracted_data)


"""
# web scrap fake temp and save in CSV
web_code = fn.get_html_code("https://programmer100.pythonanywhere.com/")
extracted_data = fn.extract_data(web_code, yaml_file="extract_temp.yaml", search="temp")
new_data = [str(datetime.now().strftime("%y-%m-%d-%H-%M-%S")), extracted_data]
fn.store_data_csv(new_data)
"""
