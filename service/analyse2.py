# 导入Paillier加密器，用于同态加密操作
from service.Paillier import PaillierEncryptor

class AnalyseService2:  # 定义一个新的分析服务类，用于处理加密数据
    def __init__(self):  # 初始化方法
        self.encryptor = PaillierEncryptor()  # 创建Paillier加密器实例

    def sum_encrypted_data(self, encrypted_data_list):  # 对指定加密数据列表的密文求和并返回密文结果
        try:  # 尝试执行以下代码
            if not encrypted_data_list:  # 如果传入的加密数据列表为空
                # 返回加密的0，因为空列表的和在同态加密中应表示为加密的零
                return self.encryptor.encrypt(0)  
            
            # 初始化总和为加密的0，这是进行同态加法的起点
            total = self.encryptor.encrypt(0)  
            
            for ciphertext in encrypted_data_list:  # 遍历加密数据列表中的每一个密文
                # 将密文（通常是字符串或整数形式）转换为Paillier库中的EncryptedNumber对象
                # 这样才能进行正确的同态加法操作
                encrypted_number = self.encryptor.public_key.encrypt(0).__class__(self.encryptor.public_key, int(ciphertext))  
                total += encrypted_number  # 将当前密文累加到总和中
            
            return total  # 返回加密的总和，而不是解密后的结果
        except Exception as e:  # 捕获执行过程中可能发生的任何异常
            print(f"密文求和失败: {str(e)}")  # 打印错误信息，帮助调试
            return None  # 如果发生错误，返回None

    # 您可以在这里添加其他与analyse2.py相关的函数