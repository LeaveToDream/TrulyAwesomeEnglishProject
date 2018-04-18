from flask import *
from flask_restful import Resource, Api
import model

app = Flask(__name__)
api = Api(app)

class DecksAPI(Resource):

    def get(self):

        result = []
        
        for document in model.Deck.find():
            result.append(document.dump())

        return jsonify(result)

api.add_resource(DecksAPI, '/api/decks')

if __name__ == '__main__':
    app.run(debug=True)
