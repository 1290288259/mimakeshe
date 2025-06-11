# 导入必要的模块
from service.analyse import AnalyseService
from flask import jsonify, current_app ,request
from models import Avg , Shuju2 ,AgeGroupAvg # 导入你定义的Avg模型
from db_config import db  # 导入数据库配置
from service.Paillier import PaillierEncryptor  # 导入Paillier加密器
from datetime import datetime # 导入 datetime 模块
from datetime import datetime, timezone, timedelta # 导入timezone和timedelta
# 定义全局变量，浮点型精度
FLOAT_PRECISION = 10

def calculate_avg():
    """
    计算各字段加密数据的平均值，并存入avg表
    返回:
        JSON响应: 包含状态码、消息和各字段平均值数据
    """
    try:
        
        # 创建分析服务实例
        service = AnalyseService()
        
        # 需要计算平均值的字段列表
        numeric_fields = ['age', 'cholesterol',
                         'triglyceride', 'HDL', 'LDL', 'BMI',
                         'ALT', 'AST', 'glucose']
        
        # 初始化结果字典
        results = {}

        # 单线程：依次计算每个字段的平均值
        for field in numeric_fields:
            try:
                # 查询记录总数，只计算group_id=1的数据
                record_count = Shuju2.query.filter_by(group_id=1).count()
                print(f"{field}字段的总记录数: {record_count}")
                
                if record_count == 0:  # 如果没有记录
                    results[field] = 0
                    continue
                
                # 分批查询处理，减少内存占用
                batch_size = 50  # 每批处理50条记录
                encrypted_data = []  # 存储加密数据
                
                # 分批查询数据，只查询group_id=1的数据
                for offset in range(0, record_count, batch_size):
                    # 查询一批数据
                    batch = Shuju2.query.filter_by(group_id=1).with_entities(
                        getattr(Shuju2, field)
                    ).limit(batch_size).offset(offset).all()
                    
                    # 提取密文数据
                    for record in batch:
                        encrypted_data.append(record[0])
                    
                    # 打印查询进度
                    print(f"{field}字段数据查询进度: {min(offset+batch_size, record_count)}/{record_count}")
                
                # 调用分析服务的平均值计算方法，传入加密数据列表
                avg = service.average_encrypted_data(encrypted_data)
                
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
        
        # 将结果存入avg表，并添加重试机制
        max_retries = 3
        for attempt in range(max_retries):
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
                print(f"平均值已成功存入avg表 (尝试 {attempt + 1}/{max_retries})")
                break  # 成功后跳出循环
            except Exception as e:
                db.session.rollback() # 发生错误时回滚事务
                print(f"存入avg表时出错 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                if attempt == max_retries - 1:
                    # 如果是最后一次尝试，则抛出异常或返回错误响应
                    return jsonify({
                        'code': 500,
                        'msg': f'平均值存入数据库失败，已重试 {max_retries} 次: {str(e)}'
                    }), 500

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
        
        # 查询所有数据记录，只查询group_id=1的数据
        records = Shuju2.query.filter_by(group_id=1).all()
        
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


# 定义一个函数用于计算各年龄段平均值并存储到数据库
def calculate_and_store_age_group_avg():
    """
    根据年龄段计算指定字段的平均值，并存储到数据库。
    
    参数:
        field_name: 需要计算平均值的字段名称
    
    返回:
        bool: 存储操作是否成功
    """
    try:
        field_name = request.args.get('field_name')  # 获取字段名称参数

        # 验证字段名称是否有效
        valid_fields = [  'cholesterol', 'triglyceride',
                        'HDL', 'LDL', 'BMI', 'ALT', 'AST', 'glucose']

        if field_name not in valid_fields:
            print(f"无效的字段名称: {field_name}")
            return False

        # 创建分析服务实例
        service = AnalyseService()

        # 从数据库中查询所有记录，但只获取年龄字段和目标字段
        records = Shuju2.query.with_entities(
            Shuju2.age,
            getattr(Shuju2, field_name)
        ).all()  # 只获取需要的两个字段

        if not records:
            print("没有找到有效数据")
            return False

        # 初始化年龄段分组
        age_groups = {
            '0-9': [],    # 0-9岁年龄段的数据列表
            '10-19': [],  # 10-19岁年龄段的数据列表
            '20-29': [],  # 20-29岁年龄段的数据列表
            '30-39': [],  # 30-39岁年龄段的数据列表
            '40-49': [],  # 40-49岁年龄段的数据列表
            '50-59': [],  # 50-59岁年龄段的数据列表
            '60-69': [],  # 60-69岁年龄段的数据列表
            '70-79': [],  # 70-79岁年龄段的数据列表
            '80+': []     # 80岁及以上年龄段的数据列表
        }

        # 遍历所有记录，解密年龄并按年龄段分组
        for record in records:
            if record.age is not None and getattr(record, field_name) is not None:
                try:
                    # 解密年龄
                    decrypted_age = service.encryptor.decrypt(
                        service.encryptor.public_key.encrypt(0).__class__(
                            service.encryptor.public_key, int(record.age)
                        )
                    )

                    # 获取指定字段的密文
                    field_ciphertext = getattr(record, field_name)

                    # 根据年龄分组
                    if 0 <= decrypted_age < 10:
                        age_groups['0-9'].append(field_ciphertext)  # 添加到0-9岁组
                    elif 10 <= decrypted_age < 20:
                        age_groups['10-19'].append(field_ciphertext)  # 添加到10-19岁组
                    elif 20 <= decrypted_age < 30:
                        age_groups['20-29'].append(field_ciphertext)  # 添加到20-29岁组
                    elif 30 <= decrypted_age < 40:
                        age_groups['30-39'].append(field_ciphertext)  # 添加到30-39岁组
                    elif 40 <= decrypted_age < 50:
                        age_groups['40-49'].append(field_ciphertext)  # 添加到40-49岁组
                    elif 50 <= decrypted_age < 60:
                        age_groups['50-59'].append(field_ciphertext)  # 添加到50-59岁组
                    elif 60 <= decrypted_age < 70:
                        age_groups['60-69'].append(field_ciphertext)  # 添加到60-69岁组
                    elif 70 <= decrypted_age < 80:
                        age_groups['70-79'].append(field_ciphertext)  # 添加到70-79岁组
                    else:
                        age_groups['80+'].append(field_ciphertext)  # 添加到80岁及以上组
                except Exception as decrypt_error:
                    print(f"解密或分组数据时出错: {decrypt_error}")
                    continue # 跳过当前记录，继续处理下一条

        # 计算每个年龄段的平均值
        calculated_result = {}  # 初始化计算结果字典
        for age_group, ciphertexts in age_groups.items():
            if ciphertexts:  # 如果该年龄段有数据
                # 使用average_encrypted_data方法计算平均值
                avg = service.average_encrypted_data(ciphertexts)

                # 如果是BMI或LDL字段，将结果除以FLOAT_PRECISION
                # 确保service.FLOAT_PRECISION可用，如果FLOAT_PRECISION是全局常量，请直接使用FLOAT_PRECISION
                # 假设 FLOAT_PRECISION 是 service 实例的一个属性
                if field_name in ['BMI', 'LDL'] and avg is not None and hasattr(service, 'FLOAT_PRECISION'):
                     avg = avg / service.FLOAT_PRECISION  # 将结果除以FLOAT_PRECISION
                     print(f"{age_group}年龄段的{field_name}平均值(已除以{service.FLOAT_PRECISION}): {avg}")  # 打印调整后的结果

                calculated_result[age_group] = avg  # 存储计算结果
            else:
                calculated_result[age_group] = None  # 如果没有数据，设为None

        # 如果计算结果为空，打印信息并返回失败
        if not calculated_result:
            print("计算结果为空")
            # 返回一个包含错误信息的JSON响应
            return jsonify({'code': 400, 'msg': '计算结果为空', 'data': None}), 400

        # 将计算结果存储到AgeGroupAvg表中
        # 尝试查询是否存在该field_name的记录
        age_group_avg_record = AgeGroupAvg.query.filter_by(field_name=field_name).first()

        if age_group_avg_record: # 如果记录存在，则更新
            age_group_avg_record.age_0_9 = calculated_result.get('0-9')
            age_group_avg_record.age_10_19 = calculated_result.get('10-19')
            age_group_avg_record.age_20_29 = calculated_result.get('20-29')
            age_group_avg_record.age_30_39 = calculated_result.get('30-39')
            age_group_avg_record.age_40_49 = calculated_result.get('40-49')
            age_group_avg_record.age_50_59 = calculated_result.get('50-59')
            age_group_avg_record.age_60_69 = calculated_result.get('60-69')
            age_group_avg_record.age_70_79 = calculated_result.get('70-79')
            age_group_avg_record.age_80_plus = calculated_result.get('80+')
            age_group_avg_record.created_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=8)
            db.session.commit()
            print(f"已成功更新 {field_name} 的年龄段平均值记录")
        else: # 如果记录不存在，则创建新记录
            new_record = AgeGroupAvg(
                field_name=field_name,
                age_0_9=calculated_result.get('0-9'),
                age_10_19=calculated_result.get('10-19'),
                age_20_29=calculated_result.get('20-29'),
                age_30_39=calculated_result.get('30-39'),
                age_40_49=calculated_result.get('40-49'),
                age_50_59=calculated_result.get('50-59'),
                age_60_69=calculated_result.get('60-69'),
                age_70_79=calculated_result.get('70-79'),
                age_80_plus=calculated_result.get('80+'),
            )
            db.session.add(new_record)
            db.session.commit()
            print(f"已创建 {field_name} 的年龄段平均值新记录")

        # 存储成功后返回成功信息，而不是True
        return jsonify({'code': 200, 'msg': f'已成功更新 {field_name} 的年龄段平均值记录', 'data': None}), 200

    except Exception as e:
        # 捕获异常并打印错误信息
        import traceback
        error_trace = traceback.format_exc()
        print(f"计算并存储各年龄段平均值失败: {str(e)}{error_trace}")
        db.session.rollback() # 发生错误时回滚事务
        # 返回一个包含错误信息的JSON响应
        return jsonify({'code': 500, 'msg': f'计算并存储各年龄段平均值失败: {str(e)}', 'data': None}), 500

