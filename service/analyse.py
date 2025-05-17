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

    def average_encrypted_data(self, encrypted_data):  
        """
        计算指定字段的加密数据平均值
        参数:
            encrypted_data: 要计算平均值的加密数据列表
        返回:
            解密后的平均值，失败返回None
        """
        try:  
            # 计算记录总数
            record_count = len(encrypted_data)  # 直接从列表长度获取记录总数
            
            # 打印记录总数
            print(f"总记录数: {record_count}")  # 打印总记录数
            
            if record_count == 0:  # 如果没有记录
                return 0  # 返回0
                
            # 初始化总和为加密的0
            total = self.encryptor.encrypt(0)  # 初始化总和为加密的0
            
            # 记录处理进度
            processed = 0
            
            # 处理所有数据
            for ciphertext in encrypted_data:
                # 将密文转换为EncryptedNumber对象
                encrypted_number = self.encryptor.public_key.encrypt(0).__class__(
                    self.encryptor.public_key, int(ciphertext))  # 将密文转换为EncryptedNumber对象
                total += encrypted_number  # 累加密文
                processed += 1
                
                # 每处理50条记录打印一次进度
                if processed % 50 == 0:
                    print(f"已处理: {processed}/{record_count} ({processed*100/record_count:.1f}%)")
            
            # 解密并计算平均值
            decrypted_total = self.encryptor.decrypt(total)  # 解密最终总和
            average = decrypted_total / record_count  # 计算平均值
            print(f"平均值计算完成: {average}")  # 打印计算结果
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

   
    def privacy_preserving_exact_match(self, target_value, all_values):
        """
        计算目标值与所有值列表中完全匹配的百分比
        
        参数:
            target_value: 目标加密值
            all_values: 所有加密值的列表
            
        返回:
            float: 匹配的百分比
        """
        try:  # 尝试执行以下代码
            # 检查目标值是否存在
            if target_value is None:  # 如果目标值为空
                print("目标值为空")  # 打印提示信息
                return 0  # 返回0（百分比为0）
            
            # 检查值列表是否为空
            total_count = len(all_values)  # 获取总数
            if total_count == 0:  # 如果没有值
                print("值列表为空")  # 打印提示信息
                return 0  # 返回0（百分比为0）
            
            # 将目标值转换为EncryptedNumber对象
            target_encrypted = self.encryptor.public_key.encrypt(0).__class__(
                self.encryptor.public_key, int(target_value))  # 将密文转换为EncryptedNumber对象
            
            # 初始化匹配计数器
            match_count = 0  # 初始化匹配计数
            
            # 记录处理进度
            processed = 0
            
            # 处理所有数据
            for value in all_values:
                # 跳过与目标值相同的记录（如果是同一条记录的同一字段）
                if value == target_value:
                    continue
                    
                # 将当前值转换为EncryptedNumber对象
                encrypted_value = self.encryptor.public_key.encrypt(0).__class__(
                    self.encryptor.public_key, int(value))
                
                # 计算差值（密文减法）
                difference = encrypted_value - target_encrypted
                
                # 解密差值
                decrypted_diff = self.encryptor.decrypt(difference)
                
                # 判断是否完全匹配
                if decrypted_diff == 0:
                    match_count += 1
                
                processed += 1
                
                # 每处理50条记录打印一次进度
                if processed % 50 == 0:
                    print(f"完全匹配已处理: {processed}/{total_count} ({processed*100/total_count:.1f}%)")
            
            # 计算匹配百分比
            if total_count > 0:  # 避免除以零
                match_percentage = (match_count / total_count) * 100  # 计算百分比
            else:
                match_percentage = 0  # 如果没有记录，百分比为0
                
            print(f"完全匹配数量: {match_count}, 总数: {total_count}")  # 打印匹配数量和总数
            print(f"完全匹配百分比: {match_percentage:.2f}%")  # 打印百分比，保留两位小数
            
            return match_percentage  # 返回匹配百分比
            
        except Exception as e:  # 捕获异常
            print(f"完全匹配计算失败: {str(e)}")  # 打印错误信息
            import traceback  # 导入traceback模块
            traceback.print_exc()  # 打印详细错误信息
            return 0  # 出错时返回0
    
    def privacy_preserving_fuzzy_match(self, target_value, all_values, precision_factor=None):
        """
        计算目标值与所有值列表中模糊匹配的百分比（偏差在5%范围内）
        
        参数:
            target_value: 目标加密值
            all_values: 所有加密值的列表
            precision_factor: 精度因子，用于处理浮点数字段（如LDL、BMI等）
            
        返回:
            float: 匹配的百分比
        """
        try:  # 尝试执行以下代码
            # 检查目标值是否存在
            if target_value is None:  # 如果目标值为空
                print("目标值为空")  # 打印提示信息
                return 0  # 返回0（百分比为0）
            
            # 检查值列表是否为空
            total_count = len(all_values)  # 获取总数
            if total_count == 0:  # 如果没有值
                print("值列表为空")  # 打印提示信息
                return 0  # 返回0（百分比为0）
            
            # 将目标值转换为EncryptedNumber对象
            target_encrypted = self.encryptor.public_key.encrypt(0).__class__(
                self.encryptor.public_key, int(target_value))  # 将密文转换为EncryptedNumber对象
            
            # 初始化匹配计数器
            match_count = 0  # 初始化匹配计数
            
            # 记录处理进度
            processed = 0
            
            # 解密目标值用于计算偏差范围
            decrypted_target = self.encryptor.decrypt(target_encrypted)
            
            # 如果有精度因子，应用于目标值
            if precision_factor:
                decrypted_target = decrypted_target / precision_factor
            
            # 处理所有数据
            for value in all_values:
                # 跳过与目标值相同的记录（如果是同一条记录的同一字段）
                if value == target_value:
                    continue
                    
                # 将当前值转换为EncryptedNumber对象
                encrypted_value = self.encryptor.public_key.encrypt(0).__class__(
                    self.encryptor.public_key, int(value))
                
                # 计算差值（密文减法）
                difference = encrypted_value - target_encrypted
                
                # 解密差值
                decrypted_diff = self.encryptor.decrypt(difference)
                
                # 如果有精度因子，应用于差值
                if precision_factor:
                    decrypted_diff = decrypted_diff / precision_factor
                
                # 判断是否模糊匹配（偏差在5%范围内）
                if decrypted_target != 0:  # 避免除以零
                    deviation_percentage = abs(decrypted_diff / decrypted_target) * 100
                    if deviation_percentage <= 5:  # 偏差在5%范围内
                        match_count += 1
                
                processed += 1
                
                # 每处理50条记录打印一次进度
                if processed % 50 == 0:
                    print(f"模糊匹配已处理: {processed}/{total_count} ({processed*100/total_count:.1f}%)")
            
            # 计算匹配百分比
            if total_count > 0:  # 避免除以零
                match_percentage = (match_count / total_count) * 100  # 计算百分比
            else:
                match_percentage = 0  # 如果没有记录，百分比为0
                
            print(f"模糊匹配数量: {match_count}, 总数: {total_count}")  # 打印匹配数量和总数
            print(f"模糊匹配百分比: {match_percentage:.2f}%")  # 打印百分比，保留两位小数
            
            return match_percentage  # 返回匹配百分比
            
        except Exception as e:  # 捕获异常
            print(f"模糊匹配计算失败: {str(e)}")  # 打印错误信息
            import traceback  # 导入traceback模块
            traceback.print_exc()  # 打印详细错误信息
            return 0  # 出错时返回0

        

