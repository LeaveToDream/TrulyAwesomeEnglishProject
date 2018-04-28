****************************************
Carte unique : ``/api/card/<string:id>``
****************************************

GET
===

Renvoie la carte définie par l'id,
Erreur sinon

PUT
===

.. warning:: **Necessite une authentification**

Met à jour la carte définie par l'id.
La nouvelle carte doit être passée en json dans le corps de la requête dans un champ ``card``, exemple :

.. code:: json

	{
		"card":{
		    "year": 2018,
		    "desc": "Ceci est une ancienne carte modifiée via une requête PUT !",
		    "name": "WOW une nouvelle carte !"
		}
	}

Renvoie la carte mise à jour

DELETE
======

.. warning:: **Necessite une authentification**

Supprime la carte définie par l'id,

Renvoie "yay !"

