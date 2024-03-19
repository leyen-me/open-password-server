import os
import bcrypt
from flask import Flask, request, g
from flask_cors import CORS
import jwt
from controller import user_controller, pwd_controller
from constants import base_db, static_folder, routing_white_list, jwt_salt, jwt_headers
from common import Result
from utils import PathUtil
from model import UserModel

app = Flask(__name__)

# cmd
# set EMAIL=xxx@xx.com PASSWORD=xxx

base_mysql_host = os.environ.get("MYSQL_HOST") or "127.0.0.1"
base_mysql_port = os.environ.get("MYSQL_PORT") or "3306"
base_mysql_name = os.environ.get("MYSQL_NAME") or "open-password-mysql"
base_mysql_user = os.environ.get("MYSQL_USER") or "root"
base_mysql_password = os.environ.get("MYSQL_PASSWORD") or "pdBGKGjRyX3Jb2Hn"

base_email = os.environ.get("EMAIL")
base_password = os.environ.get("PASSWORD")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{base_mysql_user}:{base_mysql_password}@{base_mysql_host}:{base_mysql_port}/{base_mysql_name}?charset=utf8"
app.config['SQLALCHEMY_ECHO'] = True
app.static_folder = static_folder

base_db.init_app(app)

with app.app_context():
    base_db.create_all()
    if not base_email:
        raise Exception("必须设置邮箱")

    if not base_password:
        raise Exception("必须设置密码")

    db_user = base_db.session.query(UserModel).filter(
        UserModel.email == base_email).one_or_none()
    if not db_user:
        salt = bcrypt.gensalt()
        new_password = bcrypt.hashpw(password=(base_password).encode(
            'utf-8'), salt=salt).decode("utf-8")
        base_db.session.add(
            UserModel(email=base_email, master_password=new_password))
        base_db.session.commit()

CORS(app, supports_credentials=True, resources=r"/*")


# 请求前置拦截器
@app.before_request
def before():
    # 跳过OPTIONS请求
    if request.method == 'OPTIONS':
        return
    if PathUtil.is_path_allowed(request.path, routing_white_list):
        return
    # 检查Authorization
    authorization = request.headers.get("Authorization")
    if authorization is None:
        raise Exception("用户未登录")
    else:
        # 校验JWT
        try:
            info = jwt.decode(authorization, jwt_salt, verify=True,
                              algorithms=jwt_headers["alg"])
        except Exception as e:
            raise Exception("登录已失效")
        # 校验数据库
        g.info = {
            "email": info["email"],
            "password": info["password"],
        }


# 请求错误拦截器
@app.errorhandler(Exception)
def exception(error_msg):
    return Result.error(str(error_msg))


app.register_blueprint(user_controller)
app.register_blueprint(pwd_controller)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
