from flask import request, jsonify
from db_config import db
from models import User, UserInfo, Permission  # 添加Permission导入

def update_user():
    # 获取前端发送的JSON数据
    data = request.get_json()
    
    # 查询用户
    user = User.query.filter_by(user_id=data['userId']).first()
    user_info = UserInfo.query.filter_by(user_id=data['userId']).first()
    permission = Permission.query.filter_by(user_id=data['userId']).first()  # 查询权限记录
    data['permissionId'] = int(data['permissionId'])
    print(data)
    print(user)
    print(user_info)
    print(permission)
    if not user or not user_info:
        return jsonify({
            'code': 404,
            'msg': '用户不存在'
        })

    try:
        # 更新User表
        if 'userName' in data:
            user.user_name = data['userName']
        if 'userPassword' in data:
            user.user_password = data['userPassword']

        # 更新UserInfo表
        if 'name' in data:
            user_info.name = data['name']
        if 'userAddress' in data:
            user_info.user_address = data['userAddress']
        if 'userPhone' in data:
            user_info.user_phone = data['userPhone']

        # 更新权限表
        if 'permissionId' in data and permission:
            permission.permission_id = int(data['permissionId'])  # 更新权限ID
            db.session.add(permission)  # 显式添加权限记录到会话

        # 提交更改
        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': '更新成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'msg': '更新失败',
            'error': str(e)
        })

def get_all_users():
    try:
        # 查询所有用户
        users = User.query.all()
        user_list = []
        
        for user in users:
            # 查询用户信息
            user_info = UserInfo.query.filter_by(user_id=user.user_id).first()
            # 查询用户权限
            permission = Permission.query.filter_by(user_id=user.user_id).first()
            
            # 构建用户信息字典
            user_dict = {
                'userId': user.user_id,
                'userName': user.user_name,
                'userPassword': user.user_password,
                'permissionId': permission.permission_id if permission else None,
                'name': user_info.name if user_info else '',
                'userAddress': user_info.user_address if user_info else '',
                'userPhone': user_info.user_phone if user_info else ''
            }
            user_list.append(user_dict)
        
        return jsonify({
            'code': 200,
            'msg': '获取成功',
            'data': {
                'userAllList': user_list
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': '获取失败',
            'error': str(e)
        })


def get_user_by_id():
    # 获取请求参数
    user_id = request.args.get('userId')
    
    # 查询用户
    user = User.query.filter_by(user_id=user_id).first()
    user_info = UserInfo.query.filter_by(user_id=user_id).first()
    permission = Permission.query.filter_by(user_id=user_id).first()

    if not user or not user_info:
        return jsonify({
            'code': 404,
            'msg': '用户不存在'
        })

    # 构建用户信息字典
    user_dict = {
        'userId': user.user_id,
        'userName': user.user_name,
        'userPassword': user.user_password,
        'permissionId': permission.permission_id if permission else None,
        'name': user_info.name if user_info else '',
        'userAddress': user_info.user_address if user_info else '',
        'userPhone': user_info.user_phone if user_info else ''
    }

    return jsonify({
        'code': 200,
        'msg': '获取成功',
        'data': {
            'UserAllList': [user_dict]  # 返回一个包含单个用户的列表
        }
    })


def delete_user():
    # 获取请求参数
    user_id = request.args.get('userId')
    
    # 查询用户
    user = User.query.filter_by(user_id=user_id).first()
    user_info = UserInfo.query.filter_by(user_id=user_id).first()
    permission = Permission.query.filter_by(user_id=user_id).first()

    if not user or not user_info:
        return jsonify({
            'code': 404,
            'msg': '用户不存在'
        })

    try:
        # 删除用户信息
        if user_info:
            db.session.delete(user_info)
        if permission:
            db.session.delete(permission)
        if user:
            db.session.delete(user)
        
        # 提交更改
        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': '删除成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'msg': '删除失败',
            'error': str(e)
        })


def add_user():
    # 获取前端发送的JSON数据
    data = request.get_json()
    
    try:
        # 创建User表记录
        user = User(
            user_name=data['userName'],
            user_password=data['userPassword']
        )
        db.session.add(user)
        db.session.flush()  # 获取生成的user_id

        # 创建UserInfo表记录
        user_info = UserInfo(
            user_id=user.user_id,
            name=data['name'],
            user_address=data['userAddress'],
            user_phone=data['userPhone']
        )
        db.session.add(user_info)

        # 创建Permission表记录
        permission = Permission(
            user_id=user.user_id,
            permission_id=int(data['permissionId'])
        )
        db.session.add(permission)

        # 提交更改
        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': '新增成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'msg': '新增失败',
            'error': str(e)
        })