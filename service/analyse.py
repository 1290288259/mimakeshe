from service.Paillier import PaillierEncryptor  # 导入Paillier加密器
from models import Shuju2  # 导入Shuju2模型
from db_config import db  # 导入数据库配置
FLOAT_PRECISION = 10

class AnalyseService:  # 定义分析服务类
    def __init__(self, group_id=1):  # 初始化方法，接受 group_id 参数，默认为1
        # 创建Paillier加密器实例，并根据 group_id 加载或生成密钥对
        self.encryptor = PaillierEncryptor()
        self.encryptor.load_or_generate_keypair(group_id)

    def sum_encrypted_data(self, encrypted_data_list):  # 对指定加密数据列表的密文求和并返回密文结果
        try:  # 尝试执行以下代码
            if not encrypted_data_list:  # 如果列表为空
                # 返回加密的0，因为求和结果是密文，所以空列表的和也应该是加密的0
                return self.encryptor.encrypt(0)  
            total = self.encryptor.encrypt(0)  # 初始化总和为加密的0
            for ciphertext in encrypted_data_list:  # 遍历所有密文
                # 将密文转换为EncryptedNumber对象，确保可以进行同态加法
                encrypted_number = self.encryptor.public_key.encrypt(0).__class__(self.encryptor.public_key, int(ciphertext))  
                total += encrypted_number  # 累加密文
            return total  # 返回加密的总和
        except Exception as e:  # 捕获异常
            print(f"密文求和失败: {str(e)}")  # 打印错误信息
            return None  # 返回None

    def average_encrypted_data(self, encrypted_data):  
        """
        计算指定列表的加密数据平均值
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
                
            # 调用 sum_encrypted_data 函数来获取密文总和
            encrypted_total = self.sum_encrypted_data(encrypted_data)  # 调用求和函数，现在返回的是密文
            
            if encrypted_total is None: # 如果求和失败
                return None # 返回None

            # 解密总和以计算平均值
            decrypted_total = self.encryptor.decrypt(encrypted_total) # 解密密文总和

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

        

