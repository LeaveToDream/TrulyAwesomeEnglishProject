************************
Cartes : ``/api/cards/``
************************

GET
===

Renvoie toutes les cartes dans une liste

POST
====


.. warning:: **Necessite une authentification**


Ajoute une nouvelle carte

La nouvelle carte doit être passée en JSON dans le corps de la requête dans un champ ``card``, exemple :

.. code:: json

	{
		"card":{
		    "year": 2018,
		    "desc": "Ceci est une nouvelle carte ajoutée via une requête POST !",
		    "name": "WOW une nouvelle carte !"
		}
	}

Renvoie la carte complétée avec son id en JSON

.. error::

	* ``400`` si la carte est malformée
	* ``403`` si tu n'est pas log