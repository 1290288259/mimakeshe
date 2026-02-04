from flask import request, jsonify  # 导入Flask的request和jsonify模块
from db_config import db  # 导入数据库配置
from models import UserData, Shuju2  # 导入UserData和Shuju2模型
from service.Paillier import PaillierEncryptor  # 导入Paillier加密器
from config import FLOAT_PRECISION  # 导入全局变量FLOAT_PRECISION
from service.yanzheng import calculate_averages
import os # 导入os模块，用于文件系统操作
import re # 导入re模块，用于正则表达式操作
import json # 导入json模块

# 密钥与医院名称映射文件路径
KEY_MAP_FILE = 'e:\\桌面\\zuoye\\密码学课设\\Medical_data_analysis_system\\service\\key_hospital_map.json'

def load_key_map():
    """加载密钥-医院映射"""
    if not os.path.exists(KEY_MAP_FILE):
        return {}
    try:
        with open(KEY_MAP_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_key_map(mapping):
    """保存密钥-医院映射"""
    try:
        with open(KEY_MAP_FILE, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存密钥映射失败: {e}")

# 在模块级别创建Paillier加密器实例，以便所有函数共享
encryptor = PaillierEncryptor()

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
        # encryptor = PaillierEncryptor()  # 移除此处实例化，使用模块级别的encryptor
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
            decrypted_data.append(decrypted_record)

        return jsonify({'code': 200, 'msg': '数据查询成功', 'data': decrypted_data})  # 返回成功响应
    except Exception as e:  # 捕获异常
        return jsonify({'code': 500, 'msg': '数据查询失败: ' + str(e)})  # 返回错误响应


# 获取所有加密数据（带分页）
def getAllEncryptedData():
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)  # 从请求参数中获取页码，默认为1
        page_size = request.args.get('page_size', 10, type=int)  # 从请求参数中获取每页大小，默认为10
        group_id_str = request.args.get('group_id', type=str) # 新增：从请求参数中获取group_id，期望是字符串类型
        
        # 计算偏移量
        offset = (page - 1) * page_size # 计算数据库查询的偏移量
        
        # 基础查询
        query = Shuju2.query # 初始化查询对象，针对Shuju2模型

        # 如果提供了group_id，则根据group_id进行过滤
        if group_id_str:
            try:
                group_id = int(group_id_str) # 将group_id转换为整数进行查询
                query = query.filter(Shuju2.group_id == group_id) # 直接在Shuju2表上根据group_id过滤
            except ValueError:
                # 如果group_id无法转换为整数，则返回错误信息
                return jsonify({'code': 400, 'msg': 'group_id必须是有效的整数值'}), 400

        # 查询总记录数 (应用过滤条件后)
        total_count = query.count() # 获取满足条件的总记录数
        
        # 查询shuju2表，获取分页数据 (应用过滤条件后)
        shuju2_records = query.limit(page_size).offset(offset).all() # 获取分页后的数据记录
        
        if not shuju2_records:
            # 即便 total_count > 0，当前页也可能没有数据（例如请求一个不存在的页码）
            return jsonify({
                'code': 200, # 保持200，因为请求是成功的，只是没有数据
                'msg': '未找到加密数据' if not group_id_str else f'分组 {group_id_str} 在当前页未找到加密数据',
                'data': [],
                'total': total_count,
                'page': page,
                'page_size': page_size
            })

        # 获取当前页数据的ID列表，用于后续查找关联的user_id
        data_ids_current_page = [str(record.id) for record in shuju2_records] 
        
        # 查询这些数据ID关联的user_id
        # 注意：这里仍然需要UserData表来获取user_id，因为Shuju2表本身没有user_id字段
        user_data_link_records = db.session.query(UserData.data_id, UserData.user_id).\
            filter(UserData.data_id.in_(data_ids_current_page)).\
            all()
        
        # 构建data_id到user_id的映射
        data_to_user_map = {str(data_id): user_id for data_id, user_id in user_data_link_records}

        # 解密数据
        decrypted_data = [] # 初始化解密数据列表
        
        for record in shuju2_records: # 遍历当前页的每条加密记录
            user_id_for_record = data_to_user_map.get(str(record.id)) # 通过映射获取user_id
            
            decrypted_record = { # 构建解密后的记录字典
                'id': record.id,
                'user_id': user_id_for_record, # 添加user_id到解密记录中
                'group_id': record.group_id, # 同时也可以返回记录本身的group_id
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
            decrypted_data.append(decrypted_record) # 将解密后的记录添加到列表中

        return jsonify({ # 返回成功的JSON响应
            'code': 200, 
            'msg': '数据查询成功',
            'data': decrypted_data,
            'total': total_count, # 总记录数
            'page': page, # 当前页码
            'page_size': page_size # 每页大小
        })
    except Exception as e: # 捕获所有异常
        # 打印更详细的错误信息到服务器日志，方便调试
        print(f"Error in getAllEncryptedData: {e}") 
        import traceback
        traceback.print_exc() # 打印完整的堆栈跟踪
        return jsonify({'code': 500, 'msg': '数据查询失败: ' + str(e)}) # 返回失败的JSON响应

# 根据关键字查询数据（支持ID或用户ID）
def getEncryptedData():
    keyword = request.args.get('keyword')
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    
    if not keyword:
        return jsonify({'code': 400, 'msg': '请提供查询关键字'})
    
    try:
        # 构建基础查询，关联UserData表
        query = db.session.query(Shuju2, UserData.user_id).join(
            UserData, Shuju2.id == UserData.data_id, isouter=True
        )
        
        # 尝试将关键字转换为整数进行ID匹配
        try:
            keyword_int = int(keyword)
            # 匹配数据ID或用户ID
            query = query.filter(
                (Shuju2.id == keyword_int) | 
                (UserData.user_id == keyword) 
            )
        except ValueError:
            # 如果关键字不是纯数字，仅尝试匹配用户ID（假设用户ID可能是字符串）
            query = query.filter(UserData.user_id == keyword)
        
        # 获取总记录数
        total_count = query.count()
        
        # 计算偏移量
        offset = (page - 1) * page_size
        
        # 获取分页数据
        results = query.limit(page_size).offset(offset).all()
        
        if not results:
            return jsonify({'code': 404, 'msg': '未找到匹配的数据'})
        
        # 解密数据
        # encryptor = PaillierEncryptor()  # 移除此处实例化，使用模块级别的encryptor
        decrypted_data = []  # 初始化解密后的数据列表
            
        for shuju2, user_id_result in results:
            decrypted_record = {
                'id': shuju2.id,
                'user_id': user_id_result, # 将 user_id_value 修正为 user_id_result
                'cirrhosis': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.cirrhosis))), # 解密肝硬化数据
                'age': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.age))), # 解密年龄数据
                'sex': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.sex))), # 解密性别数据
                'cholesterol': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.cholesterol))), # 解密胆固醇数据
                'triglyceride': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.triglyceride))), # 解密甘油三酯数据
                'HDL': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.HDL))), # 解密高密度脂蛋白数据
                'LDL': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.LDL))) / FLOAT_PRECISION, # 解密低密度脂蛋白数据
                'PathDiagNum': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.PathDiagNum))), # 解密病理诊断编号数据
                'BMI': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.BMI))) / FLOAT_PRECISION, # 解密体重指数数据
                'ALT': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.ALT))), # 解密谷丙转氨酶数据
                'AST': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.AST))), # 解密谷草转氨酶数据
                'glucose': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(shuju2.glucose))) # 解密血糖数据
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

        # encryptor = PaillierEncryptor() # 移除此处实例化，使用模块级别的encryptor

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


