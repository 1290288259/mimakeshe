import os
import pickle
from phe import paillier  # 导入Paillier加密库

class PaillierEncryptor:
    def __init__(self, key_length=1024):
        # 直接指定密钥文件路径
        self.public_key_file = "e:\\桌面\\zuoye\\密码学课设\\Medical_data_analysis_system\\service\\public_key.pkl"
        self.private_key_file = "e:\\桌面\\zuoye\\密码学课设\\Medical_data_analysis_system\\service\\private_key.pkl"
        
        # 检查密钥文件是否存在
        if os.path.exists(self.public_key_file) and os.path.exists(self.private_key_file):
            # 如果存在，则从文件读取密钥
            with open(self.public_key_file, 'rb') as f:
                self.public_key = pickle.load(f)
            with open(self.private_key_file, 'rb') as f:
                self.private_key = pickle.load(f)
        else:
            # 如果不存在，则生成新的密钥对并保存
            self.public_key, self.private_key = paillier.generate_paillier_keypair(n_length=key_length)
            with open(self.public_key_file, 'wb') as f:
                pickle.dump(self.public_key, f)
            with open(self.private_key_file, 'wb') as f:
                pickle.dump(self.private_key, f)

    def encrypt(self, plaintext):
        """加密数据"""
        # plaintext: 明文数据，支持int, float或list类型
        if isinstance(plaintext, (int, float)):  # 如果明文是int或float类型
            return self.public_key.encrypt(plaintext)  # 使用公钥加密
        elif isinstance(plaintext, list):  # 如果明文是list类型
            return [self.public_key.encrypt(p) for p in plaintext]  # 对列表中的每个元素加密
        else:
            raise TypeError("仅支持int, float或list类型的数据加密")  # 不支持的类型抛出异常

    def decrypt(self, ciphertext):
        """解密数据"""
        # ciphertext: 密文数据，支持EncryptedNumber或list类型
        if isinstance(ciphertext, paillier.EncryptedNumber):  # 如果密文是EncryptedNumber类型
            return self.private_key.decrypt(ciphertext)  # 使用私钥解密
        elif isinstance(ciphertext, list):  # 如果密文是list类型
            return [self.private_key.decrypt(c) for c in ciphertext]  # 对列表中的每个元素解密
        else:
            raise TypeError("仅支持EncryptedNumber或list类型的数据解密")  # 不支持的类型抛出异常

