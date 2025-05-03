from flask import request, jsonify
from service.analyse import AnalyseService  # 导入分析服务类
from models import Analysis_result  # 导入Analysis_result模型

def data_processing():  # 定义数据处理接口
    try:
        analyse_service = AnalyseService()  # 创建分析服务实例
        average_age = analyse_service.average_encrypted_data('age')  # 计算age字段的平均值
        return jsonify({'code': 200, 'data': average_age})  # 返回平均值
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'服务器内部错误: {str(e)}'})  # 返回错误信息

def privacy_intersection():  # 定义隐私求交接口
    """
    隐私求交接口，接收前端传来的数据ID，计算该数据与数据库中其他数据的交集情况
    
    请求参数:
        data_id: 数据ID，整数类型
        
    返回:
        成功: {'code': 200, 'data': percentage} - percentage为交集占比百分比
        失败: {'code': 400/500, 'msg': 错误信息}
    """
    try:
        # 获取请求参数
        data_id = request.args.get('data_id')  # 获取数据ID参数
        
        # 参数验证
        if not data_id:  # 如果数据ID为空
            return jsonify({'code': 400, 'msg': '缺少数据ID参数'})  # 返回错误信息
            
        # 先查询Analysis_result表中是否已有该ID的分析结果
        existing_result = Analysis_result.query.filter_by(id=data_id).first()
        
        if existing_result:  # 如果已有分析结果
            # 返回错误信息，说明已有结果
            return jsonify({
                'code': 400,  # 状态码
                'msg': f'ID为{data_id}的数据已有分析结果，无需重复分析'  # 错误信息
            })
        
        # 如果没有已有分析结果，则调用隐私求交方法进行分析
        analyse_service = AnalyseService()  # 创建分析服务实例
        percentage = analyse_service.privacy_preserving_intersection(data_id)  # 计算交集占比
        
        # 返回结果
        return jsonify({
            'code': 200,  # 状态码
            'data': percentage,  # 交集占比
            'msg': f'分析成功，ID为{data_id}的数据与其他数据的平均相似度为{percentage:.2f}%'  # 成功信息
        })
        
    except Exception as e:  # 捕获异常
        # 记录错误信息
        import traceback  # 导入traceback模块
        traceback.print_exc()  # 打印详细错误信息
        
        # 返回错误响应
        return jsonify({
            'code': 500,  # 状态码
            'msg': f'服务器内部错误: {str(e)}'  # 错误信息
        })


