import requests
import sys
from bs4 import BeautifulSoup
from collections import OrderedDict
import json


def wiki_parser(url_page_wiki, fichier):

    page_wiki = requests.get(url_page_wiki)
    soupe_wiki = BeautifulSoup(page_wiki.content, "html.parser")
    contenu_page = soupe_wiki.find_all(id="mw-content-text")

    if not contenu_page:
        print("Impossible de parser la page ! (pas de mw-content-text)")
        sys.exit()

    cartes = []
    for page in contenu_page:
        mw_parser_output_list = page.find_all(class_="mw-parser-output")
        for mw_parser_output in mw_parser_output_list:
            for ul in mw_parser_output.find_all("ul", recursive=False):
                if not ul.attrs:
                    for li in ul.find_all("li", recursive=False):
                        texte_brut = li.get_text()
                        texte_split = texte_brut.split(":")

                        carte = OrderedDict()

                        carte["year"] = texte_split[0]
                        carte["name"] = ""
                        carte["desc"] = "".join(texte_split[1:])
                        carte["img"] = ""
                        cartes.append(carte)

    with open(fichier, "w+") as fichier_json:

        json.dump(cartes, fichier_json, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url de la page wiki à parser")
    parser.add_argument("fichier", help="le nom du fichier de sortie")
    args = parser.parse_args()
    wiki_parser(args.url, args.fichier)
