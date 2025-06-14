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
from api.Data_processing import  privacy_intersection ,get_data_analysis_result# 导入数据处理接口
from api.ShowData import getdataByuserid, getAllEncryptedData, getEncryptedData, editEncryptedData, deleteEncryptedData ,getPlainAverages, select_keypair, get_keypair_names ,generate_new_keypair
from config import FLOAT_PRECISION  # 从config.py导入全局变量
from api.DataOB import calculate_avg, get_avg ,get_all_age_data ,calculate_and_store_age_group_avg, get_age_group_avg_from_db # 导入数据处理接口
from api.test import run_all_tests, run_average_test, run_exact_match_test_api, run_fuzzy_match_test_api

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
# 注册计算所有用户年龄段对应字段平均值路由
app.route('/data/calculate_and_store_age_group_avg', methods=['GET'])(calculate_and_store_age_group_avg)
# 注册获取所有用户年龄段对应字段平均值路由
app.route('/data/get_age_group_avg_from_db', methods=['GET'])(get_age_group_avg_from_db)
# 注册隐私求交路由
app.route('/data/privacy_intersection', methods=['GET'])(privacy_intersection)
# 注册获取隐私求交结果路由
app.route('/data/get_data_analysis_result', methods=['GET'])(get_data_analysis_result)

# 注册获取明文验证平均值结果路由
app.route('/data/get_plain_avg', methods=['GET'])(getPlainAverages)



# 注册测试相关路由
app.route('/api/test/all', methods=['GET'])(run_all_tests)
app.route('/api/test/average', methods=['GET'])(run_average_test)
app.route('/api/test/exact_match', methods=['GET'])(run_exact_match_test_api)
app.route('/api/test/fuzzy_match', methods=['GET'])(run_fuzzy_match_test_api)


# 选择密钥路由
app.route('/select_keypair', methods=['GET'])(select_keypair)

app.route('/get_keypair_names', methods=['GET'])(get_keypair_names)

app.route('/generate_new_keypair', methods=['GET'])(generate_new_keypair)

# 启动Flask应用
if __name__ == '__main__':
    app.run()
