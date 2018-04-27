from umongo import Document, Instance, fields
from datetime import datetime
import pymongo
import os
from main import config

mongo_uri = f"mongodb://{config['MONGO']['USER']}:{config['MONGO']['PASSWORD']}@{config['MONGO']['HOSTNAME']}:{config['MONGO']['PORT']}/tawep"

print(f"Attempting to connect to : {mongo_uri}")
db = pymongo.MongoClient(mongo_uri)
instance = Instance(db.tawep)

@instance.register
class Card(Document):

    year = fields.IntegerField(required=True)
    img = fields.UrlField()
    short_desc = fields.StringField(required=True,unique=True)
    long_desc = fields.StringField(required=True)

    class Meta:
        collection = db.tawep.card

@instance.register
class Deck(Document):

    name = fields.StringField(required=True,unique=True)
    cards = fields.ListField(fields.ReferenceField("Card"))

    class Meta:
        collection = db.tawep.deck

@instance.register
class User(Document):

    name = fields.StringField(required=True,unique=True)
    admin = fields.BooleanField(required=True)
    password_hash = fields.StringField(required=True)
    salt = fields.StringField(required=True)

    class Meta:
        collection = db.tawep.user

"""
carte_test = Card()
carte_test.date = datetime.now()
carte_test.short_desc = "La Carte Test"
carte_test.long_desc = "Ceci est la description LONGUUUUUE de la carte, elle apparait je ne sais pas trop où mais bon au moins on pourra peut-être y glisser queles information un peu plus utilises que ce texte que je suis en train de taper juste pour qu'il puisse prétendre à la description 'longue'"

carte_test.commit()

carte1 = Card(date=datetime.now(),short_desc="carte1",long_desc="La carte 1")
carte2 = Card(date=datetime.now(),short_desc="carte2",long_desc="La carte 2")

carte1.commit()
carte2.commit()

deck1 = Deck(name="Le deck de base",cards=[carte1,carte2])
deck1.commit()
"""

"""
goku = User(email='goku@sayen.com', birthday=datetime(1984, 11, 20))
goku.commit()
vegeta = User(email='vegeta@over9000.com', friends=[goku])
vegeta.commit()


vegeta.friends
# <object umongo.data_objects.List([<object umongo.dal.pymongo.PyMongoReference(document=User, pk=ObjectId('5717568613adf27be6363f78'))>])>
vegeta.dump()
# {id': '570ddb311d41c89cabceeddc', 'email': 'vegeta@over9000.com', friends': ['570ddb2a1d41c89cabceeddb']}
User.find_one({"email": 'goku@sayen.com'})
# <object Document __main__.User({'id': ObjectId('570ddb2a1d41c89cabceeddb'), 'friends': <object umongo.data_objects.List([])>,
#                                 'email': 'goku@sayen.com', 'birthday': datetime.datetime(1984, 11, 20, 0, 0)})>
"""