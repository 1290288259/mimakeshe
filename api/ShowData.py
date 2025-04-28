from flask import request, jsonify  # 导入Flask的request和jsonify模块
from db_config import db  # 导入数据库配置
from models import UserData, Shuju2  # 导入UserData和Shuju2模型
from service.Paillier import PaillierEncryptor  # 导入Paillier加密器
from config import FLOAT_PRECISION  # 导入全局变量FLOAT_PRECISION

def getdataByuserid():
    user_id = request.args.get('user_id')  # 从请求参数中获取user_id
    if not user_id:  # 如果user_id为空
        return jsonify({'code': 400, 'msg': 'user_id不能为空'})  # 返回错误响应

    try:
        # 查询user_data表，获取所有data_id
        user_data_records = UserData.query.filter_by(user_id=user_id).all()  # 根据user_id查询UserData表
        if not user_data_records:  # 如果未找到相关记录
            return jsonify({'code': 404, 'msg': '未找到相关数据'})  # 返回错误响应

        # 获取所有data_id
        data_ids = [record.data_id for record in user_data_records]  # 提取所有data_id

        # 查询shuju2表，获取所有数据
        shuju2_records = Shuju2.query.filter(Shuju2.id.in_(data_ids)).all()  # 根据data_id查询Shuju2表
        if not shuju2_records:  # 如果未找到相关记录
            return jsonify({'code': 404, 'msg': '未找到相关加密数据'})  # 返回错误响应

        # 解密数据
        encryptor = PaillierEncryptor()  # 创建Paillier加密器实例
        decrypted_data = []  # 初始化解密后的数据列表
        for record in shuju2_records:  # 遍历shuju2表中的每条记录
            decrypted_record = {  # 解密每条记录
                'id': record.id,  # 记录ID
                'cirrhosis': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.cirrhosis))),  # 解密肝硬化数据
                'age': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.age))),  # 解密年龄数据
                'sex': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.sex))),  # 解密性别数据
                'cholesterol': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.cholesterol))),  # 解密胆固醇数据
                'triglyceride': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.triglyceride))),  # 解密甘油三酯数据
                'HDL': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.HDL))),  # 解密高密度脂蛋白数据
                'LDL': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.LDL))) / FLOAT_PRECISION,  # 解密低密度脂蛋白数据
                'PathDiagNum': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.PathDiagNum))),  # 解密病理诊断编号数据
                'BMI': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.BMI))) / FLOAT_PRECISION,  # 解密体重指数数据
                'ALT': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.ALT))),  # 解密谷丙转氨酶数据
                'AST': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.AST))),  # 解密谷草转氨酶数据
                'glucose': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.glucose)))  # 解密血糖数据
            }
            decrypted_data.append(decrypted_record)  # 将解密后的记录添加到列表中

        return jsonify({'code': 200, 'msg': '数据查询成功', 'data': decrypted_data})  # 返回成功响应
    except Exception as e:  # 捕获异常
        return jsonify({'code': 500, 'msg': '数据查询失败: ' + str(e)})  # 返回错误响应


