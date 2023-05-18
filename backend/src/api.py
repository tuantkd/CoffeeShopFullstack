from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS
import ssl
from .database.models import setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)
ssl._create_default_https_context = ssl._create_stdlib_context

# ROUTES
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'Result': 'Coffee Shop Fullstack Api',
    })


@app.route('/drinks', methods=['GET'])
def get_drinks():
    cafe_list_drink = Drink.query.all()

    if (len(cafe_list_drink) == 0):
        abort(404)
    cafe_list_drink = [i.short() for i in cafe_list_drink]

    return jsonify({
        'success': True,
        'drinks': cafe_list_drink
    })


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drink_detail(token):
    cafe_list_drink = Drink.query.all()
    if cafe_list_drink:
        cafe_list_drink = [i.long() for i in cafe_list_drink]
        return jsonify({
            'success': True,
            'drinks': cafe_list_drink
        })


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drinks(token):
    body = request.get_json()
    cafe_title = body.get('title', None)
    cafe_recipe = body.get('recipe', None)
    if isinstance(cafe_recipe, dict):
        cafe_recipe = [cafe_recipe]
    cafe_recipe = json.dumps(cafe_recipe)
    try:
        drink = Drink(title=cafe_title, recipe=cafe_recipe)
        drink.insert()

        return jsonify({
            'success': True,
            'drinks': drink.long()
        })

    except Exception:
        abort(422)


@app.route('/drinks/<int:drinkId>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink_by_id(token, drinkId):
    body = request.get_json()
    try:
        modify_drink = Drink.query.filter(
            Drink.id == drinkId).one_or_none()

        if (modify_drink is None):
            abort(404)
        cafe_title = body.get('title', None)
        cafe_recipe = body.get('recipe', None)
        if cafe_title:
            modify_drink.title = cafe_title
        if cafe_recipe:
            if isinstance(cafe_recipe, dict):
                cafe_recipe = [cafe_recipe]
            cafe_recipe = json.dumps(cafe_recipe)
            modify_drink.recipe = cafe_recipe

        modify_drink.update()
        return jsonify({
            'success': True,
            'drinks': modify_drink.long()
        })

    except BaseException:
        abort(400)


@app.route('/drinks/<int:drinkId>', methods=['DELETE'])
@requires_auth('delete:drinks')
def del_drink_by_id(token, drinkId):
    drink = Drink.query.filter(Drink.id == drinkId).one_or_none()
    if (drink is None):
        abort(404)

    try:
        drink.delete()
        return jsonify({
            'success': True,
            'delete': drink.id
        })

    except Exception:
        abort(422)


# Error Handling
@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify({
        "error": ex.error,
        "status_code": ex.status_code,
        "message": ex.message
    })
    response.status_code = ex.status_code
    return response


@app.errorhandler(404)
def resource_not_found_error_handler(error):
    return jsonify({
        'success': False,
        'message': 'Auth error'
    }), 401


@app.errorhandler(404)
def resource_not_found_error_handler(error):
    return jsonify({
        'success': False,
        'message': 'resource not found'
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422
