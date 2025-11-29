import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

REQUEST_PATH = os.path.abspath("request.txt")
REQUEST_DIR = os.path.dirname(REQUEST_PATH)


def convert_currency(amount, from_currency, to_currency):
    """Request current conversion rates from er-api. Calculates the conversion
    and stores the results in the text file/"""

    url = f"https://open.er-api.com/v6/latest/{from_currency}"
    data = requests.get(url).json()

    if to_currency not in data["rates"]:
        results = "conversion data not available."
    else:
        rate = data["rates"][to_currency]
        coverted_currency = float(amount) * rate
        results = f"{amount} {from_currency} is {coverted_currency} {to_currency}"
        
        print(results)

    with open(REQUEST_PATH, "w") as request_file:
        request_file.write(str(results))


class Handler(FileSystemEventHandler):
    """Monitores changes does to the directory where the text file is
    located."""

    def on_modified(self, event):
        with open(REQUEST_PATH, "r") as request_file:
            request = request_file.read()

        # check if there is a new conversion request
        if request.startswith("convert:"):
            currency_data = request[len("convert:"):].strip()

            # Unpacks data in the text file
            currency_amount, from_currency, to_currency = currency_data.split(",")

            if os.path.abspath(event.src_path) == os.path.abspath(REQUEST_PATH):
                print(f"{REQUEST_PATH} has been modified")
                convert_currency(currency_amount, from_currency, to_currency)


request_manager = Observer()
request_manager.schedule(Handler(), path=REQUEST_DIR, recursive=False)
request_manager.start()


try:
    while True:
        time.sleep(0.25)
except KeyboardInterrupt:
    request_manager.stop()

request_manager.join()
