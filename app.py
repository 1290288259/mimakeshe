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
from api.updata import updata  # 导入updata路由
from api.Data_processing import data_processing, privacy_intersection ,get_data_analysis_result# 导入数据处理接口
from api.ShowData import getdataByuserid, getAllEncryptedData, getEncryptedData, editEncryptedData, deleteEncryptedData
from config import FLOAT_PRECISION  # 从config.py导入全局变量
from api.DataOB import calculate_avg, get_avg ,get_all_age_data ,get_avg_by_age_group# 导入数据处理接口

# 创建Flask应用实例
app = Flask(__name__)
# 启用跨域支持
CORS(app)

# 初始化数据库
init_db(app)

# 注册用户登录路由
app.route('/user/login', methods=['POST'])(login)
# 注册用户注册路由
app.route('/user/register', methods=['POST'])(register)
# 注册用户信息更新路由
app.route('/user/update', methods=['POST'])(update_user)
# 注册获取所有用户信息路由
app.route('/user/getall', methods=['GET'])(get_all_users)
# 注册根据用户ID获取用户信息路由
app.route('/user/getuserbyid', methods=['GET'])(get_user_by_id)
# 注册删除用户路由
app.route('/user/delete', methods=['GET'])(delete_user)
# 注册添加用户路由
app.route('/user/add', methods=['POST'])(add_user)
# 注册数据上传路由
app.route('/updata', methods=['POST'])(updata)
# 注册数据处理路由
app.route('/data_processing', methods=['GET'])(data_processing)
# 注册根据用户ID获取数据路由
app.route('/data/getdataByuserid', methods=['GET'])(getdataByuserid)
# 注册获取所有加密数据路由
app.route('/data/getAllEncryptedData', methods=['GET'])(getAllEncryptedData)
# 注册根据条件获取加密数据路由
app.route('/data/getEncryptedData', methods=['GET'])(getEncryptedData)
# 注册编辑加密数据路由
# 注册编辑加密数据路由
app.route('/data/editEncryptedData', methods=['POST'])(editEncryptedData)
# 注册删除加密数据路由 
app.route('/data/deleteEncryptedData', methods=['GET'])(deleteEncryptedData)
# 注册重新计算所有用户的平均值路由
app.route('/data/calculate_avg', methods=['GET'])(calculate_avg)
# 注册获取所有用户的平均值路由
app.route('/data/get_avg', methods=['GET'])(get_avg)
# 注册获取所有用户的年龄路由
app.route('/data/getallavg', methods=['GET'])(get_all_age_data)
# 注册所有用户年龄段对应字段平均值路由
app.route('/data/get_avg_by_age_group', methods=['GET'])(get_avg_by_age_group)
# 注册隐私求交路由
app.route('/data/privacy_intersection', methods=['GET'])(privacy_intersection)
# 注册获取隐私求交结果路由
app.route('/data/get_data_analysis_result', methods=['GET'])(get_data_analysis_result)

# 启动Flask应用
if __name__ == '__main__':
    app.run()
