***************
Modèles en JSON
***************

Structure d'une Carte
=====================

.. code:: json

    {
        "name": String,
        "desc": String,
        "img" : URL (optionnel), 
        "year": Integer
    }

Structure d'un Deck
===================

.. code:: json

    {
        "name": String,
        "cards": [ ID de Carte ] (optionnel)
    }