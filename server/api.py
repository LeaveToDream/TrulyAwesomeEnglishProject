from flask import *
from flask_restful import Resource, Api
import model
import security
import marshmallow.exceptions

app = Flask(__name__)
api = Api(app)

class CardsAPI(Resource):

    def get(self):

        result = []
        for card in model.Card.find():
            result.append(card.dump())

        return jsonify(result)

    def post(self):

        if security.can_modify(request.cookies.get("user")):
            try:
                new_card = model.Card(**request.get_json().get("card"))
                new_card.commit()
                return jsonify(new_card.dump())
            except marshmallow.exceptions.ValidationError as e:
                abort(400)
        else:
            abort(403)

class CardAPI(Resource):

    def get(self,id):

        find_id = security.getObjectId(id)
        if find_id:
            result = model.Card.find_one({"_id":find_id})
            if result:
                return jsonify(result.dump())
        
        abort(404)

    def put(self,id):

        if security.can_modify(request.cookies.get("user")):

            find_id = security.getObjectId(id)
            if find_id:
                new_card = request.get_json().get("card")
                if new_card:
                    try:
                        old_card_obj = model.Card.find_one({"_id":find_id})
                        old_card_obj.update(new_card)
                        old_card_obj.commit()
                        return (old_card_obj.dump())
                    except marshmallow.exceptions.ValidationError as e:
                        abort(400)
        else:
            abort(403)
    
    def delete(self,id):

        if security.can_modify(request.cookies.get("user")):
            find_id = security.getObjectId(id)
            if find_id:
                model.Card.find_one({"_id":find_id}).delete()
                return "yay !"
        else:
            abort(403)

class DecksAPI(Resource):

    def get(self):

        result = []
        
        for document in model.Deck.find():
            result.append(document.dump())

        return jsonify(result)

    def post(self):

        if security.can_modify(request.cookies.get("user")):
            try:
                new_deck = model.Deck(**request.get_json().get("deck"))
                new_deck.commit()
                return jsonify(new_deck.dump())
            except marshmallow.exceptions.ValidationError as e:
                abort(400)
        else:
            abort(403)

class DeckAPI(Resource):

    def get(self,id):

        find_id = security.getObjectId(id)
        if find_id:
            result = model.Deck.find_one({"_id":find_id})
            if result:
                raw_deck = result.dump()
                cards = []
                for card_id_raw in raw_deck["cards"]:
                    
                    card_id = security.getObjectId(card_id_raw)
                    
                    if not card_id:
                        print(f"Invalid card id : {card_id_raw} in deck {id}")
                        abort(500)
                    
                    card = model.Deck.find_one({"_id":card_id})
                    
                    if not card:
                        print(f"Couldn't find card with id {card_id_raw} in deck {id}")
                        abort(500)

                    cards.append(card.dump())

                raw_deck["cards"] = cards
                
                return jsonify(raw_deck)
        
        abort(404)

    def put(self,id):

        if security.can_modify(request.cookies.get("user")):

            find_id = security.getObjectId(id)
            if find_id:
                new_deck = request.get_json().get("deck")
                if new_deck:
                    try:
                        old_deck_obj = model.Deck.find_one({"_id":find_id})
                        old_deck_obj.update(new_deck)
                        old_deck_obj.commit()
                        return (old_deck_obj.dump())
                    except marshmallow.exceptions.ValidationError as e:
                        abort(400)
        abort(403)
    
    def delete(self,id):

        if security.can_modify(request.cookies.get("user")):
            find_id = security.getObjectId(id)
            if find_id:
                model.Deck.find_one({"_id":find_id}).delete()
        else:
            abort(403)
            
class LoginAPI(Resource):

    def post(self):

        login_user = {x:request.form.get(x) for x in ["name","password"]}

        if all(login_user.values()):
            
            found_user = model.User.find_one({"name": login_user["name"]})

            if found_user:

                if security.passwords_match(login_user,found_user):
                    
                    response = make_response("yay !")
                    response.set_cookie('user',value=security.cookify(found_user.dump()))
                    return response

        abort(401)

"""
@app.route("/api/login/",methods=["POST"])
def login():

    login_user = {x:request.form.get(x) for x in ["name","password"]}

    if all(login_user.values()):
        
        found_user = model.User.find_one({"name": login_user["name"]})

        if found_user:

            if security.passwords_match(login_user,found_user):
                
                response = make_response("yay !")
                response.set_cookie('user',value=security.cookify(found_user.dump()))
                return response

    abort(401)
"""


api.add_resource(DecksAPI, '/api/decks/')
api.add_resource(DeckAPI , '/api/deck/<string:id>')
api.add_resource(LoginAPI, '/api/login/')
api.add_resource(CardsAPI, '/api/cards/')
api.add_resource(CardAPI , '/api/card/<string:id>')

"""
if __name__ == '__main__':
    os.environ["MONGO_URL"] = "mongodb://admin:admin@ds147469.mlab.com:47469"
    os.environ["JWT_SECRET"] = secrets.token_bytes(40)
    app.run()
"""
