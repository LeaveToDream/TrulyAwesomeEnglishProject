***************************************
Deck unique : ``/api/deck/<string:id>``
***************************************

GET
===

Renvoie le Deck spécifié par l'id **AVEC les cartes complètes** à la place de leurs IDs dans le champ ``cards``

PUT
===

.. warning:: **Necessite une authentification**

Met à jour le Deck défini par l'id. Le nouveau deck doit être passé dans le corps de la requête en JSON dans un champ ``deck``, exemple :

.. code:: json

    {
        "deck" : {
            "cards": [
                "5ad75b374bc0050951c43096",
                "5ad75b374bc0050951c43097"
            ],
            "name": "Le deck de base, modifié avec un PUT"
        }
    }

.. error::

    * ``400`` si le deck est malformé
    * ``403`` si tu n'est pas log