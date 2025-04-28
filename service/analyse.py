from service.Paillier import PaillierEncryptor  # 导入Paillier加密器
from models import Shuju2  # 导入Shuju2模型
from db_config import db  # 导入数据库配置

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

    def average_encrypted_data(self, field):  # 对指定字段的密文求平均值并解密返回结果
        try:  # 尝试执行以下代码
            records = Shuju2.query.with_entities(getattr(Shuju2, field)).all()
            # 查询指定字段的所有记录
            if not records:  # 如果没有记录
                return 0  # 返回0
            total = self.encryptor.encrypt(0)  # 初始化总和为加密的0
            num = 0  # 初始化记录数为0
            for record in records:  # 遍历所有记录
                ciphertext = int(record[0])  # 获取密文
                encrypted_number = self.encryptor.public_key.encrypt(0).__class__(self.encryptor.public_key, ciphertext)  # 将密文转换为EncryptedNumber对象
                total += encrypted_number  # 累加密文
                num += 1  # 记录数加1
                print(f"{field}当前记录数: {num}")  # 打印当前记录数
            decrypted_total = self.encryptor.decrypt(total)  # 解密最终总和
            average = decrypted_total / len(records)  # 计算平均值
            return average  # 返回平均值
        except Exception as e:  # 捕获异常
            print(f"密文求平均值失败: {str(e)}")  # 打印错误信息
            return None  # 返回None

    def privacy_preserving_intersection(self, field, encrypted_values):  # 隐私求交：返回指定字段与给定密文的交集
        try:  # 尝试执行以下代码
            # 查询指定字段的所有记录
            records = Shuju2.query.with_entities(getattr(Shuju2, field)).all()  # 从数据库中查询指定字段的所有记录
            # 计算交集
            intersection = []  # 初始化交集列表
            for record in records:  # 遍历所有记录
                ciphertext = int(record[0])  # 获取当前记录的密文
                encrypted_record = self.encryptor.encrypt(ciphertext)  # 加密当前记录的密文
                for ev in encrypted_values:  # 遍历给定的密文列表
                    # 使用加法同态计算差值
                    difference = encrypted_record + (ev * -1)  # 计算密文差值
                    decrypted_difference = self.encryptor.decrypt(difference)  # 解密密文差值
                    if decrypted_difference == 0:  # 如果差值为0，说明明文相同
                        intersection.append(self.encryptor.decrypt(encrypted_record))  # 将解密后的明文添加到交集列表
                        break  # 跳出内层循环
            return intersection  # 返回交集列表
        except Exception as e:  # 捕获异常
            print(f"隐私求交失败: {str(e)}")  # 打印错误信息
            return None  # 返回None

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