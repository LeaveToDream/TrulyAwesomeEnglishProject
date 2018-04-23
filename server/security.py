import jwt
import os
import hashlib
import secrets
from main import config
import bson.objectid
import bson.errors


def getObjectId(id):

    try:
        return bson.objectid.ObjectId(id)
    except bson.errors.InvalidId as e:
        return None


def cookify(obj,secret=config["JWT_SECRET"]):

    return jwt.encode(obj, secret, algorithm='HS256').decode("utf-8")

def decode(raw_cookie,secret=config["JWT_SECRET"]):

    try:
        return jwt.decode(raw_cookie.encode("utf-8"),secret,algorithm='HS256')
    except jwt.InvalidSignatureError as e:
        return None

def can_modify(raw_user_cookie):

    if raw_user_cookie:
        user = decode(raw_user_cookie)
        if user:
            return user["admin"]

    return False

def passwords_match(given_user,expected_user):

    return valid_password(
        given_user["name"],
        given_user["password"],
        expected_user["password_hash"],
        expected_user["salt"]
        )

def valid_password(name, password, _hash, salt):
    return (_hash, salt) == make_password_hash(name,password,salt)

def make_password_hash(name, password, salt=""):
    salt = salt or secrets.token_hex(8)
    to_be_hashed = name+password+salt
    _hash = hashlib.sha256(to_be_hashed.encode("utf-8")).hexdigest()
    return _hash, salt