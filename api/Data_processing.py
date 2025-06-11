from flask import request, jsonify
from service.analyse import AnalyseService  # 导入分析服务类
from models import Analysis_result,Shuju2  # 导入Analysis_result模型
from db_config import db  # 导入数据库配置
import traceback  # 导入traceback模块
from models import UserData  # 导入UserData模型
from service.Paillier import PaillierEncryptor  # 导入Paillier加密器
from config import FLOAT_PRECISION  # 导入浮点精度配置
from sqlalchemy.exc import OperationalError  # 导入OperationalError异常
import time  # 导入time模块，用于延时重试

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
            # 计算平均相似度
            fields = ['cirrhosis', 'age', 'sex', 'cholesterol', 'triglyceride', 
                     'HDL', 'LDL', 'PathDiagNum', 'BMI', 'ALT', 'AST', 'glucose']
            
            # 获取所有字段的相似度值
            similarity_values = [getattr(existing_result, field) for field in fields]
            
            # 计算平均相似度
            avg_similarity = sum(similarity_values) / len(fields)
            
            # 返回已有结果
            return jsonify({
                'code': 200,  # 状态码
                'data': round(avg_similarity, 2),  # 交集占比（平均相似度）
                'msg': f'ID为{data_id}的数据已有分析结果，平均相似度为{avg_similarity:.2f}%'  # 成功信息
            })
        
        # 如果没有已有分析结果，则进行隐私求交分析
        
        
        # 2. 查询目标记录
        target_record = Shuju2.query.filter_by(id=data_id).first()  # 获取指定ID的记录
        if not target_record:  # 如果没有找到记录
            return jsonify({
                'code': 404,  # 状态码
                'msg': f'没有找到ID为{data_id}的记录'  # 错误信息
            })
        
        # 3. 查询所有记录
        all_records = Shuju2.query.all()  # 获取所有记录
        if not all_records:  # 如果没有记录
            return jsonify({
                'code': 404,  # 状态码
                'msg': '没有找到任何记录'  # 错误信息
            })
        
        # 4. 创建分析服务实例
        analyse_service = AnalyseService()  # 创建分析服务实例
        
        # 5. 定义需要比较的字段
        fields = ['cirrhosis', 'age', 'sex', 'cholesterol', 'triglyceride', 
                 'HDL', 'LDL', 'PathDiagNum', 'BMI', 'ALT', 'AST', 'glucose']  # 所有需要比较的字段
        
        # 6. 定义需要完全匹配的字段
        exact_match_fields = ['sex', 'cirrhosis', 'PathDiagNum'] 
        
        # 7. 初始化各字段的交集百分比
        intersection_percentages = {}
        
        # 8. 对每个字段进行隐私求交
        for field in fields:
            # 获取目标记录的字段值
            print(f"field: {field}开始隐私求交")  # 打印字段名
            target_value = getattr(target_record, field)
            
            # 获取所有记录的该字段值列表
            all_values = [getattr(record, field) for record in all_records if record.id != data_id]
            
            # 根据字段类型选择匹配方法
            if field in exact_match_fields:
                # 完全匹配
                percentage = analyse_service.privacy_preserving_exact_match(target_value, all_values)
            elif field in ['LDL', 'BMI']:
                # 模糊匹配，带精度因子
                from config import FLOAT_PRECISION  # 导入浮点精度配置
                percentage = analyse_service.privacy_preserving_fuzzy_match(target_value, all_values, FLOAT_PRECISION)
            else:
                # 模糊匹配，不带精度因子
                percentage = analyse_service.privacy_preserving_fuzzy_match(target_value, all_values)
            
            # 存储该字段的交集百分比
            intersection_percentages[field] = percentage
        
        # 9. 计算平均百分比
        avg_percentage = sum(intersection_percentages.values()) / len(intersection_percentages)
        
        # 10. 将结果存入Analysis_result表
        result = Analysis_result(  # 创建Analysis_result实例
            id=data_id,  # 使用传入参数的id
            cirrhosis=intersection_percentages['cirrhosis'],  # 肝硬化字段百分比
            age=intersection_percentages['age'],  # 年龄字段百分比
            sex=intersection_percentages['sex'],  # 性别字段百分比
            cholesterol=intersection_percentages['cholesterol'],  # 胆固醇字段百分比
            triglyceride=intersection_percentages['triglyceride'],  # 甘油三酯字段百分比
            HDL=intersection_percentages['HDL'],  # 高密度脂蛋白字段百分比
            LDL=intersection_percentages['LDL'],  # 低密度脂蛋白字段百分比
            PathDiagNum=intersection_percentages['PathDiagNum'],  # 病理诊断编号字段百分比
            BMI=intersection_percentages['BMI'],  # 体重指数字段百分比
            ALT=intersection_percentages['ALT'],  # 谷丙转氨酶字段百分比
            AST=intersection_percentages['AST'],  # 谷草转氨酶字段百分比
            glucose=intersection_percentages['glucose']  # 血糖字段百分比
        )
        
        # 添加到数据库会话并提交（带重试机制）
        max_retries = 3  # 最大重试次数
        retry_count = 0  # 当前重试次数
        
        while retry_count < max_retries:  # 当重试次数小于最大重试次数时循环
            try:
                db.session.add(result)  # 添加到会话
                db.session.commit()  # 提交到数据库
                print(f"分析结果已保存到analysis_result表，ID: {result.id}")  # 打印保存成功信息
                break  # 成功后跳出循环
            except OperationalError as e:  # 捕获数据库操作异常
                retry_count += 1  # 重试次数加1
                print(f"数据库连接错误，正在进行第{retry_count}次重试...")  # 打印重试信息
                
                # 回滚会话
                db.session.rollback()  # 回滚数据库会话
                
                # 如果不是最后一次重试，则等待后重试
                if retry_count < max_retries:  # 如果不是最后一次重试
                    # 重新连接数据库
                    db.session.close()  # 关闭当前会话
                    db.engine.dispose()  # 释放所有连接池中的连接
                    
                    # 等待一段时间再重试
                    time.sleep(2 * retry_count)  # 等待时间随重试次数增加
                else:
                    # 最后一次重试失败，抛出异常
                    raise Exception(f"数据库连接错误，重试{max_retries}次后仍然失败: {str(e)}")  # 抛出异常
        
        # 11. 返回结果
        return jsonify({
            'code': 200,  # 状态码
            'data': round(avg_percentage, 2),  # 交集占比
            'msg': f'分析成功，ID为{data_id}的数据与其他数据的平均相似度为{avg_percentage:.2f}%'  # 成功信息
        })
        
    except Exception as e:  # 捕获异常
        # 记录错误信息
        traceback.print_exc()  # 打印详细错误信息
        
        # 回滚数据库会话
        db.session.rollback()  # 回滚数据库会话
        
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
        

        
        
        # 遍历每个data_id，获取原始数据和分析结果
        for data_id in data_ids:
            # 查询shuju2表获取密文数据
            encrypted_record = Shuju2.query.filter_by(id=data_id).first()  # 查询加密数据记录
            
            if not encrypted_record:
                continue

            # 根据group_id选择密钥对
            # 每次循环都创建一个新的PaillierEncryptor实例，并加载对应group_id的密钥对
            encryptor = PaillierEncryptor()  # 创建加密器实例
            encryptor.load_or_generate_keypair(index=encrypted_record.group_id) # 根据group_id加载密钥对

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
        traceback.print_exc()  # 打印详细错误信息
        
        # 返回错误响应
        return jsonify({
            'code': 500, 
            'msg': f'服务器内部错误: {str(e)}'
        })