# 获取所有加密数据（带分页）
def getAllEncryptedData():
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)
        
        # 计算偏移量
        offset = (page - 1) * page_size
        
        # 查询总记录数
        total_count = Shuju2.query.count()
        
        # 查询shuju2表，获取分页数据
        shuju2_records = Shuju2.query.limit(page_size).offset(offset).all()
        if not shuju2_records:
            return jsonify({'code': 404, 'msg': '未找到加密数据'})

        # 获取所有数据的用户ID
        data_ids = [record.id for record in shuju2_records]  # 从shuju2记录中提取所有数据ID
        user_data_map = {}  # 初始化一个空字典，用于存储数据ID到用户ID的映射关系
        user_data_records = UserData.query.filter(UserData.data_id.in_(data_ids)).all()  # 查询UserData表，获取所有与data_ids匹配的记录
        
        for record in user_data_records:  # 遍历所有UserData记录
            user_data_map[record.data_id] = record.user_id  # 建立数据ID到用户ID的映射关系，用于后续查找每条数据对应的用户

        # 解密数据
        encryptor = PaillierEncryptor()  # 创建Paillier加密器实例
        decrypted_data = []  # 初始化解密后的数据列表
        
        for record in shuju2_records:
            # 如果在user_data表中找不到对应的记录，则user_id设为1
            user_id = user_data_map.get(record.id, '1')
            
            decrypted_record = {
                'id': record.id,
                'user_id': user_id,
                'cirrhosis': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.cirrhosis))),
                'age': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.age))),
                'sex': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.sex))),
                'cholesterol': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.cholesterol))),
                'triglyceride': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.triglyceride))),
                'HDL': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.HDL))),
                'LDL': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.LDL))) / FLOAT_PRECISION,
                'PathDiagNum': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.PathDiagNum))),
                'BMI': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.BMI))) / FLOAT_PRECISION,
                'ALT': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.ALT))),
                'AST': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.AST))),
                'glucose': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.glucose)))
            }
            decrypted_data.append(decrypted_record)

        return jsonify({
            'code': 200, 
            'msg': '数据查询成功', 
            'data': decrypted_data,
            'total': total_count,
            'page': page,
            'page_size': page_size
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': '数据查询失败: ' + str(e)})

# 根据用户ID和数据ID查询特定数据（带分页）
def getEncryptedData():
    user_id = request.args.get('user_id')
    data_id = request.args.get('data_id')
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    
    if not user_id and not data_id:
        return jsonify({'code': 400, 'msg': '请至少提供一个查询条件'})
    
    try:
        query = db.session.query(Shuju2, UserData.user_id).join(
            UserData, Shuju2.id == UserData.data_id, isouter=True
        )
        
        if user_id:
            query = query.filter(UserData.user_id == user_id)
        if data_id:
            query = query.filter(Shuju2.id == data_id)
        
        # 获取总记录数
        total_count = query.count()
        
        # 计算偏移量
        offset = (page - 1) * page_size
        
        # 获取分页数据
        results = query.limit(page_size).offset(offset).all()
        
        if not results:
            return jsonify({'code': 404, 'msg': '未找到匹配的数据'})
        
        # 解密数据
        encryptor = PaillierEncryptor()  # 创建Paillier加密器实例
        decrypted_data = []  # 初始化解密后的数据列表
            
        for shuju2, user_id_result in results:
            # 如果user_id为None，则设置为1
            user_id_value = user_id_result if user_id_result else '1'
            
            decrypted_record = {
                'id': shuju2.id,
                'user_id': user_id_value,
                'cirrhosis': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.cirrhosis))),
                'age': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.age))),
                'sex': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.sex))),
                'cholesterol': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.cholesterol))),
                'triglyceride': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.triglyceride))),
                'HDL': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.HDL))),
                'LDL': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.LDL))) / FLOAT_PRECISION,
                'PathDiagNum': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.PathDiagNum))),
                'BMI': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.BMI))) / FLOAT_PRECISION,
                'ALT': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.ALT))),
                'AST': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.AST))),
                'glucose': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.glucose)))
            }
            decrypted_data.append(decrypted_record)
            
        return jsonify({
            'code': 200, 
            'msg': '数据查询成功', 
            'data': decrypted_data,
            'total': total_count,
            'page': page,
            'page_size': page_size
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': '数据查询失败: ' + str(e)})


# 编辑数据接口
def editEncryptedData():
    try:
        data = request.get_json()
        data_id = data.get('id')
        if not data_id:
            return jsonify({'code': 400, 'msg': '缺少数据ID'})

        record = Shuju2.query.filter_by(id=data_id).first()
        if not record:
            return jsonify({'code': 404, 'msg': '未找到对应数据'})

        encryptor = PaillierEncryptor()

        # 逐字段加密并更新
        for field in ['cirrhosis', 'age', 'sex', 'cholesterol', 'triglyceride', 'HDL', 'LDL', 'PathDiagNum', 'BMI', 'ALT', 'AST', 'glucose']:
            if field in data:
                value = data[field]
                # BMI和LDL需要乘以FLOAT_PRECISION
                if field in ['BMI', 'LDL']:
                    value = int(float(value) * FLOAT_PRECISION)
                else:
                    value = int(float(value))
                setattr(record, field, str(encryptor.encrypt(value).ciphertext()))

        db.session.commit()
        return jsonify({'code': 200, 'msg': '编辑成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'msg': '编辑失败: ' + str(e)})

# 删除数据接口
def deleteEncryptedData():
    try:
        data_id = request.args.get('id')
        if not data_id:
            return jsonify({'code': 400, 'msg': '缺少数据ID'})

        record = Shuju2.query.filter_by(id=data_id).first()
        if not record:
            return jsonify({'code': 404, 'msg': '未找到对应数据'})

        db.session.delete(record)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'msg': '删除失败: ' + str(e)})