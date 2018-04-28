***********************
Decks : ``/api/decks/``
***********************

GET
===

Renvoie tous les decks dans une liste JSON

.. note:: Ne met **pas** les données des cartes à la place de leur id dans les champs ``cards``

POST
====

.. warning:: **Necessite une authentification**

Ajoute un nouveau deck

Le nouveau deck doit être passé en JSON dans le corps de la requête, dans un champ ``deck``, exemple :

.. code:: json

    {
        "deck" : {
            "name": "WOW, un nouveau Deck !"
        }
    }

.. note::

	Le champ ``cards`` est purement optionnel, pas besoin d'avoir créé les cartes avant de créer le deck

.. error::

    * ``400`` si le deck est malformé
    * ``403`` si tu n'est pas log