from Paillier import PaillierEncryptor
from ..db_config import db
import pandas as pd

# 初始化Paillier加密器
encryptor = PaillierEncryptor()

# 使用db_config中的db对象创建数据库连接
engine = db.engine

# 读取shuju表的所有内容
df = pd.read_sql('shuju', con=engine)

# 加密所有列（除了id列）
for col in df.columns:
    if col != 'id':  # 跳过id列
        df[f'{col}_encrypted'] = df[col].apply(lambda x: str(encryptor.encrypt(x).ciphertext()))

# 将加密后的数据存入shuju2表
df.to_sql('shuju2', con=engine, if_exists='replace', index=False)
print("加密数据已成功存入shuju2表")