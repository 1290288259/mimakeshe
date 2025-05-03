# 导入必要的模块
from service.analyse import AnalyseService
from flask import jsonify, current_app
from models import Avg , Shuju2  # 导入你定义的Avg模型
from db_config import db  # 导入数据库配置
from service.Paillier import PaillierEncryptor  # 导入Paillier加密器
# 定义全局变量，浮点型精度
FLOAT_PRECISION = 10

def calculate_avg():
    """
    计算各字段加密数据的平均值，并存入avg表
    返回:
        JSON响应: 包含状态码、消息和各字段平均值数据
    """
    try:
        # 获取当前Flask应用上下文对象
        app = current_app._get_current_object()
        
        # 创建分析服务实例
        service = AnalyseService()
        
        # 需要计算平均值的字段列表
        numeric_fields = [ 'age', 'cholesterol',
                         'triglyceride', 'HDL', 'LDL', 'BMI',
                         'ALT', 'AST', 'glucose']
        
        # 初始化结果字典
        results = {}

        # 单线程：依次计算每个字段的平均值
        for field in numeric_fields:
            try:
                # 直接调用分析服务的平均值计算方法
                avg = service.average_encrypted_data(field)
                # 保留FLOAT_PRECISION位小数
                if avg is not None:
                    avg = round(avg, FLOAT_PRECISION)
                # 对LDL和BMI字段，先除以FLOAT_PRECISION再存储
                if field in ['LDL', 'BMI'] and avg is not None:
                    avg = avg / FLOAT_PRECISION
                # 存储结果
                results[field] = avg
                print(f"已完成{field}字段的平均值计算")
            except Exception as e:
                print(f"计算{field}平均值时出错: {str(e)}")
        
        # 将结果存入avg表
        try:
            # 创建Avg对象，字段与表结构对应
            avg_record = Avg(
                age=results.get('age'),
                cholesterol=results.get('cholesterol'),
                triglyceride=results.get('triglyceride'),
                HDL=results.get('HDL'),
                LDL=results.get('LDL'),
                BMI=results.get('BMI'),
                ALT=results.get('ALT'),
                AST=results.get('AST'),
                glucose=results.get('glucose')
            )
            db.session.add(avg_record)  # 添加到会话
            db.session.commit()         # 提交到数据库
            print("平均值已成功存入avg表")
        except Exception as e:
            print(f"存入avg表时出错: {str(e)}")
        
        # 返回成功的JSON响应
        return jsonify({
            'code': 200,
            'msg': '平均值计算并存储成功',
            'data': results
        })
        
    except Exception as e:
        # 捕获异常并返回错误信息
        return jsonify({
            'code': 500,
            'msg': f'平均值计算失败: {str(e)}'
        })

def get_avg():
    """
    从avg表获取最新一条平均值数据
    返回:
        JSON响应: 包含状态码、消息和最新一条平均值数据
    """
    try:
        # 查询avg表中最新一条数据（按created_at倒序）
        latest_avg = Avg.query.order_by(Avg.created_at.desc()).first()
        if latest_avg is None:
            return jsonify({
                'code': 404,
                'msg': '没有找到平均值数据',
                'data': None
            })
        # 构造返回数据字典
        data = {
            'age': latest_avg.age,
            'cholesterol': latest_avg.cholesterol,
            'triglyceride': latest_avg.triglyceride,
            'HDL': latest_avg.HDL,
            'LDL': latest_avg.LDL,
            'BMI': latest_avg.BMI,
            'ALT': latest_avg.ALT,
            'AST': latest_avg.AST,
            'glucose': latest_avg.glucose,
            'created_at': str(latest_avg.created_at)
        }
        return jsonify({
            'code': 200,
            'msg': '获取最新平均值成功',
            'data': data
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'获取平均值失败: {str(e)}'
        })

def get_all_age_data():
    """
    查询shuju2表中age字段的所有加密数据，解密后传给前端
    返回:
        JSON响应: 包含状态码、消息和解密后的age数据列表
    """
    try:
        # 创建加密器实例
        encryptor = PaillierEncryptor()
        
        # 查询所有数据记录
        records = Shuju2.query.all()
        
        # 解密age字段数据
        decrypted_age_data = []
        for record in records:
            if record.age is not None:
                # 使用与ShowData.py相同的解密方式
                decrypted_age = encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(record.age)))
                decrypted_age_data.append(decrypted_age)
            else:
                decrypted_age_data.append(None)
        
        # 如果没有数据，返回空列表
        if not decrypted_age_data:
            return jsonify({
                'code': 200,
                'msg': '没有找到age字段数据',
                'data': []
            })
        
        # 返回成功的JSON响应，包含解密后的age数据
        return jsonify({
            'code': 200,
            'msg': '获取age字段数据成功',
            'data': decrypted_age_data
        })
        
    except Exception as e:
        # 捕获异常并返回错误信息
        import traceback
        error_trace = traceback.format_exc()
        print(f"获取age字段数据失败: {str(e)}\n{error_trace}")
        return jsonify({
            'code': 500,
            'msg': f'获取age字段数据失败: {str(e)}',
            'data': None
        })


def get_avg_by_age_group():
    """
    根据年龄段计算指定字段的平均值
    
    请求参数:
        field_name: 需要计算平均值的字段名称
        
    返回:
        JSON响应: 包含状态码、消息和各年龄段平均值数据
    """
    try:
        # 从请求中获取字段名称
        from flask import request  # 导入request模块
        field_name = request.args.get('field_name')  # 获取字段名称参数
        
        # 验证字段名称是否有效
        valid_fields = [  'cholesterol', 'triglyceride', 
                        'HDL', 'LDL', 'BMI', 'ALT', 'AST', 'glucose']
        
        if not field_name:  # 如果没有提供字段名称
            return jsonify({
                'code': 400,
                'msg': '缺少字段名称参数',
                'data': None
            })
        
        if field_name not in valid_fields:  # 如果字段名称无效
            return jsonify({
                'code': 400,
                'msg': f'无效的字段名称，有效字段: {", ".join(valid_fields)}',
                'data': None
            })
        
        # 创建分析服务实例
        service = AnalyseService()
        
        # 调用服务层方法计算各年龄段平均值
        result = service.calculate_avg_by_age_group(field_name)
        
        # 如果结果为空，返回错误信息
        if not result:
            return jsonify({
                'code': 404,
                'msg': '没有找到有效数据',
                'data': None
            })
        
        # 返回成功的JSON响应，包含各年龄段平均值数据
        return jsonify({
            'code': 200,
            'msg': '获取各年龄段平均值成功',
            'data': result
        })
        
    except Exception as e:
        # 捕获异常并返回错误信息
        import traceback
        error_trace = traceback.format_exc()
        print(f"获取各年龄段平均值失败: {str(e)}\n{error_trace}")
        return jsonify({
            'code': 500,
            'msg': f'获取各年龄段平均值失败: {str(e)}',
            'data': None
        })
