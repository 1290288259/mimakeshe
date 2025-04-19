from hmac import new
from flask import request, jsonify
from db_config import db
from models import User , Module, Permission, UserInfo

def login():
   
    # 获取前端发送的JSON数据
    data = request.get_json()
    username = data.get('userName')
    password = data.get('userPassword')
    
    # 查询用户
    user = User.query.filter_by(user_name=username).first()
    
    
    # 验证用户和密码
    if user and user.user_password == password:
        # 登录成功，查询权限
        pid = Permission.query.filter_by(user_id=user.user_id).first().permission_id
        modules = Module.query.filter_by(permission_id=pid).all()
        
        # 将Module对象转换为字典
        module_list = [{
            'module_id': module.module_id,
            'permission_id': module.permission_id,
            'moduleDescription': module.module_description, 
            'moduleRouter': module.module_router  
        } for module in modules]
        user_info = UserInfo.query.filter_by(user_id=user.user_id).first()
        return jsonify({
            'code': 200,
            'msg': '登录成功',
            'data': {
                'user': {
                    'user_id': user.user_id,
                    'user_name': user.user_name,
                    'name': user_info.name,
                    'user_password': user.user_password,
                    'permission_id': pid,
                    'user_address': user_info.user_address,
                    'user_phone': user_info.user_phone
                },
                'moduleList': module_list  # 使用转换后的字典列表
            }
        })
    else:
        return jsonify({
            'code': 401,
            'msg': '用户名或密码错误'
        })

def register():
    # 获取前端发送的注册数据
    data = request.get_json()

    # 检查用户名是否已存在
    if User.query.filter_by(user_name=data['userName']).first():
        return jsonify({
            'code': 400,
            'msg': '用户名已存在'
        })

    # 创建新用户
    new_user = User(
        user_name=data['userName'],
        user_password=data['userPassword']
    )

    # 保存到数据库
    db.session.add(new_user)
    db.session.commit()

    # 查询刚插入的用户ID
    user = User.query.filter_by(user_name=data['userName']).first()

    # 创建用户信息
    new_user_info = UserInfo(
        user_id=user.user_id,
        name=data.get('name', ''),
        user_address=data.get('userAddress', ''),
        user_phone=data.get('userPhone', '')
    )

    # 保存用户信息
    db.session.add(new_user_info)
    db.session.commit()
    
    pid = 2
    new_Permission = Permission(
        permission_id=pid,
        user_id=user.user_id
    )
    
    db.session.add(new_Permission)
    db.session.commit()

    return jsonify({
        'code': 200,
        'msg': '注册成功'
    })