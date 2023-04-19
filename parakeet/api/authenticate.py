from datetime import datetime, timedelta

import jwt
from rest_framework.response import Response


# Function for generating JWT token
def generate_jwt_token(user_id, expiration_time_minutes):
    # Define the payload for the JWT token
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=expiration_time_minutes),
    }
    # Generate the JWT token with a secret key
    jwt_token = jwt.encode(payload, "secret_key", algorithm="HS256")
    return jwt_token


# Function for verifying JWT token
def verify_jwt_token(jwt_token):
    try:
        # Decode the JWT token with the secret key
        payload = jwt.decode(jwt_token, "secret_key", algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        # If the token has expired, raise an error
        raise Exception("JWT token has expired")
    except jwt.InvalidTokenError:
        # If the token is invalid, raise an error
        raise Exception("JWT token is invalid")


# Decorator for requiring JWT token authentication
def jwt_authentication_required(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            # Get JWT token from Authorization header
            jwt_token = request.headers["Authorization"].split(" ")[1]
            # Verify JWT token and get payload
            payload = jwt.decode(jwt_token, "secret_key", algorithms=["HS256"])
            # Set user ID in request object for use in view function
            request.user_id = payload["user_id"]
            # Call the view function with authenticated request
            return view_func(request, *args, **kwargs)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, KeyError):
            # If the token is invalid or has expired, return 401 Unauthorized response
            return Response(status=401)

    return wrapper
