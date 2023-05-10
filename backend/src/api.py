# import os
# from flask import Flask, request, jsonify, abort
# from sqlalchemy import exc
# import json
# from flask_cors import CORS, cross_origin

# from .database.models import db_drop_and_create_all, setup_db, Drink
# from .auth.auth import AuthError, requires_auth

# app = Flask(__name__)
# setup_db(app)
# CORS(app)

# '''
# @TODO uncomment the following line to initialize the datbase
# !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
# !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
# !! Running this funciton will add one
# '''
# # db_drop_and_create_all()

# @app.route('/')
# @cross_origin() 
# def welcome_app(): 
#     return jsonify({'App': 'Trivia API Application'})

# # ROUTES
# '''
# @TODO implement endpoint
#     GET /drinks
#         it should be a public endpoint
#         it should contain only the drink.short() data representation
#     returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
#         or appropriate status code indicating reason for failure
# '''


# '''
# @TODO implement endpoint
#     GET /drinks-detail
#         it should require the 'get:drinks-detail' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
#         or appropriate status code indicating reason for failure
# '''


# '''
# @TODO implement endpoint
#     POST /drinks
#         it should create a new row in the drinks table
#         it should require the 'post:drinks' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
#         or appropriate status code indicating reason for failure
# '''


# '''
# @TODO implement endpoint
#     PATCH /drinks/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should update the corresponding row for <id>
#         it should require the 'patch:drinks' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
#         or appropriate status code indicating reason for failure
# '''


# '''
# @TODO implement endpoint
#     DELETE /drinks/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should delete the corresponding row for <id>
#         it should require the 'delete:drinks' permission
#     returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
#         or appropriate status code indicating reason for failure
# '''


# # Error Handling
# '''
# Example error handling for unprocessable entity
# '''


# @app.errorhandler(422)
# def unprocessable(error):
#     return jsonify({
#         "success": False,
#         "error": 422,
#         "message": "unprocessable"
#     }), 422


# '''
# @TODO implement error handlers using the @app.errorhandler(error) decorator
#     each error handler should return (with approprate messages):
#              jsonify({
#                     "success": False,
#                     "error": 404,
#                     "message": "resource not found"
#                     }), 404

# '''

# '''
# @TODO implement error handler for 404
#     error handler should conform to general task above
# '''


# '''
# @TODO implement error handler for AuthError
#     error handler should conform to general task above
# '''

from flask import Flask, request, abort
import json
from functools import wraps
from jose import jwt
from urllib.request import urlopen


app = Flask(__name__)

AUTH0_DOMAIN = 'coffee-shop.uk.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffeeshop'


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = get_token_auth_header()
        try:
            payload = verify_decode_jwt(token)
        except:
            abort(401)
        return f(payload, *args, **kwargs)

    return wrapper

@app.route('/headers')
@requires_auth
def headers(payload):
    print(payload)
    return 'Access Granted'