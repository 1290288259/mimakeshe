import pandas as pd
from sqlalchemy import create_engine
from Paillier import PaillierEncryptor

def encrypt_and_store_data():
    try:
        # 创建数据库连接
        engine = create_engine('mysql://root:123456@localhost/keshe')
        
        # 读取shuju表数据
        df = pd.read_sql('shuju', con=engine)
        
        # 初始化Paillier加密器
        encryptor = PaillierEncryptor()
        
        # 对数值型列进行加密
        for col in df.select_dtypes(include=['int64', 'float64']).columns:
            df[col] = df[col].apply(lambda x: str(encryptor.encrypt(x).ciphertext()) if pd.notna(x) else None)
        
        # 将加密后的数据存入shuju2表
        df.to_sql('shuju2', con=engine, if_exists='replace', index=False)
        print("数据加密并成功存入shuju2表")
    except Exception as e:
        print(f"操作失败: {e}")


def decrypt_and_store_data():
    try:
        # 创建数据库连接
        engine = create_engine('mysql://root:123456@localhost/keshe')
        
        # 读取shuju2表数据
        df = pd.read_sql('shuju2', con=engine)
        
        # 初始化Paillier加密器
        encryptor = PaillierEncryptor()
        
        # 对数值型列进行解密
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].apply(lambda x: encryptor.decrypt(encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(float(x)))) if pd.notna(x) and x != 'inf' and x != '-inf' else None)
            df[col] = df[col].astype(float)  # 将解密后的数据转换为浮点数
        
        # 将解密后的数据存入shuju3表
        df.to_sql('shuju3', con=engine, if_exists='replace', index=False)
        print("数据解密并成功存入shuju3表")
    except Exception as e:
        print(f"操作失败: {e}")

if __name__ == "__main__":
    decrypt_and_store_data()