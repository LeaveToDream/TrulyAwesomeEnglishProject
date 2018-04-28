*****
Login
*****

L'api demande à ce que vous soyez logué pour toute opération autre qu'une observation des données de la base

Le login est possible depuis la route suivante :

``/api/login/``
===============

POST
----

Attend les paramètres ``name`` et ``password`` en ``form-data``

Renvoie un token d'authentification ``user`` et affiche ``yay !`` en cas de succès

.. error::

	``401`` pour toute erreur 