# 定义一个函数用于从数据库获取各年龄段平均值并返回给前端
def get_age_group_avg_from_db():
    """
    根据字段名称从数据库获取最新的年龄段平均值数据并返回给前端。

    请求参数:
        field_name: 需要获取平均值的字段名称

    返回:
        JSON响应: 包含状态码、消息和各年龄段平均值数据
    """
    try:
        # 从请求参数中获取字段名称
        field_name = request.args.get('field_name')  # 获取字段名称参数

        # 验证字段名称是否有效
        valid_fields = [  'cholesterol', 'triglyceride',
                        'HDL', 'LDL', 'BMI', 'ALT', 'AST', 'glucose']

        if not field_name:
            return jsonify({
                'code': 400,
                'msg': '缺少字段名称参数',
                'data': None
            })

        if field_name not in valid_fields:
            return jsonify({
                'code': 400,
                'msg': f'无效的字段名称，有效字段: {", ".join(valid_fields)}',
                'data': None
            })

        # 从数据库中获取最新的数据并返回给前端
        latest_data = AgeGroupAvg.query.filter_by(field_name=field_name).first()

        if latest_data:
            result_to_return = {
                '0-9': latest_data.age_0_9,
                '10-19': latest_data.age_10_19,
                '20-29': latest_data.age_20_29,
                '30-39': latest_data.age_30_39,
                '40-49': latest_data.age_40_49,
                '50-59': latest_data.age_50_59,
                '60-69': latest_data.age_60_69,
                '70-79': latest_data.age_70_79,
                '80+': latest_data.age_80_plus,
                'created_at': latest_data.created_at.strftime('%Y-%m-%d %H:%M:%S') if latest_data.created_at else None # 添加创建时间，格式化为字符串
            }
            return jsonify({
                'code': 200,
                'msg': '获取各年龄段平均值成功',
                'data': result_to_return
            })
        else:
            return jsonify({
                'code': 404,
                'msg': '未找到该字段的年龄段平均值数据',
                'data': None
            })

    except Exception as e:
        # 捕获异常并返回错误信息
        import traceback
        error_trace = traceback.format_exc()
        print(f"从数据库获取各年龄段平均值失败: {str(e)}{error_trace}")
        return jsonify({
            'code': 500,
            'msg': f'从数据库获取各年龄段平均值失败: {str(e)}',
            'data': None
        })

# 请注意：原有的 get_avg_by_age_group 函数已被拆分。
# 您需要在 app.py 中将 get_age_group_avg_from_db 函数注册为路由，
# 并确保 calculate_and_store_age_group_avg 函数在需要时被调用（例如，在数据导入或更新后）。