def get_data_analysis_result():
    """
    获取数据分析结果接口
    
    请求参数:
        user_id: 用户ID，整数类型
        
    返回:
        成功: {'code': 200, 'data': {...}} - 包含原始数据和分析结果
        失败: {'code': 400/404/500, 'msg': 错误信息}
    """
    try:
        # 获取请求参数
        user_id = request.args.get('user_id')  # 获取用户ID参数
        
        # 参数验证
        if not user_id:  # 如果用户ID为空
            return jsonify({
                'code': 400, 
                'msg': '缺少用户ID参数'
            })  # 返回错误信息
        
        # 根据user_id查询user_data表获取data_id
        from models import UserData  # 导入UserData模型
        user_data_records = UserData.query.filter_by(user_id=user_id).all()  # 查询用户数据记录
        
        if not user_data_records:  # 如果没有找到用户数据记录
            return jsonify({
                'code': 404, 
                'msg': f'未找到用户ID为{user_id}的数据记录'
            })  # 返回错误信息
        
        # 获取所有data_id
        data_ids = [record.data_id for record in user_data_records]  # 提取所有data_id
        
        # 初始化结果列表
        result_list = []
        
        # 创建加密器实例
        from service.Paillier import PaillierEncryptor  # 导入Paillier加密器
        encryptor = PaillierEncryptor()  # 创建加密器实例
        
        # 导入配置和模型
        from config import FLOAT_PRECISION  # 导入浮点精度配置
        from models import Shuju2, Analysis_result  # 导入Shuju2和Analysis_result模型
        
        # 遍历每个data_id，获取原始数据和分析结果
        for data_id in data_ids:
            # 查询shuju2表获取密文数据
            encrypted_record = Shuju2.query.filter_by(id=data_id).first()  # 查询加密数据记录
            
            if not encrypted_record:  # 如果没有找到加密数据记录
                continue  # 跳过当前循环
            
            # 解密数据
            decrypted_data = {
                'id': encrypted_record.id,  # 数据ID
                'cirrhosis': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_record.cirrhosis))),  # 解密肝硬化数据
                'age': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_record.age))),  # 解密年龄数据
                'sex': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_record.sex))),  # 解密性别数据
                'cholesterol': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_record.cholesterol))),  # 解密胆固醇数据
                'triglyceride': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_record.triglyceride))),  # 解密甘油三酯数据
                'HDL': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_record.HDL))),  # 解密高密度脂蛋白数据
                'LDL': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_record.LDL))) / FLOAT_PRECISION,  # 解密低密度脂蛋白数据
                'PathDiagNum': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_record.PathDiagNum))),  # 解密病理诊断编号数据
                'BMI': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_record.BMI))) / FLOAT_PRECISION,  # 解密体重指数数据
                'ALT': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_record.ALT))),  # 解密谷丙转氨酶数据
                'AST': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_record.AST))),  # 解密谷草转氨酶数据
                'glucose': encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(encrypted_record.glucose)))  # 解密血糖数据
            }
            
            # 查询Analysis_result表获取分析结果
            analysis_result = Analysis_result.query.filter_by(id=data_id).first()  # 查询分析结果记录
            
            # 如果有分析结果，则添加到解密数据中
            if analysis_result:
                analysis_data = {
                    'cirrhosis_similarity': analysis_result.cirrhosis,  # 肝硬化相似度
                    'age_similarity': analysis_result.age,  # 年龄相似度
                    'sex_similarity': analysis_result.sex,  # 性别相似度
                    'cholesterol_similarity': analysis_result.cholesterol,  # 胆固醇相似度
                    'triglyceride_similarity': analysis_result.triglyceride,  # 甘油三酯相似度
                    'HDL_similarity': analysis_result.HDL,  # 高密度脂蛋白相似度
                    'LDL_similarity': analysis_result.LDL,  # 低密度脂蛋白相似度
                    'PathDiagNum_similarity': analysis_result.PathDiagNum,  # 病理诊断编号相似度
                    'BMI_similarity': analysis_result.BMI,  # 体重指数相似度
                    'ALT_similarity': analysis_result.ALT,  # 谷丙转氨酶相似度
                    'AST_similarity': analysis_result.AST,  # 谷草转氨酶相似度
                    'glucose_similarity': analysis_result.glucose,  # 血糖相似度
                    'created_at': str(analysis_result.created_at)  # 创建时间
                }
                
                # 计算平均相似度
                similarity_fields = ['cirrhosis', 'age', 'sex', 'cholesterol', 'triglyceride', 
                                    'HDL', 'LDL', 'PathDiagNum', 'BMI', 'ALT', 'AST', 'glucose']
                similarity_values = [getattr(analysis_result, field) for field in similarity_fields]
                avg_similarity = sum(similarity_values) / len(similarity_values)
                
                # 添加平均相似度
                analysis_data['avg_similarity'] = round(avg_similarity, 2)  # 平均相似度，保留两位小数
            else:
                analysis_data = None  # 如果没有分析结果，则设为None
            
            # 构建完整结果
            result_item = {
                'original_data': decrypted_data,  # 原始数据
                'analysis_result': analysis_data  # 分析结果
            }
            
            # 添加到结果列表
            result_list.append(result_item)
        
        # 如果没有找到任何有效数据，返回错误信息
        if not result_list:
            return jsonify({
                'code': 404, 
                'msg': f'未找到用户ID为{user_id}的有效数据'
            })
        
        # 返回成功响应
        return jsonify({
            'code': 200, 
            'msg': '数据查询成功', 
            'data': result_list,
            'total': len(result_list)
        })
        
    except Exception as e:  # 捕获异常
        # 记录错误信息
        import traceback  # 导入traceback模块
        traceback.print_exc()  # 打印详细错误信息
        
        # 返回错误响应
        return jsonify({
            'code': 500, 
            'msg': f'服务器内部错误: {str(e)}'
        })


