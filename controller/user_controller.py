from datetime import datetime, timedelta
import bcrypt
from flask import Blueprint as Controller, request, g
import jwt
from constants import base_db
from model import UserModel
from common import Result
from constants import jwt_salt, jwt_headers

user_controller = Controller("user", __name__, url_prefix='/user')

# salt = bcrypt.gensalt()
# new_password = bcrypt.hashpw(password=("482645").encode('utf-8'), salt=salt).decode("utf-8")
# print(new_password)


@user_controller.route("/login", methods=["POST"])
def login():
    email = request.json["email"]
    master_password = request.json["master_password"]
    # 账号是否存在
    db_user = base_db.session.query(UserModel).filter(
        UserModel.email == email).one_or_none()
    if not db_user:
        raise Exception("账号不存在")

    # 验证主密码
    master_password = str(master_password).encode('utf-8')
    db_master_password = str(db_user.master_password).encode('utf-8')
    if not bcrypt.checkpw(master_password, db_master_password):
        raise Exception("主密码错误")

    # 颁发TOKEN
    jwt_exp = datetime.now() + timedelta(hours=2)
    payload = {"exp": jwt_exp, "email": db_user.email,"password": master_password.decode("utf-8")}
    token = jwt.encode(payload=payload, key=jwt_salt,
                       algorithm=jwt_headers["alg"], headers=jwt_headers)
    return Result.ok(data=token)


@user_controller.route("/info", methods=["GET"])
def info():
    return Result.ok(data=g.info)


@user_controller.route("/", methods=["GET"])
def page():
    return Result.ok(data="hello, world")
