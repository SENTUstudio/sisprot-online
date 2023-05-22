from os import sys, path

sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from datetime import datetime
import requests
from bs4 import BeautifulSoup

from sisprot.models import TasaCambiaria
from sisprot.db import get_db, db_session

API = "https://petroapp-price.petro.gob.ve/price"
PAYLOAD = {"coins": ["PTR"], "fiats": ["USD", "BS"]}


def crear_tasa_cambiaria():
    session = db_session()
    try:
        response = requests.post(API, json=PAYLOAD)
        response.raise_for_status()
        data = response.json()
        with session:
            t_c = TasaCambiaria(
                fecha=datetime.now(),
                tasa=round(data["data"]["PTR"]["BS"] / data["data"]["PTR"]["USD"], 2),
            )
            session.add(t_c)
            session.commit()
    except Exception as ex:
        print(ex)
    session.close()


def crear_tasa_cambiaria_alternative():
    session = db_session()
    try:
        response = requests.get("https://www.bcv.org.ve/", verify=False)
        soup = BeautifulSoup(response.text, "lxml")
        element = soup.select_one(
            "#dolar > div > div > div.col-sm-6.col-xs-6.centrado > strong"
        )
        if element:
            num = float(element.get_text().strip().replace(",", "."))
            with session:
                t_c = TasaCambiaria(
                    fecha=datetime.now(),
                    tasa=num
                )
                session.add(t_c)
                session.commit()
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    crear_tasa_cambiaria_alternative()
