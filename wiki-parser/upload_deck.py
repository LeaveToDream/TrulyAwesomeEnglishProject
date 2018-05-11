import requests
import sys

api_url = "http://omachi.moe:9876/api/"


def upload(nom_deck, cartes):

    with requests.session() as session:

        session.post(api_url + "login/",
                     data={"name": "Syméon", "password": "1234"})

        nouveau_deck = {"deck": {"name": nom_deck}}
        deck_rep = session.post(api_url + "decks/", json=nouveau_deck)

        if not deck_rep.ok:
            print("Impossible de créer le Deck : code "
                  + str(deck_rep.status_code))

        deck_json = deck_rep.json()
        deck_id = deck_json.get("id")

        if not deck_id:
            print("Impossible de récupere l'id du Deck !")
            sys.exit()

        print("Deck créé")

        carte_ids = []

        for i, carte in enumerate(cartes):

            for champ in carte.keys():
                if carte.get(champ) == "":
                    del carte[champ]
                    break

            nouvelle_carte = {"card": carte}
            carte_rep = session.post(api_url + "cards/", json=nouvelle_carte)

            if not carte_rep.ok:
                print("Impossible de creer la carte "
                      + str(carte.get('name'))
                      + " : code " + str(carte_rep.status_code))

            carte_id = carte_rep.json().get("id")
            if carte_id:
                carte_ids.append(carte_id)
            else:
                print(f"Impossible de récuperer l'id pour la carte {carte.get('name')}")

            print(f"\rCarte {i+1}/{len(cartes)}", end="")

        print("\nRemplissage du Deck ...",end="")

        deck_json["cards"] = carte_ids
        del deck_json["id"]

        deck_rep = session.put(api_url + "deck/" +
                               deck_id, json={"deck": deck_json})

        if not deck_rep.ok:
            print("Impossible de rajouter les cartes aux deck : code "
                  + str(deck_rep.status_code))
        print("\rRemplissage du Deck : ok !")

if __name__ == "__main__":

    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("nom_deck", help="nom du deck")
    parser.add_argument(
        "fichier_cartes", help="Le fichier json qui contient les cartes")
    args = parser.parse_args()
    with open(args.fichier_cartes, "r") as f_cartes:
        reponse = upload(args.nom_deck, json.load(f_cartes))
