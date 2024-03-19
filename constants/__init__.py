from .base_db import base_db as base_db

static_folder = "static"

routing_white_list = ["/user/login"]


jwt_headers = {
    "alg": "HS256",
    "typ": "JWT"
}

jwt_salt = "asgfdgerhersasdq"

aes_iv = jwt_salt
