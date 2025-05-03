from service.Paillier import PaillierEncryptor  # 导入Paillier加密器
from models import Shuju2  # 导入Shuju2模型
from db_config import db  # 导入数据库配置
FLOAT_PRECISION = 10
class AnalyseService:  # 定义分析服务类
    def __init__(self):  # 初始化方法
        self.encryptor = PaillierEncryptor()  # 创建Paillier加密器实例

    def sum_encrypted_data(self, field):  # 对指定字段的密文求和并解密返回结果
        try:  # 尝试执行以下代码
            records = Shuju2.query.with_entities(getattr(Shuju2, field)).all()  # 查询指定字段的所有记录
            if not records:  # 如果没有记录
                return 0  # 返回0
            total = self.encryptor.encrypt(0)  # 初始化总和为加密的0
            for record in records:  # 遍历所有记录
                ciphertext = int(record[0])  # 获取密文
                encrypted_number = self.encryptor.public_key.encrypt(0).__class__(self.encryptor.public_key, ciphertext)  # 将密文转换为EncryptedNumber对象
                total += encrypted_number  # 累加密文
            return self.encryptor.decrypt(total)  # 解密并返回总和
        except Exception as e:  # 捕获异常
            print(f"密文求和失败: {str(e)}")  # 打印错误信息
            return None  # 返回None

    def average_encrypted_data(self, field):  
        """
        计算指定字段的加密数据平均值
        参数:
            field: 要计算平均值的字段名
        返回:
            解密后的平均值，失败返回None
        """
        try:  
            # 查询记录总数，避免一次性加载所有数据
            record_count = Shuju2.query.count()
            print(f"{field}字段的总记录数: {record_count}")  # 只打印一次总记录数
            
            # 打印所有数据的ID
            
            if record_count == 0:  # 如果没有记录
                return 0  # 返回0
                
            # 分批查询处理，减少内存占用
            batch_size = 50  # 每批处理50条记录
            total = self.encryptor.encrypt(0)  # 初始化总和为加密的0
            
            # 记录处理进度
            processed = 0
            
            # 分批处理数据
            for offset in range(0, record_count, batch_size):
                # 查询一批数据
                batch = Shuju2.query.with_entities(
                    getattr(Shuju2, field)
                ).limit(batch_size).offset(offset).all()
                
                # 处理这批数据
                for record in batch:
                    ciphertext = int(record[0])  # 获取密文
                    encrypted_number = self.encryptor.public_key.encrypt(0).__class__(
                        self.encryptor.public_key, ciphertext)  # 将密文转换为EncryptedNumber对象
                    total += encrypted_number  # 累加密文
                    processed += 1
                
                # 每批次结束打印一次进度，而不是每条记录都打印
                print(f"{field}字段已处理: {processed}/{record_count} ({processed*100/record_count:.1f}%)")
                
            # 解密并计算平均值
            decrypted_total = self.encryptor.decrypt(total)  # 解密最终总和
            average = decrypted_total / record_count  # 计算平均值
            print(f"{field}字段平均值计算完成: {average}")  # 打印计算结果
            return average  # 返回平均值
            
        except ValueError as e:  # 捕获值错误
            print(f"密文求平均值失败(值错误): {str(e)}")  # 打印错误信息
            return None  # 返回None
        except TypeError as e:  # 捕获类型错误
            print(f"密文求平均值失败(类型错误): {str(e)}")  # 打印错误信息
            return None  # 返回None
        except Exception as e:  # 捕获其他异常
            print(f"密文求平均值失败(未知错误): {str(e)}")  # 打印错误信息
            return None  # 返回None

    def privacy_preserving_intersection(self, data_id):  # 隐私求交：根据指定ID的数据与全部数据进行隐私求交
        """
        计算指定ID的数据与数据库中所有数据的交集百分比，并将结果存入analysis_result表
        
        参数:
            data_id (str): 要查询的数据ID
            
        返回:
            float: 交集占总集的百分比
        """
        try:  # 尝试执行以下代码
            # 查询指定ID的数据
            target_record = Shuju2.query.filter_by(id=data_id).first()  # 获取指定ID的记录
            if not target_record:  # 如果没有找到记录
                print(f"没有找到ID为{data_id}的记录")  # 打印提示信息
                return 0  # 返回0（百分比为0）
            
            # 查询所有记录总数
            total_count = Shuju2.query.count()  # 获取总记录数
            if total_count == 0:  # 如果没有记录
                print("没有找到任何记录")  # 打印提示信息
                return 0  # 返回0（百分比为0）
            
            # 获取目标记录的所有字段密文
            target_encrypted = {}  # 初始化目标密文字典
            fields = ['cirrhosis', 'age', 'sex', 'cholesterol', 'triglyceride', 
                     'HDL', 'LDL', 'PathDiagNum', 'BMI', 'ALT', 'AST', 'glucose']  # 所有需要比较的字段
            
            # 获取目标记录的所有字段密文并转换为EncryptedNumber对象
            for field in fields:  # 遍历所有字段
                ciphertext = int(getattr(target_record, field))  # 获取当前字段的密文
                encrypted_value = self.encryptor.public_key.encrypt(0).__class__(
                    self.encryptor.public_key, ciphertext)  # 将密文转换为EncryptedNumber对象
                target_encrypted[field] = encrypted_value  # 存储加密对象
                print(f"目标记录{field}字段密文已获取")  # 打印提示信息
            
            # 初始化各字段的交集计数器
            intersection_counts = {field: 0 for field in fields}  # 初始化各字段交集计数
            
            # 分批查询处理，减少内存占用
            batch_size = 50  # 每批处理50条记录
            
            # 记录处理进度
            processed = 0
            
            # 分批处理数据
            for offset in range(0, total_count, batch_size):
                # 查询一批数据
                batch = Shuju2.query.limit(batch_size).offset(offset).all()
                
                # 处理这批数据
                for record in batch:
                    # 对每个字段进行比较
                    for field in fields:
                        # 跳过与目标记录相同的记录
                        if record.id == data_id:
                            continue
                            
                        # 获取当前记录的密文并转换为EncryptedNumber对象
                        ciphertext = int(getattr(record, field))  # 获取当前记录的密文
                        encrypted_record = self.encryptor.public_key.encrypt(0).__class__(
                            self.encryptor.public_key, ciphertext)  # 将密文转换为EncryptedNumber对象
                        
                        # 计算差值（密文减法）
                        difference = encrypted_record - target_encrypted[field]  # 密文减法
                        
                        # 解密差值
                        decrypted_diff = self.encryptor.decrypt(difference)  # 解密差值
                        
                        # 对LDL和BMI字段，需要除以FLOAT_PRECISION
                        if field in ['LDL', 'BMI']:  # 如果是LDL或BMI字段
                            decrypted_diff = decrypted_diff / FLOAT_PRECISION  # 除以FLOAT_PRECISION
                        
                        # 解密目标值用于计算偏差范围
                        decrypted_target = self.encryptor.decrypt(target_encrypted[field])
                        if field in ['LDL', 'BMI']:  # 如果是LDL或BMI字段
                            decrypted_target = decrypted_target / FLOAT_PRECISION  # 除以FLOAT_PRECISION
                        
                        # 计算偏差百分比
                        if decrypted_target != 0:  # 避免除以零
                            deviation_percentage = abs(decrypted_diff / decrypted_target) * 100  # 计算偏差百分比
                            
                            # 判断偏差是否在5%范围内
                            if deviation_percentage <= 5:  # 如果偏差在5%范围内
                                intersection_counts[field] += 1  # 对应字段的交集计数加1
                    
                    processed += 1  # 处理计数加1
                
                # 每批次结束打印一次进度
                print(f"隐私求交已处理: {processed}/{total_count} ({processed*100/total_count:.1f}%)")
            
            # 计算各字段交集占总集的百分比
            intersection_percentages = {}  # 初始化百分比字典
            for field in fields:
                # 计算百分比时排除目标记录本身
                adjusted_total = total_count - 1  # 总数减1（排除目标记录自身）
                if adjusted_total > 0:  # 避免除以零
                    intersection_percentages[field] = (intersection_counts[field] / adjusted_total) * 100  # 计算百分比
                else:
                    intersection_percentages[field] = 0  # 如果只有一条记录，百分比为0
                    
                print(f"{field}字段交集数量: {intersection_counts[field]}, 调整后总记录数: {adjusted_total}")  # 打印交集数量和总记录数
                print(f"{field}字段交集占总集的百分比: {intersection_percentages[field]:.2f}%")  # 打印百分比，保留两位小数
            
            # 将结果存入Analysis_result表
            from models import Analysis_result  # 导入Analysis_result模型
            
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
            
            # 添加到数据库会话并提交
            db.session.add(result)  # 添加到会话
            db.session.commit()  # 提交到数据库
            print(f"分析结果已保存到analysis_result表，ID: {result.id}")  # 打印保存成功信息
            
            # 返回平均百分比作为总体结果
            avg_percentage = sum(intersection_percentages.values()) / len(intersection_percentages)  # 计算平均百分比
            return avg_percentage  # 返回平均百分比
            
        except Exception as e:  # 捕获异常
            print(f"隐私求交失败: {str(e)}")  # 打印错误信息
            import traceback  # 导入traceback模块
            traceback.print_exc()  # 打印详细错误信息
            db.session.rollback()  # 回滚数据库会话
            return 0  # 出错时返回0

    def get_all_averages(self):
        # 定义可以求平均值的字段列表（已移除sex字段）
        numeric_fields = ['cirrhosis', 'age', 'cholesterol', 
                         'triglyceride', 'HDL', 'LDL', 'BMI', 
                         'ALT', 'AST', 'glucose']
        
        results = {}
        for field in numeric_fields:
            try:
                avg = self.average_encrypted_data(field)
                results[field] = avg
                print(f"{field}的平均值为: {avg}")
            except Exception as e:
                print(f"计算{field}平均值时出错: {str(e)}")
                results[field] = None
        
        return results


    def average_encrypted_list(self, encrypted_list):
        """
        计算传入的密文列表的平均值
        
        参数:
            encrypted_list: 密文数据列表，每个元素为字符串形式的密文
            
        返回:
            解密后的平均值，失败返回None
        """
        try:
            # 检查列表是否为空
            if not encrypted_list or len(encrypted_list) == 0:  # 如果列表为空
                print("密文列表为空")  # 打印提示信息
                return 0  # 返回0
                
            # 获取列表长度
            record_count = len(encrypted_list)  # 记录总数就是列表长度
            print(f"密文列表的总记录数: {record_count}")  # 打印总记录数
            
            # 初始化总和为加密的0
            total = self.encryptor.encrypt(0)  # 初始化总和为加密的0
            
            # 记录处理进度
            processed = 0
            
            # 分批处理数据，减少内存占用
            batch_size = 50  # 每批处理50条记录
            
            # 分批处理数据
            for offset in range(0, record_count, batch_size):
                # 获取当前批次的数据
                batch = encrypted_list[offset:min(offset + batch_size, record_count)]
                
                # 处理这批数据
                for ciphertext_str in batch:
                    # 将字符串形式的密文转换为整数
                    ciphertext = int(ciphertext_str)  # 获取密文
                    
                    # 将密文转换为EncryptedNumber对象
                    encrypted_number = self.encryptor.public_key.encrypt(0).__class__(
                        self.encryptor.public_key, ciphertext)  # 将密文转换为EncryptedNumber对象
                        
                    # 累加密文
                    total += encrypted_number  # 累加密文
                    processed += 1
                
                # 每批次结束打印一次进度
                print(f"密文列表已处理: {processed}/{record_count} ({processed*100/record_count:.1f}%)")
            
            # 解密并计算平均值
            decrypted_total = self.encryptor.decrypt(total)  # 解密最终总和
            average = decrypted_total / record_count  # 计算平均值
            print(f"密文列表平均值计算完成: {average}")  # 打印计算结果
            return average  # 返回平均值
            
        except ValueError as e:  # 捕获值错误
            print(f"密文列表求平均值失败(值错误): {str(e)}")  # 打印错误信息
            return None  # 返回None
        except TypeError as e:  # 捕获类型错误
            print(f"密文列表求平均值失败(类型错误): {str(e)}")  # 打印错误信息
            return None  # 返回None
        except Exception as e:  # 捕获其他异常
            print(f"密文列表求平均值失败(未知错误): {str(e)}")  # 打印错误信息
            return None  # 返回None

    def calculate_avg_by_age_group(self, field_name):
        """
        根据年龄段计算指定字段的平均值
        
        参数:
            field_name (str): 需要计算平均值的字段名称
            
        返回:
            dict: 包含各年龄段平均值的字典，格式为 {'0-9': avg_value, '10-19': avg_value, ...}
        """
        try:
            # 从数据库中查询所有记录
            records = Shuju2.query.all()  # 获取所有记录
            
            if not records:  # 如果没有记录
                print("没有找到任何记录")  # 打印提示信息
                return {}  # 返回空字典
            
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
                    # 解密年龄
                    decrypted_age = self.encryptor.decrypt(
                        self.encryptor.public_key.encrypt(0).__class__(
                            self.encryptor.public_key, int(record.age)
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
            
            # 计算每个年龄段的平均值
            result = {}  # 初始化结果字典
            for age_group, ciphertexts in age_groups.items():
                if ciphertexts:  # 如果该年龄段有数据
                    # 使用average_encrypted_list方法计算平均值
                    avg = self.average_encrypted_list(ciphertexts)
                    
                    # 如果是BMI或LDL字段，将结果除以FLOAT_PRECISION
                    if field_name in ['BMI', 'LDL'] and avg is not None:
                        avg = avg / FLOAT_PRECISION  # 将结果除以FLOAT_PRECISION(10)
                        print(f"{age_group}年龄段的{field_name}平均值(已除以{FLOAT_PRECISION}): {avg}")  # 打印调整后的结果
                    
                    result[age_group] = avg  # 存储结果
                else:
                    result[age_group] = None  # 如果没有数据，设为None
            
            return result  # 返回结果字典
            
        except Exception as e:  # 捕获异常
            print(f"按年龄段计算平均值失败: {str(e)}")  # 打印错误信息
            import traceback  # 导入traceback模块
            traceback.print_exc()  # 打印详细错误信息
            return {}  # 返回空字典