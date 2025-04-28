import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from Paillier import PaillierEncryptor  # 导入Paillier加密器
FLOAT_PRECISION = 10
# 初始化加密器
encryptor = PaillierEncryptor()

try:
    # 读取CSV文件
    csv_path = 'E:\\桌面\\zuoye\\密码学课设\\Medical_data_analysis_system\\static\\hepatitis_C_EHRs_Japan.csv'
    df = pd.read_csv(csv_path)

    # 添加自增id列
    df.insert(0, 'id', range(1, len(df) + 1))

    # 创建数据库连接
    engine = create_engine('mysql://root:123456@localhost/keshe')

    # 存入MySQL
    df.to_sql('shuju', con=engine, if_exists='append', index=False)
    print("数据成功导入数据库")
except FileNotFoundError:
    print(f"错误：CSV文件未找到，路径为 {csv_path}")
except SQLAlchemyError as e:
    print(f"数据库操作失败: {e}")
except Exception as e:
    print(f"发生未知错误: {e}")
    
df = pd.read_sql('shuju', con=engine)
# 加密所有数据（除了id列）
for col in df.columns:
    if col != 'id':  # 跳过id列
        if col in ['BMI', 'LDL']:  # 对BMI和LDL字段乘以浮点型精度
            df[col] = df[col].apply(lambda x: str(encryptor.encrypt(int(float(x) * FLOAT_PRECISION)).ciphertext()))
        else:
            df[col] = df[col].apply(lambda x: str(encryptor.encrypt(int(float(x))).ciphertext()))

# 将加密后的数据存入shuju2表
df.to_sql('shuju2', con=engine, if_exists='replace', index=False)
print("加密数据已成功存入shuju2表")