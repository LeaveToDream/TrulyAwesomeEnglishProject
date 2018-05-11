import requests
import sys
from bs4 import BeautifulSoup
from collections import OrderedDict
import json

api_url = "http://omachi.moe:9876/api/"
login_data = {"name": "Syméon", "password": "1234"}
session = requests.session()
session.post(api_url + "login/", data=login_data)


url_page_wiki = "https://fr.wikipedia.org/wiki/Chronologie_du_Royaume-Uni"

page_wiki = requests.get(url_page_wiki)
soupe_wiki = BeautifulSoup(page_wiki.content, "html.parser")
contenu_page = soupe_wiki.find_all(id="mw-content-text")

if not contenu_page:
    print("Impossible de parser la page ! (pas de mw-content-text)")
    sys.exit()


uls = []
for page in contenu_page:
    mw_parser_output_list = page.find_all(class_="mw-parser-output")
    for mw_parser_output in mw_parser_output_list:
        for ul in mw_parser_output.find_all("ul", recursive=False):
            if not ul.attrs:
                uls.append(ul)
                """
                for li in ul.find_all("li", recursive=False):
                    carte = OrderedDict()

                    children = li.childGenerator()

                    date = []
                    elt = next(children)
                    while not ":" in elt.string:
                        date.append(elt)
                        elt = next(children)
                    carte["year"] = "".join(date)
                    carte["name"] = ""
                    carte["desc"] = "".join(map(lambda x: x.string, children))
                    carte["img"] = ""
                    cartes.append(carte)
                """

cartes = []
for ul in uls:
    for li in ul.find_all("li", recursive=False):
        texte_brut = li.get_text()
        texte_split = texte_brut.split(":")

        carte = OrderedDict()

        carte["year"] = texte_split[0]
        carte["name"] = ""
        carte["desc"] = "".join(texte_split[1:])
        carte["img"] = ""
        cartes.append(carte)


with open("Chronologie_du_Royaume-Uni.json", "w+") as fichier_json:

    json.dump(cartes, fichier_json, ensure_ascii=False, indent=4)
