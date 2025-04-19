from flask import Flask, request, jsonify
from flask_cors import CORS
from db_config import db, init_db
from models import User
from api.login import login, register
from api.User import update_user
from api.User import get_all_users
from api.User import get_user_by_id
from api.User import delete_user
from api.User import add_user

app = Flask(__name__)
CORS(app)


# 初始化数据库
init_db(app)
app.route('/user/login', methods=['POST'])(login)
app.route('/user/register', methods=['POST'])(register)
app.route('/user/update', methods=['POST'])(update_user)
app.route('/user/getall', methods=['GET'])(get_all_users)
app.route('/user/getuserbyid', methods=['GET'])(get_user_by_id)
app.route('/user/delete', methods=['GET'])(delete_user)
app.route('/user/add', methods=['POST'])(add_user)


if __name__ == '__main__':
    app.run()
