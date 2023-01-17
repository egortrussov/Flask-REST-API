import random 
import bcrypt
import jwt 
import datetime

from ..config import SECRET_KEY

def generate_id():
    """
    Generates a random id 
    :return: string
    """
    user_id = ''
    length = 20 
    for i in range(length):
        if random.randint(0, 1) == 0:
            user_id += chr(ord('a') + random.randint(0, 25))
        else:
            user_id += str(random.randint(0, 9))
    return user_id

def generate_password_hash(password):
    """
    Generates a hash of the password 
    :return: string
    """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) 
    return hashed.decode('utf-8') 

def check_password_hash(password, hashed):
    """
    Checks is password is equal to the hashed hassword 
    :return: bool
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8')) 

def encode_auth_token(user_id, is_worker):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'user_id': user_id,
            'is_worker': is_worker
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    except Exception as e:
        return e

def decode_token(token):
    """
    Checks if token is valid 
    :return: bool  
    """
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256']) 
        return decoded
    except jwt.ExpiredSignatureError:
        return None