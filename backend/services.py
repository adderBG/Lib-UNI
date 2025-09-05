from flask import request, jsonify
from flask_jwt_extended import create_access_token
from functools import wraps
import requests, os
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity

def token_required(f):
    """Decorator to check if the request has a valid JWT token.

    Args:
        f (object): function to be decorated

    Returns:
        function object: function
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            #app.logger.error(f"JWT verification failed: {e}")
            return jsonify({"error": "Unauthorized", "message": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated


def generate_token(identity):
    return create_access_token(identity=identity)