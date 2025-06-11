import random
from flask import request, jsonify
from db_config import db
from models import Shuju, UserData, Shuju2  # 导入Shuju和UserData模型
from service.Paillier import PaillierEncryptor  # 导入Paillier加密器
from config import FLOAT_PRECISION  # 从config.py导入全局变量

def updata():
    # 接收前端上传的数据
    data = request.get_json()
    print("接收到的数据:", data)

    # 新增：获取 group_id，如果前端没有传递，可以设置一个默认值，例如 1
    group_id = data.get('group_id', 1) # 从请求数据中获取 group_id，默认为 1
    try:
        group_id = int(group_id) # 尝试将 group_id 转换为整数
        if group_id <= 0: # 确保 group_id 是正整数
            return jsonify({'code': 400, 'msg': 'group_id 必须是正整数'}), 400
    except ValueError:
        return jsonify({'code': 400, 'msg': 'group_id 必须是整数'}), 400

    # 将数据转换为浮点型，同时处理 user_id 和 group_id
    float_data = {key: float(value) if key not in ['user_id', 'group_id'] else value for key, value in data.items()}
    print("转换后的数据:", float_data)

    # 定义数据范围
    ranges = {
        'cirrhosis': (0, 100),
        'age': (0, 120),
        'sex': (1, 2),
        'cholesterol': (0, 300),
        'triglyceride': (0, 500),
        'HDL': (0, 100),
        'LDL': (0, 200),
        'PathDiagNum': (0, 1),
        'BMI': (10, 50),
        'ALT': (0, 1000),
        'AST': (0, 1000),
        'glucose': (0, 300)
    }

    # 检查数据是否为空且符合范围
    for key, value in data.items():
        if key in ['user_id', 'group_id']:  # 跳过user_id和group_id的范围检查
            continue
        if key not in ranges:
            return jsonify({
                'code': 400,
                'msg': f'无效字段: {key}'
            })
        try:
            float_value = float(value)  # 将数据转换为浮点型
        except (ValueError, TypeError):
            return jsonify({
                'code': 400,
                'msg': f'{key}必须为数字'
            })
        if not (ranges[key][0] <= float_value <= ranges[key][1]):
            return jsonify({
                'code': 400,
                'msg': f'{key}超出范围: {ranges[key][0]} - {ranges[key][1]}'
            })

    # 生成随机11位ID
    data_id = ''.join([str(random.randint(0, 9)) for _ in range(11)])

    # 将数据存入shuju表
    try:
        new_record = Shuju(
            id=data_id,  # 存入随机ID
            cirrhosis=data['cirrhosis'],
            age=data['age'],
            sex=data['sex'],
            cholesterol=data['cholesterol'],
            triglyceride=data['triglyceride'],
            HDL=data['HDL'],
            LDL=data['LDL'],
            PathDiagNum=data['PathDiagNum'],
            BMI=data['BMI'],
            ALT=data['ALT'],
            AST=data['AST'],
            glucose=data['glucose'],
            group_id=group_id  # 新增：存入 group_id
        )
        db.session.add(new_record)

        # 将user_id和data_id存入user_data表
        user_data_record = UserData(
            user_id=data['user_id'],
            data_id=data_id,
        )
        db.session.add(user_data_record)

        # db.session.commit() # 暂时注释掉，等待shuju2也成功后再一起提交
        # print("数据成功存入shuju表和user_data表")
        

        # 根据 group_id 初始化Paillier加密器以加载对应的密钥
        encryptor = PaillierEncryptor()  # 创建 PaillierEncryptor 实例，此时会默认加载密钥对1
        encryptor.load_or_generate_keypair(index=group_id) # 根据 group_id 加载指定的密钥对
        
        encrypted_data = {  # 加密所有数据字段
            'cirrhosis': str(encryptor.encrypt(int(float_data['cirrhosis'])).ciphertext()),  # 加密肝硬化数据
            'age': str(encryptor.encrypt(int(float_data['age'])).ciphertext()),  # 加密年龄数据
            'sex': str(encryptor.encrypt(int(float_data['sex'])).ciphertext()),  # 加密性别数据
            'cholesterol': str(encryptor.encrypt(int(float_data['cholesterol'])).ciphertext()),  # 加密胆固醇数据
            'triglyceride': str(encryptor.encrypt(int(float_data['triglyceride'])).ciphertext()),  # 加密甘油三酯数据
            'HDL': str(encryptor.encrypt(int(float_data['HDL'])).ciphertext()),  # 加密高密度脂蛋白数据
            'LDL': str(encryptor.encrypt(int(float_data['LDL'] * FLOAT_PRECISION)).ciphertext()),  # 加密低密度脂蛋白数据，乘以浮点精度
            'PathDiagNum': str(encryptor.encrypt(int(float_data['PathDiagNum'])).ciphertext()),  # 加密病理诊断编号数据
            'BMI': str(encryptor.encrypt(int(float_data['BMI'] * FLOAT_PRECISION)).ciphertext()),  # 加密BMI数据，乘以浮点精度
            'ALT': str(encryptor.encrypt(int(float_data['ALT'])).ciphertext()),  # 加密谷丙转氨酶数据
            'AST': str(encryptor.encrypt(int(float_data['AST'])).ciphertext()),  # 加密谷草转氨酶数据
            'glucose': str(encryptor.encrypt(int(float_data['glucose'])).ciphertext())  # 加密血糖数据
        }
        new_encrypted_record = Shuju2(  # 创建加密数据记录
            id=data_id,  # 存入随机ID
            cirrhosis=encrypted_data['cirrhosis'],  # 存入加密的肝硬化数据
            age=encrypted_data['age'],  # 存入加密的年龄数据
            sex=encrypted_data['sex'],  # 存入加密的性别数据
            cholesterol=encrypted_data['cholesterol'],  # 存入加密的胆固醇数据
            triglyceride=encrypted_data['triglyceride'],  # 存入加密的甘油三酯数据
            HDL=encrypted_data['HDL'],  # 存入加密的高密度脂蛋白数据
            LDL=encrypted_data['LDL'],  # 存入加密的低密度脂蛋白数据
            PathDiagNum=encrypted_data['PathDiagNum'],  # 存入加密的病理诊断编号数据
            BMI=encrypted_data['BMI'],  # 存入加密的BMI数据
            ALT=encrypted_data['ALT'],  # 存入加密的谷丙转氨酶数据
            AST=encrypted_data['AST'],  # 存入加密的谷草转氨酶数据
            glucose=encrypted_data['glucose'],  # 存入加密的血糖数据
            group_id=group_id  # 新增：存入 group_id
        )
        db.session.add(new_encrypted_record)  # 将加密数据记录添加到数据库会话
        
        db.session.commit()  # 统一提交所有更改
        print("数据成功存入shuju, user_data 和 shuju2表")  # 打印成功信息

        
# 解密之前存入的加密数据并返回前端
        decrypted_data = {
            'cirrhosis': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_data['cirrhosis']))),
            'age': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_data['age']))),
            'sex': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_data['sex']))),
            'cholesterol': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_data['cholesterol']))),
            'triglyceride': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_data['triglyceride']))),
            'HDL': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_data['HDL']))),
            'LDL': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_data['LDL']))) / FLOAT_PRECISION,
            'PathDiagNum': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_data['PathDiagNum']))),
            'BMI': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_data['BMI']))) / FLOAT_PRECISION,
            'ALT': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_data['ALT']))),
            'AST': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_data['AST']))),
            'glucose': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_data['glucose'])))
        }
        print("解密后的数据:", decrypted_data)

        # 返回成功响应和解密后的数据
        return jsonify({
            'code': 200,
            'msg': '数据接收并存入成功',
            'data': decrypted_data
        })
    except Exception as e:
        db.session.rollback()
        print("数据存入失败:", str(e))
        return jsonify({
            'code': 500,
            'msg': '数据存入失败'
        })

