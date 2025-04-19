from service.Paillier import PaillierEncryptor
from sqlalchemy import create_engine
import pandas as pd

# 初始化Paillier加密器
encryptor = PaillierEncryptor()

# 创建数据库连接
engine = create_engine('mysql://root:123456@localhost/keshe')

# 读取shuju2表的所有内容
df = pd.read_sql('shuju2', con=engine)

# 解密age列的第一个数据
ciphertext = df['age'].iloc[0]  # 获取age列的第一个密文数据
encrypted_number = encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(ciphertext))  # 将密文转换为EncryptedNumber对象
decrypted_value = encryptor.decrypt(encrypted_number)  # 使用私钥解密数据

# 打印解密结果
print("age列的第一个数据的解密结果:", decrypted_value)

# # 加密所有数据（除了id列）
# for col in df.columns:
#     if col != 'id':  # 跳过id列
#         df[col] = df[col].apply(lambda x: str(encryptor.encrypt(x).ciphertext()))

# # 将加密后的数据存入shuju2表
# df.to_sql('shuju2', con=engine, if_exists='replace', index=False)
# print("加密数据已成功存入shuju2表")