# 明文求平均值接口
def getPlainAverages():
    try:
        from service.yanzheng import calculate_averages  # 直接导入函数
        group_id = request.args.get('group_id', 1, type=int)
        averages = calculate_averages(group_id=group_id)  # 直接调用函数
        return jsonify({
            'code': 200,
            'msg': '平均值计算成功',
            'data': averages
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': '平均值计算失败: ' + str(e)})

# 选择Paillier密钥对接口
def select_keypair():
    try:
        # 从请求参数中获取密钥索引，默认为1
        key_index = request.args.get('key_index', 1, type=int)
        
        # 创建Paillier加密器实例并加载指定索引的密钥对
        # encryptor = PaillierEncryptor() # 移除此处实例化，使用模块级别的encryptor
        encryptor.load_or_generate_keypair(key_index)
        
        # 返回当前加载的密钥信息
        return jsonify({
            'code': 200,
            'msg': f'成功加载第{key_index}个密钥对',
            'data': encryptor.get_current_key_info()
        })
    except Exception as e:
        # 捕获异常并返回错误信息
        return jsonify({'code': 500, 'msg': '选择密钥对失败: ' + str(e)})





def get_keypair_names():
    try:
        # 定义密钥文件目录
        key_dir = 'e:\\桌面\\zuoye\\密码学课设\\Medical_data_analysis_system\\service\\private_key'
        # 获取所有以.pkl结尾的文件名
        key_files = [f for f in os.listdir(key_dir) if f.endswith('.pkl')]
        
        mapping = load_key_map()
        
        result = []
        for f in key_files:
            # 提取索引
            match = re.search(r'private_key(\d+).pkl', f)
            if match:
                idx = int(match.group(1))
                hospital = mapping.get(str(idx), "未知医院")
                result.append({'id': idx, 'hospital_name': hospital, 'filename': f})
            else:
                result.append({'id': f, 'hospital_name': "Unknown", 'filename': f})
                
        # 按ID排序
        result.sort(key=lambda x: x['id'] if isinstance(x['id'], int) else 0)
        
        # 返回包含详细信息的列表
        return jsonify({
            'code': 200,
            'msg': '成功获取密钥文件信息',
            'data': result
        })
    except Exception as e:
        # 捕获异常并返回错误信息
        return jsonify({'code': 500, 'msg': '获取密钥文件名称失败: ' + str(e)})


# 新增密钥对接口
def generate_new_keypair():
    try:
        # 从 GET 请求的查询参数中获取 key_index
        key_index = request.args.get('key_index')
        hospital_name = request.args.get('hospital_name', '未命名医院')

        # 如果没有提供 key_index，自动计算下一个可用的索引
        if not key_index:
            key_dir = 'e:\\桌面\\zuoye\\密码学课设\\Medical_data_analysis_system\\service\\private_key'
            if not os.path.exists(key_dir):
                os.makedirs(key_dir)
            
            existing_indices = []
            for f in os.listdir(key_dir):
                match = re.search(r'private_key(\d+).pkl', f)
                if match:
                    existing_indices.append(int(match.group(1)))
            
            if existing_indices:
                key_index = max(existing_indices) + 1
            else:
                key_index = 1
        else:
            # 将 key_index 转换为整数
            try:
                key_index = int(key_index)
            except ValueError:
                return jsonify({'code': 400, 'msg': 'key_index 必须是整数'}), 400

        # 调用 PaillierEncryptor 中的 generate_keypair 方法生成密钥对
        # encryptor 实例已在模块级别创建
        encryptor.generate_keypair(key_index)
        
        # 保存映射
        mapping = load_key_map()
        mapping[str(key_index)] = hospital_name
        save_key_map(mapping)
        
        # 返回成功信息
        return jsonify({
            'code': 200,
            'msg': f'成功生成密钥对，索引为 {key_index}',
            'data': {
                'public_key_file': encryptor.public_key_file,
                'private_key_file': encryptor.private_key_file,
                'hospital_name': hospital_name
            }
        })
    except FileExistsError as fee: # 捕获文件已存在的异常
        return jsonify({'code': 409, 'msg': str(fee)}), 409 # 返回 409 Conflict 状态码
    except Exception as e: # 捕获其他所有异常
        # 捕获异常并返回错误信息
        return jsonify({'code': 500, 'msg': '生成密钥对失败: ' + str(e)}), 500


