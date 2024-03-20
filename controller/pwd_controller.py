from flask import Blueprint as Controller, request, g
from constants import base_db
from model import PwdModel
from common import Result
from utils import KeyUtil, AesUtil

pwd_controller = Controller("pwd", __name__, url_prefix='/pwd')


@pwd_controller.route("/list", methods=["GET"])
def list():
    email = g.info['email']
    db_pwds = base_db.session.query(PwdModel).filter(
        PwdModel.email == email).order_by(PwdModel.sort.asc()).all()
    return Result.ok(data=[item.json() for item in db_pwds])


@pwd_controller.route("/info/<string:pwd_id>", methods=["GET"])
def info(pwd_id):
    key = g.info["password"]
    padded_key = KeyUtil.pad_key(key)

    pc = AesUtil(padded_key)

    db_pwd = base_db.session.query(PwdModel).filter(
        PwdModel.id == pwd_id).one()

    db_pwd.password = pc.decrypt(db_pwd.password)
    return Result.ok(data=db_pwd.json())


@pwd_controller.route("/", methods=["POST"])
def save():
    # 使用主密码进行加密
    key = g.info["password"]
    padded_key = KeyUtil.pad_key(key)
    email = g.info["email"]

    platform = request.json["platform"]
    account = request.json["account"]
    password = request.json["password"]

    pc = AesUtil(padded_key)
    aes_password = pc.encrypt(password)

    base_db.session.add(
        PwdModel(platform=platform, email=email, account=account, password=aes_password))
    base_db.session.commit()
    return Result.ok()


@pwd_controller.route("/", methods=["PUT"])
def update():
    # 使用主密码进行加密
    key = g.info["password"]
    padded_key = KeyUtil.pad_key(key)
    email = g.info["email"]

    vo = request.json
    password = request.json["password"]
    model = PwdModel.query.filter(PwdModel.id == vo['id']).one()
    for key, value in vo.items():
        setattr(model, key, value)

    # 更新密码
    pc = AesUtil(padded_key)
    aes_password = pc.encrypt(password)
    model.password = aes_password
    model.email = email

    base_db.session.commit()
    return Result.ok()


@pwd_controller.route("/", methods=["DELETE"])
def delete():
    ids = request.json
    users_to_delete = PwdModel.query.filter(PwdModel.id.in_(ids)).all()
    for pwd in users_to_delete:
        base_db.session.delete(pwd)
    base_db.session.commit()
    return Result.ok()


@pwd_controller.route("/sort", methods=["POST"])
def sort():
    ids = request.json
    pwds = PwdModel.query.filter(PwdModel.id.in_(ids)).all()
    sort_arr = [i for i in range(len(pwds))]
    new_pwds = [{'id': ids[i], 'sort': sort_arr[i]} for i in range(len(pwds))]
    base_db.session.bulk_update_mappings(PwdModel, new_pwds)
    base_db.session.commit()
    return Result.ok()
