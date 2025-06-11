import os
import pickle
from phe import paillier  # 导入Paillier加密库

class PaillierEncryptor:
    def __init__(self, key_length=1024):
        self.key_length = key_length
        self.public_key = None
        self.private_key = None
        self.public_key_file = None
        self.private_key_file = None
        # 默认加载或生成第一个密钥对
        self.load_or_generate_keypair(1)

    def _get_key_filenames(self, index):
        """根据索引获取密钥文件的路径"""
        
        return (
                f"e:\\桌面\\zuoye\\密码学课设\\Medical_data_analysis_system\\service\\public_key\\public_key{index}.pkl",
                f"e:\\桌面\\zuoye\\密码学课设\\Medical_data_analysis_system\\service\\private_key\\private_key{index}.pkl"
            )

    def load_keypair(self, index):
        """加载指定索引的密钥对"""
        pub_file, priv_file = self._get_key_filenames(index)
        if os.path.exists(pub_file) and os.path.exists(priv_file):
            with open(pub_file, 'rb') as f:
                self.public_key = pickle.load(f)
            with open(priv_file, 'rb') as f:
                self.private_key = pickle.load(f)
            print(f"已加载密钥对：{pub_file} 和 {priv_file}")
            self.public_key_file = pub_file
            self.private_key_file = priv_file
            return True
        return False

    def generate_keypair(self, index):
        """生成指定索引的密钥对"""
        pub_file, priv_file = self._get_key_filenames(index)
        # 检查文件是否已存在，如果存在则抛出异常
        if os.path.exists(pub_file) or os.path.exists(priv_file):
            raise FileExistsError(f"密钥文件已存在：{pub_file} 或 {priv_file}，请选择其他索引或删除现有文件。")

        self.public_key, self.private_key = paillier.generate_paillier_keypair(n_length=self.key_length)
        with open(pub_file, 'wb') as f:
            pickle.dump(self.public_key, f)
        with open(priv_file, 'wb') as f:
            pickle.dump(self.private_key, f)
        print(f"已生成并保存新的密钥对：{pub_file} 和 {priv_file}")
        self.public_key_file = pub_file
        self.private_key_file = priv_file

    def load_or_generate_keypair(self, index=None):
        """加载或生成指定索引的密钥对"""
        if index is None:
            # 如果未指定索引，则查找下一个可用的索引
            index = self._find_next_key_index()

        if not self.load_keypair(index):
            # 如果加载失败，则生成新的密钥对
            self.generate_keypair(index)

    def _find_next_key_index(self):
        """查找下一个可用的密钥文件索引"""
        index = 1
        while True:
            pub_file, priv_file = self._get_key_filenames(index)
            if not os.path.exists(pub_file) or not os.path.exists(priv_file):
                return index
            index += 1

    def encrypt(self, plaintext):
        """加密数据"""
        # plaintext: 明文数据，支持int, float或list类型
        if self.public_key is None:
            raise ValueError("公钥未加载，请先加载或生成密钥对。")
        if isinstance(plaintext, (int, float)):  # 如果明文是int或float类型
            return self.public_key.encrypt(plaintext)  # 使用公钥加密
        elif isinstance(plaintext, list):  # 如果明文是list类型
            return [self.public_key.encrypt(p) for p in plaintext]  # 对列表中的每个元素加密
        else:
            raise TypeError("仅支持int, float或list类型的数据加密")  # 不支持的类型抛出异常

    def decrypt(self, ciphertext):
        """解密数据"""
        # ciphertext: 密文数据，支持EncryptedNumber或list类型
        if self.private_key is None:
            raise ValueError("私钥未加载，请先加载或生成密钥对。")
        if isinstance(ciphertext, paillier.EncryptedNumber):  # 如果密文是EncryptedNumber类型
            return self.private_key.decrypt(ciphertext)  # 使用私钥解密
        elif isinstance(ciphertext, list):  # 如果密文是list类型
            return [self.private_key.decrypt(c) for c in ciphertext]  # 对列表中的每个元素解密
        else:
            raise TypeError("仅支持EncryptedNumber或list类型的数据解密")  # 不支持的类型抛出异常

    def get_current_key_info(self):
        """获取当前加载的密钥信息"""
        if self.public_key_file and self.private_key_file:
            return {
                "public_key_file": self.public_key_file,
                "private_key_file": self.private_key_file
            }
        return "当前没有加载任何密钥对。"

    def list_all_key_pairs(self):
        """列出所有已存在的密钥对"""
        key_pairs = []
        index = 1
        while True:
            pub_file, priv_file = self._get_key_filenames(index)
            if os.path.exists(pub_file) and os.path.exists(priv_file):
                key_pairs.append({"index": index, "public_key": pub_file, "private_key": priv_file})
            else:
                # 如果public_key.pkl不存在，但public_key2.pkl存在，说明中间有缺失，继续查找
                # 否则，如果第一个不存在，或者连续两个不存在，则停止查找
                if index > 1 and (not os.path.exists(self._get_key_filenames(index-1)[0]) or not os.path.exists(pub_file)):
                    break
                elif index == 1 and not os.path.exists(pub_file):
                    break
            index += 1
        return key_pairs

